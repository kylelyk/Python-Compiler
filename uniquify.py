from compiler.ast import *
import astpp
import varAnalysis

#Helper to get new name and add it to names dictionary
def getNewName(name, gen, names):
	newName = name + gen.name()
	names[name] = newName
	return newName

#Helper that given an ast, will add all write variables to the
#name dictionary
def addNewVars(ast, gen, names):
	write, read = varAnalysis.getVars(ast)
	for name in write:
		getNewName(name, gen, names)

def uniquifyModule(ast, gen, names):
	#go through the top level scope and add the variables to the dictionary
	addNewVars(ast.node, gen, names)
	ast.node = uniquify(ast.node, gen, names)

def uniquifyStmt(ast, gen, names):
	return Stmt([uniquify(n, gen, names) for n in ast.nodes])

def uniquifyPrintnl(ast, gen, names):
	return Printnl([uniquify(ast.nodes[0], gen, names)], None)

def uniquifyConst(ast, gen, names):
	return ast

def uniquifyUnarySub(ast, gen, names):
	return UnarySub(uniquify(ast.expr, gen, names))

def uniquifyAdd(ast, gen, names):
	return Add([uniquify(ast.left, gen, names), uniquify(ast.right, gen, names)])

def uniquifyDiscard(ast, gen, names):
	return Discard(uniquify(ast.expr, gen, names))

def uniquifyAssign(ast, gen, names):
	return Assign([uniquify(ast.nodes[0], gen, names)], uniquify(ast.expr, gen, names))

def uniquifyName(ast, gen, names):
	#TODO remove this hack
	if ast.name == "input" or ast.name == "True" or ast.name == "False":
		return ast
	return Name(names[ast.name])

def uniquifyAssName(ast, gen, names):
	#print "names:",names
	return AssName(names[ast.name], ast.flags)

def uniquifyCallFunc(ast, gen, names):
	return CallFunc(uniquify(ast.node, gen, names), [uniquify(arg, gen, names) for arg in ast.args])

def uniquifyCompare(ast, gen, names):
	return Compare(uniquify(ast.expr, gen, names), [(ast.ops[0][0], uniquify(ast.ops[0][1], gen, names))])

def uniquifyOr(ast, gen, names):
	return Or([uniquify(ast.nodes[0], gen, names),uniquify(ast.nodes[1], gen, names)])

def uniquifyAnd(ast, gen, names):
	return And([uniquify(ast.nodes[0], gen, names),uniquify(ast.nodes[1], gen, names)])

def uniquifyNot(ast, gen, names):
	return Not(uniquify(ast.expr, gen, names))

def uniquifyList(ast, gen, names):
	return List([uniquify(n, gen, names) for n in ast.nodes])

def uniquifyDict(ast, gen, names):
	return Dict([(uniquify(k, gen, names), uniquify(v, gen, names)) for (k, v) in ast.items])

def uniquifySubscript(ast, gen, names):
	return Subscript(uniquify(ast.expr, gen, names), ast.flags, [uniquify(sub, gen, names) for sub in ast.subs])

def uniquifyIfExp(ast, gen, names):
	return IfExp(
		uniquify(ast.test, gen, names),
		uniquify(ast.then, gen, names),
		uniquify(ast.else_, gen, names)
	)

def uniquifyFunction(ast, gen, names):
	#Transform into "var = lambda"
	return uniquify(Assign(
	[AssName(ast.name, 'OP_ASSIGN')],
		Lambda(ast.argnames, ast.defaults, ast.flags, ast.code)
	), gen, names)

def uniquifyLambda(ast, gen, names):
	#Modify lambda's so that they can hold multiple stmts and a final return
	if not isinstance(ast.code, Stmt):
		ast.code = Stmt([Return(ast.code)])
	#rename args
	gen.inc()
	newDict = names.copy()
	funcArgs = [getNewName(arg, gen, newDict) for arg in ast.argnames]
	#Figure out which variables are in the scope of the body
	#and modify the dict to reflect that change
	addNewVars(ast.code, gen, newDict)
	#recurse with new dictionary
	funcCode = uniquify(ast.code, gen, newDict)
	gen.dec()
	return Lambda(funcArgs, ast.defaults, ast.flags, funcCode)

def uniquifyReturn(ast, gen, names):
	return Return(uniquify(ast.value, gen, names))

#names is a dictionary which keeps track of all variables seen
#so far and what they should be renamed to
def uniquify(ast, gen, names):
	return {
		Module:    uniquifyModule,
		Stmt:      uniquifyStmt,
		Printnl:   uniquifyPrintnl,
		Const:     uniquifyConst,
		UnarySub:  uniquifyUnarySub,
		Add:       uniquifyAdd,
		Discard:   uniquifyDiscard,
		Assign:    uniquifyAssign,
		Name:      uniquifyName,
		AssName:   uniquifyAssName,
		CallFunc:  uniquifyCallFunc,
		Compare:   uniquifyCompare,
		Or:        uniquifyOr,
		And:       uniquifyAnd,
		Not:       uniquifyNot,
		List:      uniquifyList,
		Dict:      uniquifyDict,
		Subscript: uniquifySubscript,
		IfExp:     uniquifyIfExp,
		Function:  uniquifyFunction,
		Lambda:    uniquifyLambda,
		Return:    uniquifyReturn
	}[ast.__class__](ast, gen, names)
