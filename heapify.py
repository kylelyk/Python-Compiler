from compiler.ast import *
from compiler.visitor import *
import compiler
import varAnalysis

class ModLambda(Node):
	'''test needs to be a name but is made into an instruction in 
	pyToAsm (spillCode function needs this);
	ret needs to be a variable name;
	thenAssign and elseAssign need to be lists of assignments/asm instructions
	that would be executed on that branch.'''
	def __init__(self, params, paramAllocs, paramInits, localInits, body):
		self.name = name
		self.paramAllocs = paramAllocs
		self.paramInits = paramInits
		self.localInits = localInits
		self.body = body
	def getChildren(self):
		return (self.name, self.paramAllocs, self.paramInits, self.localInits, self.body)
	def __str__(self):
		ret = self.name + " = lambda: \n"
		ret += "\t" + str(paramAllocs) + "\n"
		ret += "\t" + str(paramInits) + "\n"
		ret += "\t" + str(localInits) + "\n"
		for instr in self.body:
			ret += +"\t" + str(instr) + "\n"
		return ret

def glModule(ast, scope):
	return getLambdas(ast.node)

def glStmt(ast, scope):
	return reduce(lambda acc, n : acc + getLambdas(n, scope), ast.nodes, [])

def glPrintnl(ast, scope):
	return getLambdas(ast.nodes[0], scope)

def glLambda(ast, scope):
	return [(ast, scope + 1)] + getLambdas(ast.code, scope + 1)

def glAssign(ast, scope):
	return getLambdas(ast.expr, scope)

def glDiscard(ast, scope):
	return getLambdas(ast.expr, scope)

def glCallFunc(ast, scope):
	return getLambdas(ast.node, scope)


def glReturn(ast, scope):
	return getLambdas(ast.value, scope)

#Finds all lambda's in the tree, returns a list of tuples: (lambda, scope level)
def getLambdas(ast, scope):
	glPass = lambda a, s: []
	return {
		Module:    glModule,
		Stmt:      glStmt,
		Printnl:   glPrintnl,
		Discard:   glDiscard,
		Assign:    glAssign,
		CallFunc:  glCallFunc,
		Lambda:    glLambda,
		Return:    glReturn
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
	if lhs.name in names:
		return Assign(Subscript(lhs, "OP_ASSIGN", [Const(0)]), heapify(ast.expr, names))
	else:
		return Assign([heapify(ast.nodes[0], names)], heapify(ast.expr, names))

def heapifyName(ast, names):
	print "heapifyName:",ast.name
	if ast.name in names:
		return Subscript(ast, "OP_ASSIGN" ,[Const(0)])
	else:
		return ast

def heapifyAssName(ast, names):
	return ast

def heapifyCallFunc(ast, names):
	return CallFunc(heapify(ast.node, names), [heapify(arg, names) for arg in ast.args])

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

#Creates new modified lambda instances
def heapifyLambda(ast, names):
	if not isinstance(ast.code, Stmt):
		ast.code = Stmt([Return(ast.code)])
	heapParams = [p in names for p in ast.argnames]
	print "heapParams:",heapParams
	pPrime = [p+"_heap" if heapParams[i] else p for i, p in enumerate(ast.argnames)]
	print "pPrime:",pPrime
	paramAllocs = [Assign(AssName( , "OP_ASSIGN"), ) for p in heapParams]
	addNewVars(ast.code, gen, newDict)
	#recurse with new dictionary
	funcCode = heapify(ast.code, gen, newDict)
	#print "newDict:",newDict
	#print "names after:",names
	gen.dec()
	return ModLambda(funcArgs, funcCode)

def heapifyReturn(ast, names):
	print ast
	return Return(heapify(ast.value, names))

def heapify(ast, names):
	return {
		Module:    heapifyModule,
		Stmt:      heapifyStmt,
		Printnl:   heapifyPrintnl,
		Const:     heapifyConst,
		UnarySub:  heapifyUnarySub,
		Add:       heapifyAdd,
		Discard:   heapifyDiscard,
		Assign:    heapifyAssign,
		Name:      heapifyName,
		AssName:   heapifyAssName,
		CallFunc:  heapifyCallFunc,
		Compare:   heapifyCompare,
		Or:        heapifyOr,
		And:       heapifyAnd,
		Not:       heapifyNot,
		List:      heapifyList,
		Dict:      heapifyDict,
		Subscript: heapifySubscript,
		IfExp:     heapifyIfExp,
		Lambda:    heapifyLambda,
		Return:    heapifyReturn
	}[ast.__class__](ast, names)

#find all lambda's, and recurse repeatedly on them
def runHeapify(ast):
	#If a variable is used in a scope that is not its origin, add to set of variables
	#We calculate this by seeing if a read or write variable's scope does not match 
	#the scope that this read or write occurred, add to set
	
	#A set of variable names that need to be heapified
	heapVars = set()
	
	print "getLambdas:"
	lambdas = getLambdas(ast.node, 0)
	for n, s in lambdas:
		s = str(s)
		print n
		read, write = varAnalysis.getVars(n.code)
		for var in read | write:
			print var
			if var[var.rfind("_")+1:] != s:
				print var,"was referenced in scope",s
				heapVars.add(var)
	print ""
	print heapVars
	
	#Now that we have a set of vars that need to be heapified, recurse through the tree
	
	heapify(ast, heapVars)
	
	#Now initalize all heapVars at the start of the program
	#i.e prepend h_1 = [0], h_2 = [0] etc. to our outermost stmt node
	for var_name in heapVars:
		stmt_array = ast.node.nodes
		new_ass_node = Assign([AssName(var_name, 'OP_ASSIGN')], List([Const(0)]))
		ast.node.nodes = [new_ass_node] + ast.node.nodes
	
	return ast
