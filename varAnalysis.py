from compiler.ast import *
from HelperClasses import *
import astpp

#helper to combine the 2-tuple's innards
def combine(first, second):
	#print "first:",first
	#print "second:",second
	f1, f2 = first
	s1, s2 = second
	return (f1 | s1, f2 | s2)

def varsModule(ast):
	#need to do disjunct with free and written_to?
	return getVars(ast.node)

def varsStmt(ast):
	return reduce(lambda acc, n: combine(acc, getVars(n)), ast.nodes, (set(), set()))

def varsPrintnl(ast):
	return getVars(ast.nodes[0])

def varsConst(ast):
	return set(), set()

def varsUnarySub(ast):
	return getVars(ast.expr)

def varsAdd(ast):
	return combine(getVars(ast.left), getVars(ast.right))

def varsDiscard(ast):
	return getVars(ast.expr)

def varsAssign(ast):
	#TODO Find a better way to do this
	if isinstance(ast.nodes[0], Subscript):
		return combine(getVars(ast.nodes[0]), getVars(ast.expr))
	else:
		return combine(getVars(ast.nodes[0]), getVars(ast.expr))

def varsName(ast):
	return set(), set([ast.name])

def varsAssName(ast):
	return set([ast.name]), set()

def varsCallFunc(ast):
	return combine(getVars(ast.node), reduce(lambda acc, arg: combine(acc, getVars(arg)), ast.args, (set(),set())))

def varsCallRuntime(ast):
	return combine(getVars(ast.node), reduce(lambda acc, arg: combine(acc, getVars(arg)), ast.args, (set(),set())))

def varsCompare(ast):
	return combine(getVars(ast.ops[0][1]), getVars(ast.expr))

def varsOr(ast):
	return combine(getVars(ast.nodes[0]), getVars(ast.nodes[1]))

def varsAnd(ast):
	return combine(getVars(ast.nodes[0]), getVars(ast.nodes[1]))

def varsNot(ast):
	return getVars(ast.expr)

def varsList(ast):
	return reduce(lambda acc, arg: combine(acc, getVars(arg)), ast.nodes, (set(),set()))

def varsDict(ast):
	return reduce(lambda acc, (k,v): combine(combine(acc, getVars(k)), getVars(v)), ast.items, (set(),set()))

def varsSubscript(ast):
	return combine(getVars(ast.expr), getVars(ast.subs[0]))

def varsIfExp(ast):
	return combine(combine(getVars(ast.test), getVars(ast.then)), getVars(ast.else_))

def varsFunction(ast):
	return set([ast.name]), set()

def varsLambda(ast):
	return set(), set()

def varsReturn(ast):
	return getVars(ast.value)

def varsGetTag(ast):
	return getVars(ast.arg)

def varsInjectFrom(ast):
	return getVars(ast.arg)

def varsProjectTo(ast):
	return getVars(ast.arg)

def varsLet(ast):
	if isinstance(ast.var, Subscript):
		return combine(getVars(ast.var), combine(getVars(ast.rhs), getVars(ast.body)))
	else:
		return combine((set([ast.var.name]), set()), combine(getVars(ast.rhs), getVars(ast.body)))

def varsIsType(ast):
	return getVars(ast.arg)

def varsThrowError(ast):
	return set(), set()

#Returns a tuple of: set of all variables written to, set of all variables read from
#In the current scope only and does not recurse on functions and lambda's
def getVars(ast):
	return {
		Module:      varsModule,
		Stmt:        varsStmt,
		Printnl:     varsPrintnl,
		Const:       varsConst,
		UnarySub:    varsUnarySub,
		Add:         varsAdd,
		Discard:     varsDiscard,
		Assign:      varsAssign,
		Name:        varsName,
		AssName:     varsAssName,
		CallFunc:    varsCallFunc,
		CallRuntime: varsCallRuntime,
		Compare:     varsCompare,
		Or:          varsOr,
		And:         varsAnd,
		Not:         varsNot,
		List:        varsList,
		Dict:        varsDict,
		Subscript:   varsSubscript,
		IfExp:       varsIfExp,
		Function:    varsFunction,
		Lambda:      varsLambda,
		Return:      varsReturn,
		GetTag:      varsGetTag,
		InjectFrom:  varsInjectFrom,
		ProjectTo:   varsProjectTo,
		Let:         varsLet,
		IsType:      varsIsType,
		ThrowError:  varsThrowError
	}[ast.__class__](ast)