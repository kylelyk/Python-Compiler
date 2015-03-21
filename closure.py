from compiler.ast import *
from HelperClasses import *
from compiler.ast import *
import varAnalysis, astpp

def addNewVars(ast, l):
	#go through the top level scope and add the variables to the dictionary
	for (funcName, funcDef) in l:
		assign_f = Assign([AssName(funcName, 'OP_ASSIGN')], funcDef)
		ast.node.nodes = [assign_f] + ast.node.nodes
	return ast

def closureModule(ast):
	ast, l = closure(ast.node)
	ast = addNewVars(ast, l)
	return ast

def closureStmt(ast):
	listtTup = [closure(n) for n in ast.nodes]
	a, l = reduce(lambda (acc_a, acc_l), (a, l) : acc_a + [a], acc_l + [l], listTup, ([],[]))
	return Stmt(a), l

def closurePrintnl(ast):
	ast, l = closure(ast.nodes[0])
	return Printnl([ast], None), l

def closureConst(ast):
	return ast, []

def closureUnarySub(ast):
	ast, l = closure(ast.expr)
	return UnarySub(ast), l

def closureAdd(ast):
	ast_left, l_left = closure(ast.left)
	ast_right, l_right = closure(ast.right)
	return Add([ast_left, ast_right]), l_left + l_right

def closureDiscard(ast):
	ast, l = closure(ast.expr)
	return Discard(ast), l

def closureAssign(ast):
	astN, l = closure(ast.expr)
	return Assign([ast.nodes[0]], astN), l

def closureName(ast):
	return ast,[]

def closureAssName(ast):
	return ast, []

def closureCallFunc(ast):
	raise NotImplementedError
	#return CallFunc(closure(ast.node), [closure(arg) for arg in ast.args])

def closureCompare(ast):
	ast_left, l_left = closure(ast.expr)
	ast_right, l_right = closure(ast.ops[0][1])
	return Compare(ast_left, [(ast.ops[0][0], ast_right)]), l_left + l_right

def closureOr(ast):
	ast_left, l_left = closure(ast.nodes[0])
	ast_right, l_right = closure(ast.nodes[1])
	return Or([ast_left,ast_right]), l_left + l_right

def closureAnd(ast):
	ast_left, l_left = closure(ast.nodes[0])
	ast_right, l_right = closure(ast.nodes[1])
	return And([ast_left,ast_right]), l_left + l_right

def closureNot(ast):
	ast, l = closure(ast.expr)
	return Not(ast), l

def closureList(ast):
	listTup = [closure(n) for n in ast.nodes]
	a, l = reduce(lambda (acc_a, acc_l), (a, l) : acc_a + [a], acc_l + [l], listTup, ([],[]))
	return List(a), l

def closureDict(ast):
	l = []
	new_items = []
	for (k, v) in ast.items:
		ast_v, l_v = closure(v)
		l = l + l_v
		new_items = new_items + [(k, ast_v)]
	return Dict(new_items), l

def closureSubscript(ast):
	astN, l = closure(ast.expr)
	return Subscript(astN, ast.flags, ast.subs), l

def closureIfExp(ast):
	ast_test, l_test = closure(ast.test)
	ast_then, l_then = closure(ast.then)
	ast_else_, l_else_ = closure(ast.else_)
	
	return IfExp(ast_test, ast_then, ast_else_), l_test+l_then+l_else_

def closureModLambda(ast):
	#First recurse into the body
	new_body, l_body = closure(ast.body)
	
	#TODO Actually generate a unique free_vars name (generate X)
	gen_int = X = str(0)
	
	written_to, read_from = varAnalysis.getvars(ast.body)
	free_vars = list((read_from - written_to) - set(ast.params))
	free_vars_param = 'free_vars_' + gen_int
	
	#Add the free_var assignments to the start of the body
	#i.e x = free_vars_X[0]; y = free_vars_X[1]
	i = 0
	for var in free_vars:
		n_assign = Assign([var], Subscript(Name(free_vars_param), 'OP_APPLY', [Const(i)]))
		newBody = Stmt(n_assign + new_body.nodes)
		i = i + 1
	
	#Create the function definition for the top level scope
	#NOTE: I believe we add the name of the free_vars list here,
	#not the actual list itself. Correct if wrong.
	newParams = [free_vars_param] + ast.params
	funcDef = ModLambda(newParams, ast.paramAllocs, ast.paramInit, ast.localInits, newBody)
	
	#Create the local, closure convention'd reference to the function
	funcName = "lambda_" + gen_int
	closedLambda = CallFunc(Name('create_closure'),[funcName, free_vars])
	return closedLambda, l_body + [(funcName, funcDef)]
	
	
def closureReturn(ast):
	#print ast
	ast, l = closure(ast.value)
	return Return(ast), l

def closureGetTag(ast):
	ast, l = closure(ast.arg)
	return GetTag(ast), l

def closureInjectFrom(ast):
	astN, l = closure(ast.arg)
	return InjectFrom(ast.typ, astN), l

def closureProjectTo(ast):
	astN, l = closure(ast.arg)
	return ProjectTo(ast.typ, astN), l

def closureLet(ast):
	ast_rhs, l_rhs = closure(ast.rhs)
	ast_body, l_body = closure(ast.body)
	return Let(ast.var, ast_rhs, ast_body), l_rhs+l_body

def closureIsType(ast):
	astN, l = closure(ast.arg)
	return IsType(ast.typ, astN), l

def closureThrowError(ast):
	return ast

#The function list is given as a tuple of (FuncName, Lambda)
#Where FuncName is the name the Lambda is to be assigned to
def closure(ast):
	 #astpp.printAst(ast)
	return {
		Module:    closureModule,
		Stmt:      closureStmt,
		Printnl:   closurePrintnl,
		Const:     closureConst,
		UnarySub:  closureUnarySub,
		Add:       closureAdd,
		Discard:   closureDiscard,
		Assign:    closureAssign,
		Name:      closureName,
		AssName:   closureAssName,
		CallFunc:  closureCallFunc, #TODO
		Compare:   closureCompare,
		Or:        closureOr,
		And:       closureAnd,
		Not:       closureNot,
		List:      closureList,
		Dict:      closureDict,
		Subscript: closureSubscript,
		IfExp:     closureIfExp,
		ModLambda: closureModLambda,
		Return:    closureReturn,
		GetTag:     closureGetTag,
		InjectFrom: closureInjectFrom,
		ProjectTo:  closureProjectTo,
		Let:        closureLet,
		IsType:     closureIsType,
		ThrowError: closureThrowError
	}[ast.__class__](ast)
	
