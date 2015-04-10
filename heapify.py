from compiler.ast import *
from HelperClasses import *
from compiler.ast import *
import varAnalysis, astpp

def glModule(ast, scope):
	return getLambdas(ast.node)

def glStmt(ast, scope):
	return reduce(lambda acc, n : acc + getLambdas(n, scope), ast.nodes, [])

def glPrintnl(ast, scope):
	return getLambdas(ast.nodes[0], scope)

def glConst(ast, scope):
	return []

def glUnarySub(ast, scope):
	return getLambdas(ast.expr, scope)

def glAdd(ast, scope):
	return getLambdas(ast.left, scope) + getLambdas(ast.right, scope)

def glDiscard(ast, scope):
	return getLambdas(ast.expr, scope)

def glAssign(ast, scope):
	return getLambdas(ast.expr, scope)

def glName(ast, scope):
	return [] 

def glAssName(ast, scope):
	return []

def glCallFunc(ast, scope):
	return getLambdas(ast.node, scope)

def glCallFunc(ast, scope):
	return reduce(lambda acc, n : acc + getLambdas(n, scope), ast.args, [])

def glCompare(ast, scope):
	return getLambdas(ast.expr, scope) + getLambdas(ast.ops[0][1], scope)

def glOr(ast, scope):
	return getLambdas(ast.nodes[0], scope) + getLambdas(ast.nodes[1], scope)

def glAnd(ast, scope):
	return getLambdas(ast.nodes[0], scope) + getLambdas(ast.nodes[1], scope)

def glNot(ast, scope):
	return getLambdas(ast.expr, scope)

def glList(ast, scope):
	return reduce(lambda acc, n : acc + getLambdas(n, scope), ast.nodes, [])

def glDict(ast, scope):
	#Functions can't be a key. Only check the values.
	return reduce(lambda acc, n : acc + getLambdas(n[1], scope), ast.items, [])

def glSubscript(ast, scope):
	return getLambdas(ast.expr, scope) + getLambdas(ast.subs[0], scope)

def glIfExp(ast, scope):
	test_gl = getLambdas(ast.test, scope)
	then_gl = getLambdas(ast.then, scope)
	else__gl = getLambdas(ast.else_, scope)
	return test_gl + then_gl + else__gl

def glLambda(ast, scope):
	return [(ast, scope + 1)] + getLambdas(ast.code, scope + 1)

def glReturn(ast, scope):
	return getLambdas(ast.value, scope)

def glGetTag(ast, scope):
	return getLambdas(ast.arg, scope)

def glInjectFrom(ast, scope):
	return getLambdas(ast.arg, scope)

def glProjectTo(ast, scope):
	return getLambdas(ast.arg, scope)

def glLet(ast, scope):
	return getLambdas(ast.rhs, scope) + getLambdas(ast.body, scope)

def glIsType(ast, scope):
	return getLambdas(ast.arg, scope)

def glThrowError(ast, scope):
	return []
	
#Finds all lambda's in the tree, returns a list of tuples: (lambda, scope level)
def getLambdas(ast, scope):
	glPass = lambda a, s: []
	return {
		Module:    glModule,
		Stmt:      glStmt,
		Printnl:   glPrintnl,
		Const:     glConst,
		UnarySub:  glUnarySub,
		Add:       glAdd,
		Discard:   glDiscard,
		Assign:    glAssign,
		Name:      glName,
		AssName:   glAssName,
		CallFunc:  glCallFunc,
		Compare:   glCompare,
		Or:        glOr,
		And:       glAnd,
		Not:       glNot,
		List:      glList,
		Dict:      glDict,
		Subscript: glSubscript,
		IfExp:     glIfExp,
		Lambda:    glLambda,
		Return:    glReturn,
		GetTag:     glGetTag,
		InjectFrom: glInjectFrom,
		ProjectTo:  glProjectTo,
		Let:        glLet,
		IsType:     glIsType,
		ThrowError: glThrowError
	}.get(ast.__class__, glPass)(ast, scope)


def heapifyModule(ast, names):
	#go through the top level scope and add the variables to the dictionary
	ast.node = heapify(ast.node, names)

def heapifyStmt(ast, names):
	return Stmt([heapify(n, names) for n in ast.nodes])

def heapifyPrintnl(ast, names):
	return Printnl([heapify(ast.nodes[0], names)], None)

def heapifyConst(ast, names):
	return ast

def heapifyUnarySub(ast, names):
	return UnarySub(heapify(ast.expr, names))

def heapifyAdd(ast, names):
	return Add([heapify(ast.left, names), heapify(ast.right, names)])

def heapifyDiscard(ast, names):
	return Discard(heapify(ast.expr, names))

def heapifyAssign(ast, names):
	lhs = ast.nodes[0]
	if isinstance(lhs, AssName):
		if lhs.name in names:
			return Assign([Subscript(Name(lhs.name), "OP_ASSIGN", [Const(0)])], heapify(ast.expr, names))
		else:
			return Assign([lhs], heapify(ast.expr, names))
	elif isinstance(lhs, AssAttr):
		return Assign([heapify(lhs, names)], heapify(ast.expr, names))
	else:
		return Assign([Subscript(heapify(lhs.expr, names), lhs.flags, [heapify(lhs.subs[0], names)])], heapify(ast.expr, names))

def heapifyName(ast, names):
	if ast.name in names:
		return Subscript(ast, "OP_APPLY" ,[Const(0)])
	else:
		return ast

def heapifyAssName(ast, names):
	return ast

def heapifyCallFunc(ast, names):
	return CallFunc(heapify(ast.node, names), [heapify(arg, names) for arg in ast.args])

def heapifyCallRuntime(ast, names):
	return CallRuntime(ast.node, [heapify(arg, names) for arg in ast.args])

def heapifyCompare(ast, names):
	return Compare(heapify(ast.expr, names), [(ast.ops[0][0], heapify(ast.ops[0][1], names))])

def heapifyOr(ast, names):
	return Or([heapify(ast.nodes[0], names),heapify(ast.nodes[1], names)])

def heapifyAnd(ast, names):
	return And([heapify(ast.nodes[0], names),heapify(ast.nodes[1], names)])

def heapifyNot(ast, names):
	return Not(heapify(ast.expr, names))

def heapifyList(ast, names):
	return List([heapify(n, names) for n in ast.nodes])

def heapifyDict(ast, names):
	return Dict([(heapify(k, names), heapify(v, names)) for (k, v) in ast.items])

def heapifySubscript(ast, names):
	return Subscript(heapify(ast.expr, names), None, [heapify(sub, names) for sub in ast.subs])

def heapifyIfExp(ast, names):
	return IfExp(
		heapify(ast.test, names),
		heapify(ast.then, names),
		heapify(ast.else_, names)
	)

def heapifyLambda(ast, names):
	if not isinstance(ast.code, Stmt):
		ast.code = Stmt([Return(ast.code)])
	heapParams = [p in names for p in ast.argnames]
	pPrime = [p+"_heap" if heapParams[i] else p for i, p in enumerate(ast.argnames)]
	w, r = varAnalysis.getVars(ast.code)
	l_h = w & names
	p_h = [p for p in ast.argnames]
	paramAllocs = [Assign([AssName(p, 'OP_ASSIGN')], List([Const(1)])) for p in p_h if p in names]
	paramInits = [Assign([Subscript(Name(p), 'OP_ASSIGN', [Const(0)])], Name(pPrime[i])) for i, p in enumerate(p_h) if p in names]
	localInits = [Assign([AssName(p, 'OP_ASSIGN')], List([Const(1)])) for p in l_h]
	funcCode = heapify(ast.code, names)
	
	#Combine the code together
	funcCode.nodes = paramAllocs + paramInits + localInits + funcCode.nodes
	return Lambda(pPrime, ast.defaults, ast.flags, funcCode)

def heapifyReturn(ast, names):
	return Return(heapify(ast.value, names))

def heapifyWhile(ast, names):
	return While(heapify(ast.test, names), heapify(ast.body, names), None)

def heapifyAssAttr(ast, names):
	return AssAttr(heapify(ast.expr, names), ast.attrname, ast.flags)

def heapifyGetattr(ast, names):
	return Getattr(heapify(ast.expr, names), ast.attrname)

def heapifyGetTag(ast, names):
	return GetTag(heapify(ast.arg))

def heapifyInjectFrom(ast, names):
	return InjectFrom(ast.typ, heapify(ast.arg, names))

def heapifyProjectTo(ast, names):
	return ProjectTo(ast.typ, heapify(ast.arg, names))

#Iffy about this one. Does Let handle subscripts?
def heapifyLet(ast, names):
	return Let(heapify(ast.var, names), heapify(ast.rhs, names), heapify(ast.body, names))

def heapifyIsType(ast, names):
	return IsType(ast.typ, heapify(ast.arg, names))

def heapifyThrowError(ast, names):
	return ast

def heapify(ast, names):
	return {
		Module:       heapifyModule,
		Stmt:         heapifyStmt,
		Printnl:      heapifyPrintnl,
		Const:        heapifyConst,
		UnarySub:     heapifyUnarySub,
		Add:          heapifyAdd,
		Discard:      heapifyDiscard,
		Assign:       heapifyAssign,
		Name:         heapifyName,
		AssName:      heapifyAssName,
		CallFunc:     heapifyCallFunc,
		CallRuntime:  heapifyCallRuntime,
		Compare:      heapifyCompare,
		Or:           heapifyOr,
		And:          heapifyAnd,
		Not:          heapifyNot,
		List:         heapifyList,
		Dict:         heapifyDict,
		Subscript:    heapifySubscript,
		IfExp:        heapifyIfExp,
		Lambda:       heapifyLambda,
		Return:       heapifyReturn,
		While:        heapifyWhile,
		#AssAttr:      heapifyAssAttr,
		#Getattr:      heapifyGetattr,
		GetTag:       heapifyGetTag,
		InjectFrom:   heapifyInjectFrom,
		ProjectTo:    heapifyProjectTo,
		Let:          heapifyLet,
		IsType:       heapifyIsType,
		ThrowError:   heapifyThrowError
	}[ast.__class__](ast, names)

#find all lambda's, and recurse repeatedly on them
def runHeapify(ast):
	#If a variable is used in a scope that is not its origin, add to set of variables
	#We calculate this by seeing if a read or write variable's scope does not match 
	#the scope that this read or write occurred, add to set
	
	#A set of variable names that need to be heapified
	heapVars = set()
	
	lambdas = getLambdas(ast.node, 0)
	for n, s in lambdas:
		s = str(s)
		write, read = varAnalysis.getVars(n.code)
		for var in read - write - set(n.argnames):
			heapVars.add(var)
	
	#Now that we have a set of vars that need to be heapified, recurse through the tree
	heapVars -= set(["True", "False"])
	heapify(ast, heapVars)
	
	#Now initalize all heapVars at the start of the program
	#i.e prepend h_1 = [0], h_2 = [0] etc. to our outermost stmt node
	for var_name in heapVars:
		ast.node.nodes = [Assign([AssName(var_name, 'OP_ASSIGN')], List([Const(0)]))] + ast.node.nodes
	return ast
