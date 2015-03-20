import compiler
from compiler.ast import *
from HelperClasses import *

debug = False

def addAssign(node, newast, gen, map, name = None):
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

def flatModule(ast, newast, gen, map):
	return flatten(ast.node, newast, gen, map)

def flatStmt(ast, newast, gen, map):
	newast = Stmt([])
	for node in ast.nodes:
		flatten(node, newast, gen, map)
	return newast

def flatPrintnl(ast, newast, gen, map):
	simple = flatten(ast.nodes[0], newast, gen, map)
	return newast.nodes.append(CallFunc(Name("print_any"),[simple]))

def flatConst(ast, newast, gen, map):
	#Do not inject if its a str constant (for throwing errors)
	if isinstance(ast.value, str):
		return ast
	else:
		return addAssign(CallFunc(Name("inject_int"),[ast]), newast, gen, map)

def flatName(ast, newast, gen, map):
	return ast

def flatUnarySub(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	if isinstance(simple, Const):
		return Const(-simple.value)
	return addAssign(UnarySub(simple), newast, gen, map)

def flatAdd(ast, newast, gen, map):
	s1 = flatten(ast.left, newast, gen, map)
	s2 = flatten(ast.right, newast, gen, map)
	return addAssign(Add((s1, s2)), newast, gen, map)

def flatDiscard(ast, newast, gen, map):
	return flatten(ast.expr, newast, gen, map)

def flatAssName(ast, newast, gen, map):
	return ast.name

def flatAssign(ast, newast, gen, map):
	#TODO remove this hack
	rhs = flatten(ast.expr, newast, gen, map)
	lhs = flatten(ast.nodes[0], newast, gen, map)
	if isinstance(lhs, Subscript):
		return flatten(CallFunc(Name("set_subscript"),[lhs.expr, lhs.subs[0], rhs]), newast, gen, map)
	else:
		return addAssign(rhs, newast, gen, map, lhs)

def flatCallFunc(ast, newast, gen, map):
	return addAssign(CallFunc(
		Name("input_int") if ast.node.name == "input" else ast.node,
		[flatten(n, newast, gen, map) for n in ast.args]
	),newast, gen, map)

def flatCompare(ast, newast, gen, map):
	s1 = flatten(ast.expr, newast, gen, map)
	s2 = flatten(ast.ops[0][1], newast, gen, map)
	return addAssign(Compare(s1,[(ast.ops[0][0], s2)]), newast, gen, map)

def flatOr(ast, newast, gen, map):
	'''Warning, does not implement short-circuiting.
	Only code generated in the explicate pass should reach here which 
	does not rely on short-circuiting.
	This Node performs the bitwise Or operation.'''
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(Or([prev, new]), newast, gen, map)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map)
		s2 = flatten(ast.nodes[1], newast, gen, map)
		return addAssign(Or([s1, s2]), newast, gen, map)

def flatAnd(ast, newast, gen, map):
	'''Warning, does not implement short-circuiting.
	Only code generated in the explicate pass should reach here which 
	does not rely on short-circuiting.
	This Node performs the bitwise And operation.'''
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(And([prev, new]), newast, gen, map)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map)
		s2 = flatten(ast.nodes[1], newast, gen, map)
		return addAssign(And([s1, s2]), newast, gen, map)

def flatBitxor(ast, newast, gen, map):
	if len(ast.nodes) > 2:
		prev = flatten(ast.nodes[0])
		for i in range(1,len(ast.nodes)):
			new = flatten(ast.nodes[i])
			prev = addAssign(Bitxor([prev, new]), newast, gen, map)
		return prev
	else:
		s1 = flatten(ast.nodes[0], newast, gen, map)
		s2 = flatten(ast.nodes[1], newast, gen, map)
		return addAssign(Bitxor([s1, s2]), newast, gen, map)

def flatNot(ast, newast, gen, map):
	#TODO fix this hack
	return flatten(InjectFrom("bool", Bitxor([CallFunc(Name("is_true"),[flatten(ast.expr, newast, gen, map)]), ProjectTo("int",Const(1))])), newast, gen, map)

def flatList(ast, newast, gen, map):
	listName = flatten(InjectFrom("big",CallFunc(Name("create_list"),[Const(len(ast.nodes))])), newast, gen, map)
	for i,n in enumerate(ast.nodes):
		flatten(CallFunc(Name("set_subscript"),[listName, Const(i), n]), newast, gen, map)
	return listName

def flatDict(ast, newast, gen, map):
	dictName = flatten(InjectFrom("big",CallFunc(Name("create_dict"),[Const(len(ast.items))])), newast, gen, map)
	for k, v in ast.items:
		#Ensure value is calculated before key
		vName = flatten(v, newast, gen, map)
		flatten(CallFunc(Name("set_subscript"),[dictName, k, vName]), newast, gen, map)
	return dictName

def flatSubscript(ast, newast, gen, map):
	if ast.flags == "OP_ASSIGN":
		#TODO take out this hack and refactor flatten
		return Subscript(flatten(ast.expr, newast, gen, map), ast.flags, [flatten(ast.subs[0], newast, gen, map)])
	else:
		return flatten(CallFunc(Name("get_subscript"),[ast.expr, ast.subs[0]]), newast, gen, map)

def flatIfExp(ast, newast, gen, map):
	#Will not be fully flattened in order to preserve correctness
	#Unifies returns to a single variable
	thenNewast = Stmt([])
	elseNewast = Stmt([])
	thenRet = flatten(ast.then, thenNewast, gen, map)
	elseRet = flatten(ast.else_, elseNewast, gen, map)
	retVar = Name(gen.inc().name())
	addAssign(thenRet, thenNewast, gen, map, retVar.name)
	addAssign(elseRet, elseNewast, gen, map, retVar.name)
	cond = flatten(ast.test, newast, gen, map)
	if isinstance(cond, Const):
		cond = addAssign(cond, newast, gen, map)
	
	newast.nodes.append(IfStmt(
		cond,
		thenNewast,
		elseNewast,
		retVar,
		Set([]),
		Set([])
	))
	return retVar

def flatLambda(ast, newast, gen, map):
	#Shouldn't reach here
	raise NotImplementedError 

def flatModLambda(ast, newast, gen, map):
	#Keep the flattens inside the body; we don't want to add flattened statements outside of the function
	flat_body = Stmt([])
	flat_body += flatten(ast.body, flat_body, gen, map)
	return ModLambda(ast.params, ast.paramAllocs, ast.paramInits, ast.localInits, flat_body)

#Have to break the contract here
def flatReturn(ast, newast, gen, map):
	return Return(flatten(ast.value, newast, gen, map))

def flatGetTag(ast, newast, gen, map):
	simple = flatten(ast.arg, newast, gen, map)
	return addAssign(CallFunc(Name("tag"),[simple]), newast, gen, map)

def flatInjectFrom(ast, newast, gen, map):
	simple = flatten(ast.arg, newast, gen, map)
	temp = addAssign(CallFunc(Name("inject_"+ast.typ),[simple]), newast, gen, map)
	return temp

def flatProjectTo(ast, newast, gen, map):
	simple = flatten(ast.arg, newast, gen, map)
	return addAssign(CallFunc(Name("project_"+ast.typ),[simple]), newast, gen, map)

def flatLet(ast, newast, gen, map):
	rhs = flatten(ast.rhs, newast, gen, map)
	var = flatten(ast.var, newast, gen, map)
	addAssign(rhs, newast, gen, map, var.name)
	return flatten(ast.body, newast, gen, map)

def flatIsType(ast, newast, gen, map):
	simple = flatten(ast.arg, newast, gen, map)
	return addAssign(CallFunc(Name("is_"+ast.typ),[simple]), newast, gen, map)

def flatThrowError(ast, newast, gen, map):
	simple = flatten(ast.msg, newast, gen, map)
	return addAssign(CallFunc(Name("error_pyobj"),[simple]), newast, gen, map)

def flatten(ast, newast, gen, map):
	return {
		Module:     flatModule,
		Stmt:       flatStmt,
		Printnl:    flatPrintnl,
		Const:      flatConst,
		UnarySub:   flatUnarySub,
		Add:        flatAdd,
		Discard:    flatDiscard,
		AssName:    flatAssName,
		Assign:     flatAssign,
		Name:       flatName,
		CallFunc:   flatCallFunc,
		Compare:    flatCompare,
		Or:         flatOr,
		And:        flatAnd,
		Bitxor:     flatBitxor,
		Not:        flatNot,
		List:       flatList,
		Dict:       flatDict,
		Subscript:  flatSubscript,
		IfExp:      flatIfExp,
		Lambda:     flatLambda,
		ModLambda:  flatModLambda,
		Return:     flatReturn,
		GetTag:     flatGetTag,
		InjectFrom: flatInjectFrom,
		ProjectTo:  flatProjectTo,
		Let:        flatLet,
		IsType:     flatIsType,
		ThrowError: flatThrowError
	}[ast.__class__](ast, newast, gen, map)
