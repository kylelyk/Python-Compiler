from compiler.ast import *
from HelperClasses import *
import astpp
import varAnalysis

#Helper to get new name and add it to names dictionary
def getNewName(name,gen, names, scopes):
	newName = name + scopes[-1]
	names[0][name] = newName
	names[1][newName] = name
	return newName

#Helper that given an ast, will add all write variables to the
#name dictionary
def addNewVars(ast,gen, names, scopes):
	write, read = varAnalysis.getVars(ast)
	for name in write:
		getNewName(name,gen, names, scopes)

def uniquifyModule(ast,gen, names, scopes):
	#go through the top level scope and add the variables to the dictionary
	addNewVars(ast.node,gen, names, scopes)
	ast.node = uniquify(ast.node,gen, names, scopes)

def uniquifyStmt(ast,gen, names, scopes):
	return Stmt([uniquify(n,gen, names, scopes) for n in ast.nodes])

def uniquifyPrintnl(ast,gen, names, scopes):
	return Printnl([uniquify(ast.nodes[0],gen, names, scopes)], None)

def uniquifyConst(ast,gen, names, scopes):
	return ast

def uniquifyUnarySub(ast,gen, names, scopes):
	return UnarySub(uniquify(ast.expr,gen, names, scopes))

def uniquifyAdd(ast,gen, names, scopes):
	return Add([uniquify(ast.left,gen, names, scopes), uniquify(ast.right,gen, names, scopes)])

def uniquifyDiscard(ast,gen, names, scopes):
	return Discard(uniquify(ast.expr,gen, names, scopes))

def uniquifyAssign(ast,gen, names, scopes):
	return Assign([uniquify(ast.nodes[0],gen, names, scopes)], uniquify(ast.expr,gen, names, scopes))

def uniquifyName(ast,gen, names, scopes):
	if ast.name == "True" or ast.name == "False":
		return ast
	#TODO remove this hack
	if ast.name not in names[0]:
		return ast
	return Name(names[0][ast.name])

def uniquifyAssName(ast,gen, names, scopes):
	return AssName(names[0][ast.name], ast.flags)

def uniquifyCallFunc(ast,gen, names, scopes):
	return CallFunc(uniquify(ast.node,gen, names, scopes), [uniquify(arg,gen, names, scopes) for arg in ast.args])

def uniquifyCallRuntime(ast,gen, names, scopes):
	return CallRuntime(ast.node, [uniquify(arg,gen, names, scopes) for arg in ast.args])

def uniquifyCompare(ast,gen, names, scopes):
	return Compare(uniquify(ast.expr,gen, names, scopes), [(ast.ops[0][0], uniquify(ast.ops[0][1],gen, names, scopes))])

def uniquifyOr(ast,gen, names, scopes):
	return Or([uniquify(ast.nodes[0],gen, names, scopes),uniquify(ast.nodes[1],gen, names, scopes)])

def uniquifyAnd(ast,gen, names, scopes):
	return And([uniquify(ast.nodes[0],gen, names, scopes),uniquify(ast.nodes[1],gen, names, scopes)])

def uniquifyNot(ast,gen, names, scopes):
	return Not(uniquify(ast.expr,gen, names, scopes))

def uniquifyList(ast,gen, names, scopes):
	return List([uniquify(n,gen, names, scopes) for n in ast.nodes])

def uniquifyDict(ast,gen, names, scopes):
	return Dict([(uniquify(k,gen, names, scopes), uniquify(v,gen, names, scopes)) for (k, v) in ast.items])

def uniquifySubscript(ast,gen, names, scopes):
	return Subscript(uniquify(ast.expr,gen, names, scopes), ast.flags, [uniquify(sub,gen, names, scopes) for sub in ast.subs])

def uniquifyIfExp(ast,gen, names, scopes):
	return IfExp(
		uniquify(ast.test,gen, names, scopes),
		uniquify(ast.then,gen, names, scopes),
		uniquify(ast.else_,gen, names, scopes)
	)

def uniquifyIf(ast,gen, names, scopes):
	return If(
		[(uniquify(ast.tests[0][0],gen, names, scopes),
		uniquify(ast.tests[0][1],gen, names, scopes))],
		uniquify(ast.else_,gen, names, scopes)
	)

def uniquifyFunction(ast,gen, names, scopes):
	#Transform into "var = lambda"
	return uniquify(Assign(
	[AssName(ast.name, ['OP_ASSIGN',ast.flags,"NONE"])],
		Lambda(ast.argnames, ast.defaults, ast.flags, ast.code)
	),gen, names, scopes)

def uniquifyLambda(ast,gen, names, scopes):
	#Modify lambda's so that they can hold multiple stmts and a final return
	if not isinstance(ast.code, Stmt):
		ast.code = Stmt([Return(ast.code)])
	#rename args
	scopes.append(gen.inc().name())
	#Copy the first mapping so it doesn't persist after the scope is over
	newDicts = (names[0].copy(), names[1])
	funcArgs = [getNewName(arg, gen, newDicts, scopes) for arg in ast.argnames]
	#Figure out which variables are in the scope of the body
	#and modify the dict to reflect that change
	addNewVars(ast.code, gen, newDicts, scopes)
	#recurse with new dictionary
	scopes.pop()
	funcCode = uniquify(ast.code, gen, newDicts, scopes)
	return Lambda(funcArgs, ast.defaults, ast.flags, funcCode)

def uniquifyReturn(ast,gen, names, scopes):
	return Return(uniquify(ast.value,gen, names, scopes))

def uniquifyWhile(ast,gen, names, scopes):
	return While(uniquify(ast.test,gen, names, scopes), uniquify(ast.body,gen, names, scopes), None)

def uniquifyAssAttr(ast,gen, names, scopes):
	return AssAttr(uniquify(ast.expr,gen, names, scopes), names[ast.attrname], ast.flags)

def uniquifyGetattr(ast,gen, names, scopes):
	return Getattr(uniquify(ast.expr,gen, names, scopes), names[ast.attrname])

def uniquifyInjectFrom(ast,gen, names, scopes):
	return InjectFrom(ast.typ, uniquify(ast.arg,gen, names, scopes))

def uniquifyLet(ast,gen, names, scopes):
	return Let(uniquify(ast.var,gen, names, scopes), uniquify(ast.rhs,gen, names, scopes), uniquify(ast.body,gen, names, scopes))

#names is a 2-tuple of dictionaries which keeps track of all variables seen
#so far and what they should be renamed to, the renamed variables to their original names
def uniquify(ast,gen, names, scopes):
	return {
		Module:      uniquifyModule,
		Stmt:        uniquifyStmt,
		Printnl:     uniquifyPrintnl,
		Const:       uniquifyConst,
		UnarySub:    uniquifyUnarySub,
		Add:         uniquifyAdd,
		Discard:     uniquifyDiscard,
		Assign:      uniquifyAssign,
		Name:        uniquifyName,
		AssName:     uniquifyAssName,
		CallFunc:    uniquifyCallFunc,
		CallRuntime: uniquifyCallRuntime,
		Compare:     uniquifyCompare,
		Or:          uniquifyOr,
		And:         uniquifyAnd,
		Not:         uniquifyNot,
		List:        uniquifyList,
		Dict:        uniquifyDict,
		Subscript:   uniquifySubscript,
		IfExp:       uniquifyIfExp,
		If:          uniquifyIf,
		Function:    uniquifyFunction,
		Lambda:      uniquifyLambda,
		Return:      uniquifyReturn,
		While:       uniquifyWhile,
		#AssAttr:     uniquifyAssAttr,
		#Getattr:     uniquifyGetattr,
		InjectFrom:  uniquifyInjectFrom,
		Let:         uniquifyLet
	}[ast.__class__](ast,gen, names, scopes)

def runUniquify(ast):
	gen = GenSym("$")
	names = ({},{})
	uniquify(ast, gen, names, [gen.name()])
	return names