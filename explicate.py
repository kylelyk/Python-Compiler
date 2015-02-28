from compiler.ast import *
import astpp

class GetTag(Node):
	def __init__(self, arg):
		self.arg = arg
	def getChildren(self):
		return (self.arg,)
class InjectFrom(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
class ProjectTo(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
class Let(Node):
	def __init__(self, var, rhs, body):
		self.var = var
		self.rhs = rhs
		self.body = body
	def getChildren(self):
		return (self.var, self.rhs, self.body)
class IsType(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
class ThrowError(Node):
	def __init__(self, msg):
		self.msg = msg
	def getChildren(self):
		return (self.msg,)

def explicateModule(ast, gen):
	#print "explicateModule called"
	ast.node = explicate(ast.node, gen)

def explicateStmt(ast, gen):
	#print "explicateStmt called"
	return Stmt([explicate(n, gen) for n in ast.nodes])

def explicatePrintnl(ast, gen):
	#print "explicatePrintnl called"
	return Printnl([explicate(ast.nodes[0], gen)], None)

def explicateConst(ast, gen):
	return ast

def explicateUnarySub(ast, gen):
	name = Name(gen.inc().name())
	return Let(name, explicate(ast.expr, gen),
		IfExp(InjectFrom("bool",IsType("bool",name)),
			InjectFrom("int",UnarySub(ProjectTo("bool", name))),
			IfExp(InjectFrom("bool",IsType("int",name)),
				InjectFrom("int",UnarySub(ProjectTo("int", name))),
				ThrowError(Const("negError"))
			)
		)
	)

def explicateAdd(ast, gen):
	name1 = Name(gen.inc().name())
	name2 = Name(gen.inc().name())
	return Let(name1, explicate(ast.left, gen),
		Let(name2, explicate(ast.right, gen),
			IfExp(InjectFrom("bool",And([Or([IsType("bool",name1), IsType("int",name1)]),Or([IsType("bool",name2), IsType("int",name2)])])),
				InjectFrom("int",Add((ProjectTo("int", name1),ProjectTo("int", name2)))),
				IfExp(InjectFrom("bool",And([IsType("big",name1), IsType("big",name2)])),
					InjectFrom("big",CallFunc("add",[ProjectTo("big", name1),ProjectTo("big", name2)])),
					ThrowError(Const("addError"))
				)
			)
		)
	)

def explicateDiscard(ast, gen):
	return Discard(explicate(ast.expr,gen))

def explicateAssign(ast, gen):
	return Assign([ast.nodes[0]], explicate(ast.expr, gen))

def explicateName(ast, gen):
	return ast

def explicateCallFunc(ast, gen):
	return CallFunc(ast.node, [explicate(arg, gen) for arg in ast.args])

def explicateCompare(ast, gen):
	op, expr = ast.ops[0]
	if op == "is":
		return Compare(explicate(ast.expr, gen), [("is", explicate(expr, gen))])
	else:
		lhs = explicate(ast.expr, gen)
		rhs = explicate(expr, gen)
		name1 = Name(gen.inc().name())
		name2 = Name(gen.inc().name())
		funcname = "not_equal" if op == "!=" else "equal"
		return Let(name1, lhs, Let(name2, rhs, IfExp(
			And([Not(IsType("big", name1)), Not(IsType("big", name2))]),
			Compare(name1,[(op,name2)]),
			IfExp(
				InjectFrom("bool", And([IsType("big", name1), IsType("big", name2)])),
				InjectFrom("bool", CallFunc(funcname, [ProjectTo("big",name1), ProjectTo("big",name2)])),
				Name("False")
			)
		)))

def explicateOr(ast, gen):
	#Implements Short-circuiting using nested IfStmt's
	def rec(nodes, index):
		if index < len(nodes) - 1:
			name = Name(gen.inc().name())
			return Let(name, explicate(nodes[index], gen),
				IfExp(name, name, rec(nodes, index+1))
			)
		return explicate(nodes[index], gen)
	return rec(ast.nodes, 0)

def explicateAnd(ast, gen):
	#Implements Short-circuiting using nested IfStmt's
	def rec(nodes, index):
		if index < len(nodes) - 1:
			name = Name(gen.inc().name())
			return Let(name, explicate(nodes[index], gen),
				IfExp(name, rec(nodes, index+1), name)
			)
		return explicate(nodes[index], gen)
	return rec(ast.nodes, 0)

def explicateNot(ast, gen):
	return Not(InjectFrom("bool",CallFunc("is_true", [explicate(ast.expr, gen)])))

def explicateList(ast, gen):
	return List([explicate(n, gen) for n in ast.nodes])

def explicateDict(ast, gen):
	return Dict([(explicate(k, gen), explicate(v, gen)) for (k, v) in ast.items])

def explicateSubscript(ast, gen):
	return Subscript(ast.expr, None, [explicate(sub, gen) for sub in ast.subs])

def explicateIfExp(ast, gen):
	return IfExp(explicate(ast.test, gen), explicate(ast.then, gen), explicate(ast.else_, gen))

def explicate(ast, gen):
	return {
		Module:   explicateModule,
		Stmt:     explicateStmt,
		Printnl:  explicatePrintnl,
		Const:    explicateConst,
		UnarySub: explicateUnarySub,
		Add:      explicateAdd,
		Discard:  explicateDiscard,
		Assign:   explicateAssign,
		Name:     explicateName,
		CallFunc: explicateCallFunc,
		Compare:  explicateCompare,
		Or:       explicateOr,
		And:      explicateAnd,
		Not:      explicateNot,
		List:     explicateList,
		Dict:     explicateDict,
		Subscript:explicateSubscript,
		IfExp:    explicateIfExp
	}[ast.__class__](ast, gen)