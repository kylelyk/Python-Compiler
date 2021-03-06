from HelperClasses import *

#These passes should only be run after uniquifying

def linesModule(ast, map):
	lines(ast.node, map)

def linesStmt(ast, map):
	for n in ast.nodes:
		lines(n, map)

def linesAssign(ast, map):
	n = ast.nodes[0]
	if not isinstance(n, Subscript):
		if n.name not in map:
			map[n.name] = n.flags[1]
		if isinstance(ast.expr, Lambda):
			lines(ast.expr, map)

def linesIf(ast, map):
	lines(ast.tests[0][1], map)
	lines(ast.else_, map)

def linesLambda(ast, map):
	lines(ast.code, map)

def linesWhile(ast, map):
	lines(ast.body, map)

def lines(ast, map):
	passFunc = lambda a, m : None
	return {
		Module:    linesModule,
		Stmt:      linesStmt,
		Assign:    linesAssign,
		Printnl:   passFunc,
		Discard:   passFunc,
		If:        linesIf,
		Lambda:  linesLambda,
		Return:    passFunc,
		While:     linesWhile,
	}[ast.__class__](ast, map)


def typesModule(ast, map):
	types(ast.node, map)

def typesStmt(ast, map):
	for n in ast.nodes:
		types(n, map)

def typesAssign(ast, map):
	type = ast.nodes[0].flags[2]
	if type != "NONE":
		map[ast.nodes[0].name] = type

def typesIf(ast, map):
	types(ast.tests[0][1], map)
	types(ast.else_, map)

def typesLambda(ast, map):
	types(ast.code, map)

def typesWhile(ast, map):
	types(ast.body, map)

def types(ast, map):
	passFunc = lambda a, m : None
	return {
		Module:    typesModule,
		Stmt:      typesStmt,
		Assign:    typesAssign,
		Printnl:   passFunc,
		Discard:   passFunc,
		If:        typesIf,
		Lambda:    typesLambda,
		Return:    passFunc,
		While:     typesWhile,
	}[ast.__class__](ast, map)