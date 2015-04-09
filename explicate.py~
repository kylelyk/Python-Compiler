from compiler.ast import *
from HelperClasses import *
import astpp

def explicateModule(ast, gen):
	ast.node = explicate(ast.node, gen)

def explicateStmt(ast, gen):
	return Stmt([explicate(n, gen) for n in ast.nodes])

def explicatePrintnl(ast, gen):
	return Printnl([explicate(ast.nodes[0], gen)], None)

def explicateConst(ast, gen):
	return ast

def explicateUnarySub(ast, gen):
	name = Name(gen.inc().name())
	return Let(name, explicate(ast.expr, gen),
		IfExp(InjectFrom("bool", Or([IsType("bool",name), IsType("int",name)])),
			InjectFrom("int",UnarySub(ProjectTo("boolint", name))),
			ThrowError(Const("negError"))
		)
	)

def explicateAdd(ast, gen):
	name1 = Name(gen.inc().name())
	name2 = Name(gen.inc().name())
	return Let(name1, explicate(ast.left, gen),
		Let(name2, explicate(ast.right, gen),
			#If(n1 = int || n2 = bool) && (n2 = int || n2 = bool)
			IfExp(InjectFrom("bool",And([Or([IsType("bool",name1), IsType("int",name1)]),Or([IsType("bool",name2), IsType("int",name2)])])),
				InjectFrom("int",Add((ProjectTo("boolint",name1),ProjectTo("boolint",name2)))),
				IfExp(InjectFrom("bool",And([IsType("big",name1), IsType("big",name2)])),
					InjectFrom("big",CallRuntime(Name("add"),[ProjectTo("big", name1),ProjectTo("big", name2)])),
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
	def rec(index, len, args, cont):
		print "rec called with:", index, len, args
		if index < len:
			return Let(args[index][0], args[index][1], rec(index+1, len, args, cont))
		else:
			return cont
	
	f = Name(gen.inc().name())
	o = Name(gen.inc().name())
	newFunc = explicate(ast.node, gen)
	args = [(Name(gen.inc().name()), explicate(arg, gen)) for arg in ast.args]
	print "ast.args:", ast.args
	print "args:",args
	return Let(
		f, 
		newFunc, 
		rec(0, len(args), args, IfExp(
			InjectFrom("bool", IsType("class",f)),
			Let(
				o,
				InjectFrom("big", CallRuntime(Name("create_object"),[f])),
				IfExp(
					InjectFrom("bool", CallRuntime(Name("has_attr"), [f, Const("__init__")])),
					Let(
						Name(gen.inc().name()),
						CallFunc(
							InjectFrom("big", CallRuntime(Name("get_function"), [CallRuntime(Name("get_attr"), [f, Const("__init__")])])),
							[o] + [tup[0] for tup in args]
						),
						o
					),
					o
				)
			),
			IfExp(
				InjectFrom("bool", IsType("bound_method",f)),
				CallFunc(
					InjectFrom("big", CallRuntime(Name("get_function"), [f])), 
					[InjectFrom("big", CallRuntime(Name("get_receiver"), [f]))] + [tup[0] for tup in args]
				),
				IfExp(
					InjectFrom("bool", IsType("unbound_method",f)),
					CallFunc(
						InjectFrom("big", CallRuntime(Name("get_function"), [f])), 
						[tup[0] for tup in args]
					),
					CallFunc(explicate(ast.node, gen), [explicate(arg, gen) for arg in ast.args])
				)
			)
		))
	)

def explicateCallRuntime(ast, gen):
	return CallRuntime(ast.node, [explicate(arg, gen) for arg in ast.args])

def explicateCompare(ast, gen):
	op, expr = ast.ops[0]
	if op == "is":
		return Compare(explicate(ast.expr, gen), [("is", explicate(expr, gen))])
	else:
		lhs = explicate(ast.expr, gen)
		rhs = explicate(expr, gen)
		name1 = Name(gen.inc().name())
		name2 = Name(gen.inc().name())
		funcname = Name("not_equal" if op == "!=" else "equal")
		return Let(name1, lhs, Let(name2, rhs, 
			IfExp(
				InjectFrom("bool",And([IsType("big", name1), IsType("big", name2)])),
				InjectFrom("bool", CallRuntime(funcname, [ProjectTo("big",name1), ProjectTo("big",name2)])),
				IfExp(
					InjectFrom("bool",Or([IsType("big", name1), IsType("big", name2)])),
					Name("False") if op == "==" else Name("True"),
					Compare(ProjectTo("boolint", name1), [(op, ProjectTo("boolint", name2))])
				)
			)
		))

def explicateOr(ast, gen):
	#Implements Short-circuiting using nested IfExp's
	name = Name(gen.inc().name())
	return Let(name,
		explicate(ast.nodes[0], gen),
		IfExp(InjectFrom("bool",CallRuntime(Name("is_true"), [name])),
			name,
			explicate(ast.nodes[1], gen)
		)
	)

def explicateAnd(ast, gen):
	#Implements Short-circuiting using nested IfExp's
	name = Name(gen.inc().name())
	return Let(name,
		explicate(ast.nodes[0], gen),
		IfExp(InjectFrom("bool",CallRuntime(Name("is_true"), [name])),
			explicate(ast.nodes[1], gen),
			name
		)
	)

def explicateNot(ast, gen):
	return Not(explicate(ast.expr, gen))

def explicateList(ast, gen):
	return List([explicate(n, gen) for n in ast.nodes])

def explicateDict(ast, gen):
	return Dict([(explicate(k, gen), explicate(v, gen)) for (k, v) in ast.items])

def explicateSubscript(ast, gen):
	return Subscript(ast.expr, None, [explicate(sub, gen) for sub in ast.subs])

def explicateIfExp(ast, gen):
	test = explicate(ast.test, gen)
	then_node = explicate(ast.then, gen)
	else_node = explicate(ast.else_, gen)
	
	#Check if the input is a list or dict, and spit out appropriate node
	if isinstance(test,List):
		return then_node if test.nodes else else_node
	elif isinstance(test,Dict):
		return then_node if test.items else else_node
	
	return IfExp(InjectFrom("bool", CallRuntime(Name("is_true"),[test])),then_node, else_node)

#Turn If into IfExp
def explicateIf(ast, gen):
	test = explicate(ast.tests[0][0], gen)
	then_node = explicate(ast.tests[0][1], gen)
	else_node = explicate(ast.else_, gen)
	
	#Check if the input is a list or dict, and spit out appropriate node
	if isinstance(test,List):
		return then_node if test.nodes else else_node
	elif isinstance(test,Dict):
		return then_node if test.items else else_node
	
	return Discard(IfExp(InjectFrom("bool", CallRuntime(Name("is_true"),[test])),then_node, else_node))

def explicateLambda(ast, gen):
	return Lambda(ast.argnames, ast.defaults, ast.flags, explicate(ast.code, gen))

def explicateReturn(ast, gen):
	return Return(explicate(ast.value, gen))

def explicateWhile(ast, gen):
	newTest = InjectFrom("bool", CallRuntime(Name("is_true"),[explicate(ast.test, gen)]))
	return While(newTest, explicate(ast.body, gen), None)

def explicateAssAttr(ast, gen):
	return AssAttr(explicate(ast.expr, gen), ast.attrname, ast.flags)

def explicateGetattr(ast, gen):
	return Getattr(explicate(ast.expr, gen), ast.attrname)

def explicateInjectFrom(ast, gen):
	return InjectFrom(ast.typ, explicate(ast.arg, gen))

def explicateLet(ast, gen):
	return Let(ast.var, explicate(ast.rhs, gen), explicate(ast.body, gen))

def explicate(ast, gen):
	return {
		Module:      explicateModule,
		Stmt:        explicateStmt,
		Printnl:     explicatePrintnl,
		Const:       explicateConst,
		UnarySub:    explicateUnarySub,
		Add:         explicateAdd,
		Discard:     explicateDiscard,
		Assign:      explicateAssign,
		Name:        explicateName,
		CallFunc:    explicateCallFunc,
		CallRuntime: explicateCallRuntime,
		Compare:     explicateCompare,
		Or:          explicateOr,
		And:         explicateAnd,
		Not:         explicateNot,
		List:        explicateList,
		Dict:        explicateDict,
		Subscript:   explicateSubscript,
		IfExp:       explicateIfExp,
		If:          explicateIf,
		Lambda:      explicateLambda,
		Return:      explicateReturn,
		While:       explicateWhile,
		#AssAttr:     explicateAssAttr,
		#Getattr:     explicateGetattr,
		InjectFrom:  explicateInjectFrom,
		Let:         explicateLet
	}[ast.__class__](ast, gen)
