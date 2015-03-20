from compiler.ast import *
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
	return set(), getVars(ast.nodes[0])

def varsConst(ast):
	return set()

def varsUnarySub(ast):
	return getVars(ast.expr)

def varsAdd(ast):
	return getVars(ast.left) | getVars(ast.right)

def varsDiscard(ast):
	return set(), getVars(ast.expr)

def varsAssign(ast):
	#TODO Find a better way to do this
	if isinstance(ast.nodes[0], Subscript):
		return set(), getVars(ast.nodes[0]) | getVars(ast.expr)
	else:
		return getVars(ast.nodes[0]), getVars(ast.expr)

def varsName(ast):
	return set([ast.name])

def varsAssName(ast):
	return set([ast.name])

def varsCallFunc(ast):
	return getVars(ast.node) | reduce(lambda acc, arg: acc | getVars(arg), ast.args, set([]))

def varsCompare(ast):
	return getVars(ast.ops[0][1]) | getVars(ast.expr)

def varsOr(ast):
	return getVars(ast.nodes[0]) | getVars(ast.nodes[1])

def varsAnd(ast):
	return getVars(ast.nodes[0]) | getVars(ast.nodes[1])

def varsNot(ast):
	return getVars(ast.expr)

def varsList(ast):
	return reduce(lambda acc, arg: acc | getVars(arg), ast.nodes, set([]))

def varsDict(ast):
	return reduce(lambda acc, (k,v): acc | getVars(k) | getVars(v), ast.items, set([]))

def varsSubscript(ast):
	return getVars(ast.expr) | getVars(ast.subs[0])

def varsIfExp(ast):
	return getVars(ast.test) | getVars(ast.then) | getVars(ast.else_)

def varsFunction(ast):
	return set([ast.name]), set()

def varsLambda(ast):
	return set()

def varsReturn(ast):
	return set(), getVars(ast.value)

#Returns a tuple of: set of all variables written to, set of all variables read from
#In the current scope only and does not recurse on functions and lambda's
def getVars(ast):
	return {
		Module:    varsModule,
		Stmt:      varsStmt,
		Printnl:   varsPrintnl,
		Const:     varsConst,
		UnarySub:  varsUnarySub,
		Add:       varsAdd,
		Discard:   varsDiscard,
		Assign:    varsAssign,
		Name:      varsName,
		AssName:   varsAssName,
		CallFunc:  varsCallFunc,
		Compare:   varsCompare,
		Or:        varsOr,
		And:       varsAnd,
		Not:       varsNot,
		List:      varsList,
		Dict:      varsDict,
		Subscript: varsSubscript,
		IfExp:     varsIfExp,
		Function:  varsFunction,
		Lambda:    varsLambda,
		Return:    varsReturn
	}[ast.__class__](ast)