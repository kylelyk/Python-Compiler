import compiler
from compiler.ast import *
from HelperClasses import *

debug = False

def addAssign(node, newast, gen, map, strings, name = None):
	if isinstance(name, Name):
		raise TypeError
	if not name:
		name = gen.inc().name()
		map[name] = len(map)
	elif name not in map:
		map[name] = len(map)
	if isinstance(node, tuple):
		raise NotImplementedError
	newnode = Assign([AssName(name, 'OP_ASSIGN')], node)
	newast.nodes.append(newnode)
	return Name(name)

def flatStmt(ast, newast, gen, map, strings):
	for node in ast.nodes:
		flatten(node, newast, gen, map, strings)

def flatPrintnl(ast, newast, gen, map, strings):
	simple = flatten(ast.nodes[0], newast, gen, map, strings)
	return newast.nodes.append(CallRuntime(Name("print_any"),[simple]))

def flatConst(ast, newast, gen, map, strings):
	#Do not inject if its a str constant (for throwing errors and storing)
	if isinstance(ast.value, str):
		if ast.value[0] != "$":
			strings.add(ast.value)
		return ast
	else:
		return addAssign(CallRuntime(Name("inject_int"),[ast]), newast, gen, map, strings)

def flatName(ast, newast, gen, map, strings):
	return ast

def flatUnarySub(ast, newast, gen, map, strings):
	simple = flatten(ast.expr, newast, gen, map, strings)
	if isinstance(simple, Const):
		return Const(-simple.value)
	return addAssign(UnarySub(simple), newast, gen, map, strings)

def flatAdd(ast, newast, gen, map, strings):
	s1 = flatten(ast.left, newast, gen, map, strings)
	s2 = flatten(ast.right, newast, gen, map, strings)
	return addAssign(Add((s1, s2)), newast, gen, map, strings)

def flatDiscard(ast, newast, gen, map, strings):
	return flatten(ast.expr, newast, gen, map, strings)

def flatAssName(ast, newast, gen, map, strings):
	return ast.name

def flatAssign(ast, newast, gen, map, strings):
	#TODO remove this hack
	rhs = flatten(ast.expr, newast, gen, map, strings)
	lhs = flatten(ast.nodes[0], newast, gen, map, strings)
	if isinstance(lhs, Subscript):
		return flatten(CallRuntime(Name("set_subscript"),[lhs.expr, lhs.subs[0], rhs]), newast, gen, map, strings)
	elif isinstance(lhs, AssAttr):
		return addAssign(CallRuntime(Name("set_attr"),[lhs.expr, Const(lhs.attrname), rhs]), newast, gen, map, strings)
	else:
		return addAssign(rhs, newast, gen, map, strings, lhs)

def flatCallFunc(ast, newast, gen, map, strings):
	return addAssign(CallFunc(
		flatten(ast.node, newast, gen, map, strings),
		[flatten(n, newast, gen, map, strings) for n in ast.args]
	),newast, gen, map, strings)

def flatCallRuntime(ast, newast, gen, map, strings):
	return addAssign(CallRuntime(
		ast.node,
		[flatten(n, newast, gen, map, strings) for n in ast.args]
	),newast, gen, map, strings)

def flatCompare(ast, newast, gen, map, strings):
	s1 = flatten(ast.expr, newast, gen, map, strings)
	s2 = flatten(ast.ops[0][1], newast, gen, map, strings)
	return addAssign(Compare(s1,[(ast.ops[0][0], s2)]), newast, gen, map, strings)

def flatOr(ast, newast, gen, map, strings):
	'''Warning, does not implement short-circuiting.
	Only code generated in the explicate pass should reach here which 
	does not rely on short-circuiting.
	This Node performs the bitwise Or operation.'''
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(Or([prev, new]), newast, gen, map, strings)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map, strings)
		s2 = flatten(ast.nodes[1], newast, gen, map, strings)
		return addAssign(Or([s1, s2]), newast, gen, map, strings)

def flatAnd(ast, newast, gen, map, strings):
	'''Warning, does not implement short-circuiting.
	Only code generated in the explicate pass should reach here which 
	does not rely on short-circuiting.
	This Node performs the bitwise And operation.'''
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(And([prev, new]), newast, gen, map, strings)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map, strings)
		s2 = flatten(ast.nodes[1], newast, gen, map, strings)
		return addAssign(And([s1, s2]), newast, gen, map, strings)

def flatBitxor(ast, newast, gen, map, strings):
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(Bitxor([prev, new]), newast, gen, map, strings)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map, strings)
		s2 = flatten(ast.nodes[1], newast, gen, map, strings)
		return addAssign(Bitxor([s1, s2]), newast, gen, map, strings)

def flatNot(ast, newast, gen, map, strings):
	#TODO fix this hack
	return flatten(InjectFrom("bool", Bitxor([CallRuntime(Name("is_true"),[flatten(ast.expr, newast, gen, map, strings)]), ProjectTo("int",Const(1))])), newast, gen, map, strings)

def flatList(ast, newast, gen, map, strings):
	listName = flatten(InjectFrom("big",CallRuntime(Name("create_list"),[Const(len(ast.nodes))])), newast, gen, map, strings)
	for i,n in enumerate(ast.nodes):
		flatten(CallRuntime(Name("set_subscript"),[listName, Const(i), n]), newast, gen, map, strings)
	return listName

def flatDict(ast, newast, gen, map, strings):
	dictName = flatten(InjectFrom("big",CallRuntime(Name("create_dict"),[Const(len(ast.items))])), newast, gen, map, strings)
	for k, v in ast.items:
		#Ensure value is calculated before key
		vName = flatten(v, newast, gen, map, strings)
		flatten(CallRuntime(Name("set_subscript"),[dictName, k, vName]), newast, gen, map, strings)
	return dictName

def flatSubscript(ast, newast, gen, map, strings):
	#flags doesn't neccesarily exist
	if ast.flags and ast.flags[0] == "OP_ASSIGN":
		#TODO take out this hack and refactor flatten
		return Subscript(flatten(ast.expr, newast, gen, map, strings), ast.flags, [flatten(ast.subs[0], newast, gen, map, strings)])
	else:
		return flatten(CallRuntime(Name("get_subscript"),[ast.expr, ast.subs[0]]), newast, gen, map, strings)

def flatIfExp(ast, newast, gen, map, strings):
	#Will not be fully flattened in order to preserve correctness
	#Unifies returns to a single variable
	thenNewast = Stmt([])
	elseNewast = Stmt([])
	thenRet = flatten(ast.then, thenNewast, gen, map, strings) or Const(-1)
	elseRet = flatten(ast.else_, elseNewast, gen, map, strings) or Const(-1)
	retVar = Name(gen.inc().name())
	addAssign(thenRet, thenNewast, gen, map, strings, retVar.name)
	addAssign(elseRet, elseNewast, gen, map, strings, retVar.name)
	cond = flatten(ast.test, newast, gen, map, strings)
	if isinstance(cond, Const):
		cond = addAssign(cond, newast, gen, map, strings)
	
	newast.nodes.append(IfStmt(
		cond,
		thenNewast,
		elseNewast,
		retVar,
		set(),
		set()
	))
	return retVar

#Have to break the contract here
def flatLambda(ast, newast, gen, map, strings):
	#Keep the flattens inside the body; we don't want to add flattened statements outside of the function
	flat_body = Stmt([])
	flatten(ast.code, flat_body, gen, map, strings)
	return Lambda(ast.argnames, ast.defaults, ast.flags, flat_body)

def flatReturn(ast, newast, gen, map, strings):
	name = flatten(ast.value, newast, gen, map, strings)
	newast.nodes.append(Return(name))
	return name

def flatWhile(ast, newast, gen, map, strings):
	#Will not be fully flattened in order to preserve correctness
	testAssign = Stmt([])
	test = flatten(ast.test, testAssign, gen, map, strings)
	bodyAssign = Stmt([])
	flatten(ast.body, bodyAssign, gen, map, strings)
	newast.nodes.append(ModWhile(test, testAssign, bodyAssign, set(), set()))
	return None

#Break contract here
def flatAssAttr(ast, newast, gen, map, strings):
	return AssAttr(flatten(ast.expr, newast, gen, map, strings), ast.attrname, ast.flags)

def flatGetattr(ast, newast, gen, map, strings):
	simple = flatten(ast.expr, newast, gen, map, strings)
	return addAssign(CallRuntime(Name("get_attr"),[simple, Const(ast.attrname)]), newast, gen, map, strings)

def flatGetTag(ast, newast, gen, map, strings):
	simple = flatten(ast.arg, newast, gen, map, strings)
	return addAssign(CallRuntime(Name("tag"),[simple]), newast, gen, map, strings)

def flatInjectFrom(ast, newast, gen, map, strings):
	simple = flatten(ast.arg, newast, gen, map, strings)
	temp = addAssign(CallRuntime(Name("inject_"+ast.typ),[simple]), newast, gen, map, strings)
	return temp

def flatProjectTo(ast, newast, gen, map, strings):
	simple = flatten(ast.arg, newast, gen, map, strings)
	return addAssign(CallRuntime(Name("project_"+ast.typ),[simple]), newast, gen, map, strings)

def flatLet(ast, newast, gen, map, strings):
	rhs = flatten(ast.rhs, newast, gen, map, strings)
	var = flatten(ast.var, newast, gen, map, strings)
	addAssign(rhs, newast, gen, map, strings, var.name)
	return flatten(ast.body, newast, gen, map, strings)

def flatIsType(ast, newast, gen, map, strings):
	simple = flatten(ast.arg, newast, gen, map, strings)
	return addAssign(CallRuntime(Name("is_"+ast.typ),[simple]), newast, gen, map, strings)

def flatThrowError(ast, newast, gen, map, strings):
	return addAssign(CallRuntime(Name("error_pyobj"),[ast.msg]), newast, gen, map, strings)

def flatten(ast, newast, gen, map, strings):
	return {
		Stmt:        flatStmt,
		Printnl:     flatPrintnl,
		Const:       flatConst,
		UnarySub:    flatUnarySub,
		Add:         flatAdd,
		Discard:     flatDiscard,
		AssName:     flatAssName,
		Assign:      flatAssign,
		Name:        flatName,
		CallFunc:    flatCallFunc,
		CallRuntime: flatCallRuntime,
		Compare:     flatCompare,
		Or:          flatOr,
		And:         flatAnd,
		Bitxor:      flatBitxor,
		Not:         flatNot,
		List:        flatList,
		Dict:        flatDict,
		Subscript:   flatSubscript,
		IfExp:       flatIfExp,
		Lambda:      flatLambda,
		Return:      flatReturn,
		While:       flatWhile,
		#AssAttr:     flatAssAttr,
		#Getattr:     flatGetattr,
		GetTag:      flatGetTag,
		InjectFrom:  flatInjectFrom,
		ProjectTo:   flatProjectTo,
		Let:         flatLet,
		IsType:      flatIsType,
		ThrowError:  flatThrowError
	}[ast.__class__](ast, newast, gen, map, strings)

#Returns a list of tuples: (lambda name, new ast for the lambda)
def runFlatten(ast, gen, map, strings):
	l = []
	for n, a in ast:
		newast = flatten(a, None, gen, map, strings)
		l.append((n, newast))
	return l
