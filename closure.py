from compiler.ast import *
from HelperClasses import *
from compiler.ast import *
import varAnalysis, astpp

#Combines the func list and ast into a list of tuples (funcname, ModLambda)
#all code not in a lambda will be put into main
def standardize(ast, l):
	#TODO check if correct
	#print ast.nodes
	ast.nodes.append(Return(Const(0)))
	return l + [("main", ModLambda([], [], [], [], ast))]
	
	
	#print "addNewVars:",ast
	#goes through the top level scope and add the variables to the dictionary
	for (funcName, funcDef) in l:
		#astpp.printAst(funcDef)
		assign_f = Assign([AssName(funcName, 'OP_ASSIGN')], funcDef)
		ast.nodes = [assign_f] + ast.nodes
	return ast

def iterList(list, gen, lambdaGen):
	listTup = [closure(n, gen, lambdaGen) for n in list]
	return reduce(lambda (acc_a, acc_l), (a, l) : (acc_a + [a], acc_l + l), listTup, ([],[]))

def closureModule(ast, gen, lambdaGen):
	ast, l = closure(ast.node, gen, lambdaGen)
	#print "\n\n",ast
	#print "\n\n", l
	#print standardize(ast, l)
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
	if ast.node.name == "input":
		ast.node.name = "input_int"
		#print "convert input into runtime call"
		return closureCallRuntime(ast, gen, lambdaGen)
	cl = Name(gen.inc().name())
	a, l = iterList(ast.args, gen, lambdaGen)
	args = [CallRuntime(Name("get_free_vars"), [cl])] + l
	return Let(cl, ast.node,
		CallFunc(CallRuntime(Name("get_fun_ptr"), [cl]), args)), l

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
	ast, l = closure(ast.expr, gen, gen, lambdaGen)
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

def closureModLambda(ast, gen, lambdaGen):
	#First recurse into the body
	new_body, l_body = closure(ast.body, gen, lambdaGen)
	
	lambdaName = lambdaGen.inc().name()
	
	written_to, read_from = varAnalysis.getVars(ast.body)
	free_vars = list((read_from - written_to) - set(ast.params))
	free_vars_param = 'free_vars_' + lambdaName
	
	#Add the free_var assignments to the start of the body
	#i.e x = free_vars_X[0]; y = free_vars_X[1]
	for i, var in enumerate(free_vars):
		n_assign = Assign([AssName(var, 'OP_ASSIGN')], Subscript(Name(free_vars_param), 'OP_APPLY', [Const(i)]))
		new_body.nodes = [n_assign] + new_body.nodes
	
	#Create the function definition for the top level scope
	newParams = [Name(free_vars_param)] + ast.params
	funcDef = ModLambda(newParams, ast.paramAllocs, ast.paramInits, ast.localInits, new_body)
	
	#Create the local, closure convention'd reference to the function
	closedLambda = CallRuntime(Name('create_closure'),[Const(lambdaName)] + [Name(fvar) for fvar in free_vars])
	return closedLambda, l_body + [(lambdaName, funcDef)]
	
	
def closureReturn(ast, gen, lambdaGen):
	#print ast
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
	 #astpp.printAst(ast)
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
		ModLambda:   closureModLambda,
		Return:      closureReturn,
		GetTag:      closureGetTag,
		InjectFrom:  closureInjectFrom,
		ProjectTo:   closureProjectTo,
		Let:         closureLet,
		IsType:      closureIsType,
		ThrowError:  closureThrowError
	}[ast.__class__](ast, gen, lambdaGen)
	
