def closureModule(ast):
	#go through the top level scope and add the variables to the dictionary
	addNewVars(ast.node)
	ast.node = closure(ast.node)

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
	ast, l = closure(ast.expr)
	return Assign([ast.nodes[0]], ast), l

def closureName(ast):
	return ast,[]

def closureAssName(ast):
	return ast, []

def closureCallFunc(ast):
	return CallFunc(closure(ast.node), [closure(arg) for arg in ast.args])

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
	ast, l = closure(ast.expr)
	return Subscript(ast, ast.flags, ast.subs), l

def closureIfExp(ast):
	ast_test, l_test = closure(ast.test)
	ast_then, l_then = closure(ast.then)
	ast_else_, l_else_ = close(ast.else_)
	
	return IfExp(ast_test, ast_then, ast_else_), l_test+l_then+l_else_

def closureModLambda(ast):
	return 

def closureReturn(ast):
	#print ast
	ast, l = closure(ast.value)
	return Return(ast), l

#names is a dictionary which keeps track of all variables seen
#so far and what they should be renamed to
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
		CallFunc:  closureCallFunc,
		Compare:   closureCompare,
		Or:        closureOr,
		And:       closureAnd,
		Not:       closureNot,
		List:      closureList,
		Dict:      closureDict,
		Subscript: closureSubscript,
		IfExp:     closureIfExp,
		ModLambda: closureModLambda,
		Return:    closureReturn
	}[ast.__class__](ast)