import compiler, astpp, varAnalysis
from compiler.ast import *
from HelperClasses import *

def declassifyModule(ast, gen, name, strings):
	ast.node = declassify(ast.node, gen, name, strings)

def declassifyStmt(ast, gen, name, strings):
	return Stmt([declassify(n, gen, name, strings) for n in ast.nodes])

def declassifyPrintnl(ast, gen, name, strings):
	return Printnl([declassify(ast.nodes[0], gen, name, strings)], None)

def declassifyConst(ast, gen, name, strings):
	#Hack
	if ast.value == None:
		return Const(0)
	return ast

def declassifyUnarySub(ast, gen, name, strings):
	return UnarySub(declassify(ast.expr, gen, name, strings))

def declassifyAdd(ast, gen, name, strings):
	return Add([declassify(ast.left, gen, name, strings), declassify(ast.right, gen, name, strings)])

def declassifyDiscard(ast, gen, name, strings):
	return Discard(declassify(ast.expr, gen, name, strings))

def declassifyAssign(ast, gen, name, strings):
	lhs = ast.nodes[0]
	if isinstance(lhs, AssName) and name:
		return Assign([AssName(gen.inc().name(), "OP_ASSIGN")], CallRuntime(Name("set_attr"), [name, Const(lhs.name), declassify(ast.expr, gen, name, strings)]))
	elif isinstance(lhs, AssAttr):
		return Assign(
			[AssName(gen.inc().name(), "OP_ASSIGN")], 
			CallRuntime(
				Name("set_attr"), 
				[
					declassify(lhs.expr, gen, name, strings), 
					Const(lhs.attrname), 
					declassify(ast.expr, gen, name, strings)
				]
			)
		)
	return Assign([declassify(lhs, gen, name, strings)], declassify(ast.expr, gen, name, strings))

def declassifyName(ast, gen, name, strings):
	if name and ast.name != "True" and ast.name != "False":
		#This is an attribute access
		strings.add(ast.name)
		return IfExp(
			InjectFrom("bool", CallRuntime(Name("has_attr"),[name, Const(ast.name)])),
			CallRuntime(Name("get_attr"),[name, Const(ast.name)]),
			ast
		)
	return ast

def declassifyAssName(ast, gen, name, strings):
	return ast

def declassifyCallFunc(ast, gen, name, strings):
	#Make input() a call to runtime
	if isinstance(ast.node, Name) and ast.node.name == "input":
		return CallRuntime(Name("input_int"), [declassify(arg, gen, name, strings) for arg in ast.args])
	return CallFunc(declassify(ast.node, gen, name, strings), [declassify(arg, gen, name, strings) for arg in ast.args])

def declassifyCompare(ast, gen, name, strings):
	return Compare(declassify(ast.expr, gen, name, strings), [(ast.ops[0][0], declassify(ast.ops[0][1], gen, name, strings))])

def declassifyOr(ast, gen, name, strings):
	return Or([declassify(ast.nodes[0], gen, name, strings),declassify(ast.nodes[1], gen, name, strings)])

def declassifyAnd(ast, gen, name, strings):
	return And([declassify(ast.nodes[0], gen, name, strings),declassify(ast.nodes[1], gen, name, strings)])

def declassifyNot(ast, gen, name, strings):
	return Not(declassify(ast.expr, gen, name, strings))

def declassifyList(ast, gen, name, strings):
	return List([declassify(n, gen, name, strings) for n in ast.nodes])

def declassifyDict(ast, gen, name, strings):
	return Dict([(declassify(k, gen, name, strings), declassify(v, gen, name, strings)) for (k, v) in ast.items])

def declassifySubscript(ast, gen, name, strings):
	return Subscript(declassify(ast.expr, gen, name, strings), ast.flags, [declassify(sub, gen, name, strings) for sub in ast.subs])

def declassifyIfExp(ast, gen, name, strings):
	return IfExp(
		declassify(ast.test, gen, name, strings),
		declassify(ast.then, gen, name, strings),
		declassify(ast.else_, gen, name, strings)
	)

def declassifyIf(ast, gen, name, strings):
	return If(
		[(declassify(ast.tests[0][0], gen, name, strings),
		declassify(ast.tests[0][1], gen, name, strings))],
		declassify(ast.else_, gen, name, strings) if ast.else_ else Stmt([Discard(Const(0))])
	)

def declassifyFunction(ast, gen, name, strings):
	ast.code = declassify(ast.code, gen, None, strings)
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

def declassifyLambda(ast, gen, name, strings):
	return Lambda(
		ast.argnames, 
		ast.defaults, 
		ast.flags, 
		declassify(ast.code, gen, None, strings)
	)

def declassifyReturn(ast, gen, name, strings):
	return Return(declassify(ast.value, gen, name, strings))

def declassifyWhile(ast, gen, name, strings):
	return While(declassify(ast.test, gen, name, strings), declassify(ast.body, gen, name, strings), None)

def declassifyClass(ast, gen, name, strings):
	superName = name
	name = Name(gen.inc().name())
	write, read = varAnalysis.getVars(ast.code)
	newbody = declassify(ast.code, gen, name, strings)
	newbody.nodes.append(Assign([AssName(ast.name, "OP_ASSIGN")], name))
	#If this is a nested class, set attr of parent class
	if superName:
		newbody.nodes.append(Discard(CallRuntime(Name("set_attr"), [superName, Const(ast.name), name])))
	
	return Let(
		name, 
		InjectFrom("big", CallRuntime(Name("create_class"),[List(ast.bases)])),
		newbody
	)

def declassifyAssAttr(ast, gen, name, strings):
	raise NotImplementedError

def declassifyGetattr(ast, gen, name, strings):
	return CallRuntime(Name("get_attr"), [declassify(ast.expr, gen, name, strings), Const(ast.attrname)])

def declassify(ast, gen, name, strings):
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
	}[ast.__class__](ast, gen, name, strings)
