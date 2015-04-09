import compiler, astpp, varAnalysis
from compiler.ast import *
from HelperClasses import *

def declassifyModule(ast, gen, name, scopes, strings):
	#go through the top level scope and add the variables to the dictionary
	write, read = varAnalysis.getVars(ast.node)
	ast.node = declassify(ast.node, gen, name, (set(), write), strings)

def declassifyStmt(ast, gen, name, scopes, strings):
	return Stmt([declassify(n, gen, name, scopes, strings) for n in ast.nodes])

def declassifyPrintnl(ast, gen, name, scopes, strings):
	return Printnl([declassify(ast.nodes[0], gen, name, scopes, strings)], None)

def declassifyConst(ast, gen, name, scopes, strings):
	return ast

def declassifyUnarySub(ast, gen, name, scopes, strings):
	return UnarySub(declassify(ast.expr, gen, name, scopes, strings))

def declassifyAdd(ast, gen, name, scopes, strings):
	return Add([declassify(ast.left, gen, name, scopes, strings), declassify(ast.right, gen, name, scopes, strings)])

def declassifyDiscard(ast, gen, name, scopes, strings):
	return Discard(declassify(ast.expr, gen, name, scopes, strings))

def declassifyAssign(ast, gen, name, scopes, strings):
	lhs = ast.nodes[0]
	if isinstance(lhs, AssName) and name:
		return Assign([AssName(gen.inc().name(), "OP_ASSIGN")], CallRuntime(Name("set_attr"), [name, Const(lhs.name), declassify(ast.expr, gen, name, scopes, strings)]))
	elif isinstance(lhs, AssAttr):
		return Assign(
			[AssName(gen.inc().name(), "OP_ASSIGN")], 
			CallRuntime(
				Name("set_attr"), 
				[
					declassify(lhs.expr, gen, name, scopes, strings), 
					Const(lhs.attrname), 
					declassify(ast.expr, gen, name, scopes, strings)
				]
			)
		)
	return Assign([declassify(lhs, gen, name, scopes, strings)], declassify(ast.expr, gen, name, scopes, strings))

def declassifyName(ast, gen, name, scopes, strings):
	#print "declassifyName:",ast, "name:",name
	if name and ast.name != "True" and ast.name != "False":
		#This is an attribute access
		#TODO use the more efficient method
		strings.add(ast.name)
		return IfExp(
			InjectFrom("bool", CallRuntime(Name("has_attr"),[name, Const(ast.name)])),
			CallRuntime(Name("get_attr"),[name, Const(ast.name)]),
			ast
		)
	return ast

def declassifyAssName(ast, gen, name, scopes, strings):
	return ast

def declassifyCallFunc(ast, gen, name, scopes, strings):
	return CallFunc(declassify(ast.node, gen, name, scopes, strings), [declassify(arg, gen, name, scopes, strings) for arg in ast.args])

def declassifyCompare(ast, gen, name, scopes, strings):
	return Compare(declassify(ast.expr, gen, name, scopes, strings), [(ast.ops[0][0], declassify(ast.ops[0][1], gen, name, scopes, strings))])

def declassifyOr(ast, gen, name, scopes, strings):
	return Or([declassify(ast.nodes[0], gen, name, scopes, strings),declassify(ast.nodes[1], gen, name, scopes, strings)])

def declassifyAnd(ast, gen, name, scopes, strings):
	return And([declassify(ast.nodes[0], gen, name, scopes, strings),declassify(ast.nodes[1], gen, name, scopes, strings)])

def declassifyNot(ast, gen, name, scopes, strings):
	return Not(declassify(ast.expr, gen, name, scopes, strings))

def declassifyList(ast, gen, name, scopes, strings):
	return List([declassify(n, gen, name, scopes, strings) for n in ast.nodes])

def declassifyDict(ast, gen, name, scopes, strings):
	return Dict([(declassify(k, gen, name, scopes, strings), declassify(v, gen, name, scopes, strings)) for (k, v) in ast.items])

def declassifySubscript(ast, gen, name, scopes, strings):
	return Subscript(declassify(ast.expr, gen, name, scopes, strings), ast.flags, [declassify(sub, gen, name, scopes, strings) for sub in ast.subs])

def declassifyIfExp(ast, gen, name, scopes, strings):
	return IfExp(
		declassify(ast.test, gen, name, scopes, strings),
		declassify(ast.then, gen, name, scopes, strings),
		declassify(ast.else_, gen, name, scopes, strings)
	)

def declassifyIf(ast, gen, name, scopes, strings):
	return If(
		[(declassify(ast.tests[0][0], gen, name, scopes, strings),
		declassify(ast.tests[0][1], gen, name, scopes, strings))],
		declassify(ast.else_, gen, name, scopes, strings)
	)

def declassifyFunction(ast, gen, name, scopes, strings):
	ast.code = declassify(ast.code, gen, None, (set(),set()), strings)
	if not isinstance(ast.code.nodes[-1], Return):
		ast.code.nodes.append(Return(Const(0)))
	if name:
		oldFuncName = ast.name
		newFuncName = oldFuncName + "$"+name.name
		ast.name = newFuncName
		return Let(
			Name(oldFuncName),
			ast,
			CallRuntime(
				Name("set_attr"),
				[name, Const(oldFuncName), Name(newFuncName)]
			)
		)
	return ast

def declassifyLambda(ast, gen, name, scopes, strings):
	return Lambda(
		[declassify(a, gen, None, (set(),set()), strings) for a in ast.argnames], 
		ast.defaults, 
		ast.flags, 
		declassify(ast.code, gen, None, (set(),set()), strings)
	)

def declassifyReturn(ast, gen, name, scopes, strings):
	return Return(declassify(ast.value, gen, name, scopes, strings))

def declassifyWhile(ast, gen, name, scopes, strings):
	#TODO: Remove this horrendous hack
	ast.body.nodes = [Assign([AssName("HorrendousHack", "OP_ASSIGN")], List([Const(0)]))] + ast.body.nodes
	#This has to do with a problem in liveness, not here. This is just the first function called.
	return While(declassify(ast.test, gen, name, scopes, strings), declassify(ast.body, gen, name, scopes, strings), None)

def declassifyClass(ast, gen, name, scopes, strings):
	name = Name(gen.inc().name())
	#read, write = varAnalysis.getVars(ast.code)
	#print "ast.code",ast.code
	#print "class body"
	write, read = varAnalysis.getVars(ast.code)
	scopes = (scopes[1], write)
	newbody = declassify(ast.code, gen, name, scopes, strings)
	#astpp.printAst(newbody)
	newbody.nodes.append(Assign([AssName(ast.name, "OP_ASSIGN")], name))
	#astpp.printAst(newbody)
	#print "end class body"
	return Let(
		name, 
		InjectFrom("big", CallRuntime(Name("create_class"),[List(ast.bases)])),
		newbody
	)

def declassifyAssAttr(ast, gen, name, scopes, strings):
	raise NotImplementedError

def declassifyGetattr(ast, gen, name, scopes, strings):
	return CallRuntime(Name("get_attr"), [declassify(ast.expr, gen, name, scopes, strings), Const(ast.attrname)])

def declassify(ast, gen, name, scopes, strings):
	#print "declassify:",ast
	#This str check is likely hacky. declassifyLambda's argnames can be strings
	#and can therefore pass a string into here at line 120. 
	if isinstance(ast, str):
		return ast
	return {
		Module:    declassifyModule,
		Stmt:      declassifyStmt,
		Printnl:   declassifyPrintnl,
		Const:     declassifyConst,
		UnarySub:  declassifyUnarySub,
		Add:       declassifyAdd,
		Discard:   declassifyDiscard,
		Assign:    declassifyAssign,
		Name:      declassifyName,
		AssName:   declassifyAssName,
		CallFunc:  declassifyCallFunc,
		Compare:   declassifyCompare,
		Or:        declassifyOr,
		And:       declassifyAnd,
		Not:       declassifyNot,
		List:      declassifyList,
		Dict:      declassifyDict,
		Subscript: declassifySubscript,
		IfExp:     declassifyIfExp,
		If:        declassifyIf,
		Function:  declassifyFunction,
		Lambda:    declassifyLambda,
		Return:    declassifyReturn,
		While:     declassifyWhile,
		Class:     declassifyClass,
		AssAttr:   declassifyAssAttr,
		Getattr:   declassifyGetattr
	}[ast.__class__](ast, gen, name, scopes, strings)
