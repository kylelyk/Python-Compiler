from compiler.ast import *
from HelperClasses import *
from compiler.ast import *
import varAnalysis, astpp

#Combines the func list and ast into a list of tuples (funcname, ModLambda)
#all code not in a lambda will be put into main
def standardize(ast, l):
	ast.nodes.append(Return(Const(0)))
	return l + [("main", Lambda([], [], 0, ast))]

#Helper to recursive call closure on each elm
#and to reduce the list of tuples into one large tuple
def iterList(list, gen, lambdaGen):
	listTup = [closure(n, gen, lambdaGen) for n in list]
	return reduce(lambda (acc_a, acc_l), (a, l) : (acc_a + [a], acc_l + l), listTup, ([],[]))

def closureModule(ast, gen, lambdaGen):
	ast, l = closure(ast.node, gen, lambdaGen)
	return standardize(ast, l)

def closureStmt(ast, gen, lambdaGen):
	a, l = iterList(ast.nodes, gen, lambdaGen)
	return Stmt(a), l

def closurePrintnl(ast, gen, lambdaGen):
	ast, l = closure(ast.nodes[0], gen, lambdaGen)
	return Printnl([ast], None), l

def closureConst(ast, gen, lambdaGen):
	return ast, []

def closureUnarySub(ast, gen, lambdaGen):
	ast, l = closure(ast.expr, gen, lambdaGen)
	return UnarySub(ast), l

def closureAdd(ast, gen, lambdaGen):
	ast_left, l_left = closure(ast.left, gen, lambdaGen)
	ast_right, l_right = closure(ast.right, gen, lambdaGen)
	return Add([ast_left, ast_right]), l_left + l_right

def closureDiscard(ast, gen, lambdaGen):
	ast, l = closure(ast.expr, gen, lambdaGen)
	return Discard(ast), l

def closureAssign(ast, gen, lambdaGen):
	astN, l = closure(ast.expr, gen, lambdaGen)
	return Assign([ast.nodes[0]], astN), l

def closureName(ast, gen, lambdaGen):
	return ast, []

def closureAssName(ast, gen, lambdaGen):
	return ast, []

def closureCallFunc(ast, gen, lambdaGen):
	#Make input() a call to runtime
	if isinstance(ast.node, Name) and ast.node.name == "input":
		ast.node.name = "input_int"
		return closureCallRuntime(ast, gen, lambdaGen)
	cl = Name(gen.inc().name())
	funcRef, l1 = closure(ast.node, gen, lambdaGen)
	a, l2 = iterList(ast.args, gen, lambdaGen)
	args = [CallRuntime(Name("get_free_vars"), [cl])] + a
	return Let(cl, funcRef,
		CallFunc(CallRuntime(Name("get_fun_ptr"), [cl]), args)), l1 + l2

def closureCallRuntime(ast, gen, lambdaGen):
	a, l = iterList(ast.args, gen, lambdaGen)
	return CallRuntime(ast.node, a), l

def closureCompare(ast, gen, lambdaGen):
	ast_left, l_left = closure(ast.expr, gen, lambdaGen)
	ast_right, l_right = closure(ast.ops[0][1], gen, lambdaGen)
	return Compare(ast_left, [(ast.ops[0][0], ast_right)]), l_left + l_right

def closureOr(ast, gen, lambdaGen):
	ast_left, l_left = closure(ast.nodes[0], gen, lambdaGen)
	ast_right, l_right = closure(ast.nodes[1], gen, lambdaGen)
	return Or([ast_left,ast_right]), l_left + l_right

def closureAnd(ast, gen, lambdaGen):
	ast_left, l_left = closure(ast.nodes[0], gen, lambdaGen)
	ast_right, l_right = closure(ast.nodes[1], gen, lambdaGen)
	return And([ast_left,ast_right]), l_left + l_right

def closureNot(ast, gen, lambdaGen):
	ast, l = closure(ast.expr, gen, lambdaGen)
	return Not(ast), l

def closureList(ast, gen, lambdaGen):
	a, l = iterList(ast.nodes, gen, lambdaGen)
	return List(a), l

def closureDict(ast, gen, lambdaGen):
	l = []
	new_items = []
	for (k, v) in ast.items:
		ast_v, l_v = closure(v, gen, lambdaGen)
		l = l + l_v
		new_items = new_items + [(k, ast_v)]
	return Dict(new_items), l

def closureSubscript(ast, gen, lambdaGen):
	astN, l = closure(ast.expr, gen, lambdaGen)
	return Subscript(astN, ast.flags, ast.subs), l

def closureIfExp(ast, gen, lambdaGen):
	ast_test, l_test = closure(ast.test, gen, lambdaGen)
	ast_then, l_then = closure(ast.then, gen, lambdaGen)
	ast_else_, l_else_ = closure(ast.else_, gen, lambdaGen)
	
	return IfExp(ast_test, ast_then, ast_else_), l_test+l_then+l_else_

def closureLambda(ast, gen, lambdaGen):
	#First recurse into the body
	new_body, l_body = closure(ast.code, gen, lambdaGen)
	lambdaName = lambdaGen.inc().name()
	
	write, read = varAnalysis.getVars(new_body)
	free_vars = list((read - write) - set(ast.argnames))
	free_vars_param = '$free_vars_' + lambdaName
	#Add the free_var assignments to the start of the body
	#i.e x = free_vars_X[0]; y = free_vars_X[1]
	for i, var in enumerate(free_vars):
		n_assign = Assign([AssName(var, 'OP_ASSIGN')], Subscript(Name(free_vars_param), 'OP_APPLY', [Const(i)]))
		new_body.nodes = [n_assign] + new_body.nodes
	
	#Create the function definition for the top level scope
	newParams = [free_vars_param] + ast.argnames
	funcDef = Lambda(newParams, ast.defaults, ast.flags, new_body)
	#Create the local, closure convention'd reference to the function
	closedLambda = InjectFrom("big", CallRuntime(Name('create_closure'),[Const(lambdaName), List([Name(fvar) for fvar in free_vars])]))
	return closedLambda, l_body + [(lambdaName, funcDef)]

def closureReturn(ast, gen, lambdaGen):
	ast, l = closure(ast.value, gen, lambdaGen)
	return Return(ast), l

def closureGetTag(ast, gen, lambdaGen):
	ast, l = closure(ast.arg, gen, lambdaGen)
	return GetTag(ast), l

def closureInjectFrom(ast, gen, lambdaGen):
	astN, l = closure(ast.arg, gen, lambdaGen)
	return InjectFrom(ast.typ, astN), l

def closureProjectTo(ast, gen, lambdaGen):
	astN, l = closure(ast.arg, gen, lambdaGen)
	return ProjectTo(ast.typ, astN), l

def closureLet(ast, gen, lambdaGen):
	ast_rhs, l_rhs = closure(ast.rhs, gen, lambdaGen)
	ast_body, l_body = closure(ast.body, gen, lambdaGen)
	return Let(ast.var, ast_rhs, ast_body), l_rhs+l_body

def closureIsType(ast, gen, lambdaGen):
	astN, l = closure(ast.arg, gen, lambdaGen)
	return IsType(ast.typ, astN), l

def closureThrowError(ast, gen, lambdaGen):
	return ast, []

#The function list is given as a tuple of (FuncName, Lambda)
#Where FuncName is the name that the Lambda is assigned to
def closure(ast, gen, lambdaGen):
	return {
		Module:      closureModule,
		Stmt:        closureStmt,
		Printnl:     closurePrintnl,
		Const:       closureConst,
		UnarySub:    closureUnarySub,
		Add:         closureAdd,
		Discard:     closureDiscard,
		Assign:      closureAssign,
		Name:        closureName,
		AssName:     closureAssName,
		CallFunc:    closureCallFunc,
		CallRuntime: closureCallRuntime,
		Compare:     closureCompare,
		Or:          closureOr,
		And:         closureAnd,
		Not:         closureNot,
		List:        closureList,
		Dict:        closureDict,
		Subscript:   closureSubscript,
		IfExp:       closureIfExp,
		Lambda:      closureLambda,
		Return:      closureReturn,
		GetTag:      closureGetTag,
		InjectFrom:  closureInjectFrom,
		ProjectTo:   closureProjectTo,
		Let:         closureLet,
		IsType:      closureIsType,
		ThrowError:  closureThrowError
	}[ast.__class__](ast, gen, lambdaGen)
	
