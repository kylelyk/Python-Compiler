import compiler
from compiler.ast import *
from x86AST import *

__all__ = ('flatten',)

def addAssign(node, newast, gen, map, name = None):
	if not name:
		name = gen.inc().name()
		map[name] = len(map)
	elif name not in map:
		map[name] = len(map)
	newnode = Assign([AssName(name, 'OP_ASSIGN')], node)
	newast.nodes.append(newnode)
	return Name(name)

def flatModule(ast, newast, gen, map):
	return flatten(ast.node, newast, gen, map)

def flatStmt(ast, newast, gen, map):
	newast = Stmt([])
	for node in ast.nodes:
		flatten(node, newast, gen, map)
	return newast

def flatPrintnl(ast, newast, gen, map):
	simple = flatten(ast.nodes[0], newast, gen, map)
	return newast.nodes.append(Printnl([simple], None))

def flatConst(ast, newast, gen, map):
	return ast

def flatName(ast, newast, gen, map):
	return ast

def flatUnarySub(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	if isinstance(simple, Const):
		return Const(-simple.value)
	return addAssign(UnarySub(simple), newast, gen, map)

def flatAdd(ast, newast, gen, map):
	s1 = flatten(ast.left, newast, gen, map)
	s2 = flatten(ast.right, newast, gen, map)
	return addAssign(Add((s1, s2)), newast, gen, map)

def flatDiscard(ast, newast, gen, map):
	return flatten(ast.expr, newast, gen, map)

def flatAssign(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	return addAssign(simple, newast, gen, map, ast.nodes[0].name)

def flatCallFunc(ast, newast, gen, map):
	return addAssign(ast, newast, gen, map)

def flatten(ast, newast, gen, map):
	return {
		Module:   flatModule,
		Stmt:     flatStmt,
		Printnl:  flatPrintnl,
		Const:    flatConst,
		UnarySub: flatUnarySub,
		Add:      flatAdd,
		Discard:  flatDiscard,
		Assign:   flatAssign,
		Name:     flatName,
		CallFunc: flatCallFunc
	}[ast.__class__](ast, newast, gen, map)