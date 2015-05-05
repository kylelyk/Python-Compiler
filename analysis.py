import sys

'''
Graph will have edges between nodes whose types are the same
Compound types (functions) will have sub nodes so that edges between
these subnodes and other nodes describes that the other node has the same
type as part of the function. Ex:
	x = true
	def f1():
		return lambda x : 0

	y = f1()

y will have an edge to f1's subnode 

	typeFunc([typeBool],typeInt) 

where f1 would have the type

	typeFunc([], typeFunc([typeBool],typeInt))

The constraint Graph has nodes (keys) of variable "objects" where each object
has an optional name and a type tree, and edges (values) which are other variable objects



def

a = 0
b = True
b = a
def f(x,y):
	c = x + b
	d = x and b
	return d
g = f
z = f(a,b)



def addInts(x,y):
	return lambda y : x + y
z = addInts(0)(1)




Name	Line	Type
a		1		[int, list]
b		2		[bool, int, list]
f		3		lambda

'''


import compiler
from compiler.ast import *
from HelperClasses import *

class VarObject:
	def __init__(self, name, types):
		self.name = name
		self.types = types

class TAny:
	def __class__(self):
		return TAny
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TAny"
	def __repr__(self):
		return str(self)

class TNone:
	def __class__(self):
		return TNone
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TNone"
	def __repr__(self):
		return str(self)

class TInt:
	def __class__(self):
		return TInt
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TInt"
	def __repr__(self):
		return str(self)

class TBool:
	def __class__(self):
		return TBool
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TBool"
	def __repr__(self):
		return str(self)

class TList:
	def __init__(self, typ):
		self.typ = typ
	def __class__(self):
		return TList
	def __eq__(self, other):
		return other.__class__ == self.__class__ and other.typ == self.typ
	def __hash__(self):
		return hash((self.__class__, self.typ))
	def __str__(self):
		return "TList("+str(self.typ)+")"
	def __repr__(self):
		return str(self)

class TDict:
	def __init__(self, ktyp, vtyp):
		self.ktyp = ktyp
		self.vtyp = vtyp
	def __class__(self):
		return TDict
	def __eq__(self, other):
		return other.__class__ == self.__class__ and other.ktyp == self.ktyp and other.vtyp == self.vtyp
	def __hash__(self):
		return hash((self.__class__, self.ktyp, self.vtyp))
	def __str__(self):
		return "TDict("+str(self.ktyp)+","+str(self.vtyp)+")"
	def __repr__(self):
		return str(self)

class TFunc:
	def __init__(self, args, ret):
		self.args = args
		self.ret = ret
	def __class__(self):
		return TDict
	def __eq__(self, other):
		return other.__class__ == self.__class__ and  other.args == self.args and other.ret == self.ret
	def __hash__(self): 
		return hash((self.__class__, self.args, self.ret))
	def __str__(self):
		s = "TFunc("
		for a in self.args:
			s += str(a)+","
		s += str(self.ret)+")"
		return s
	def __repr__(self):
		return str(self)

class TIter:
	def __init__(self, ktyp, vtyp):
		self.ktyp = ktyp
		self.vtyp = vtyp
	def __class__(self):
		return TDict
	def __eq__(self, other):
		return other.__class__ == self.__class__ and other.ktyp == self.ktyp and other.vtyp == self.vtyp
	def __hash__(self):
		return hash((self.__class__, self.ktyp, self.vtyp))
	def __str__(self):
		return "TIter("+str(self.ktyp)+","+str(self.vtyp)+")"

def addEdge(source, dest, graph, label=None):
	if source in graph:
		graph[source].append((dest,label))
	else:
		graph[source] = [(dest,label)]
	if dest not in graph:
		graph[dest] = []

def analyzeStmt(ast, graph, consts, gens, func):
	for n in ast.nodes:
		analyze(n, graph, consts, gens, func)

def analyzePrintnl(ast, graph, consts, gens, func):
	return None, None

def analyzeConst(ast, graph, consts, gens, func):
	name = gens["const"].inc().name()
	consts[name] = TInt()
	return name, None

def analyzeName(ast, graph, consts, gens, func):
	return ast.name, None

def analyzeUnarySub(ast, graph, consts, gens, func):
	name = gens["neg"].inc().name()
	expr, lbl = analyze(ast.expr, graph, consts, gens, func)
	addEdge(expr, name, graph, lbl)
	return name, None

def analyzeAdd(ast, graph, consts, gens, func):
	rhs, r_lbl = analyze(ast.right, graph, consts, gens, func)
	lhs, l_lbl = analyze(ast.left,  graph, consts, gens, func)
	name = gens["add"].inc().name()
	addEdge(rhs, name, graph, r_lbl)
	addEdge(lhs, name, graph, l_lbl)
	return name, None

def analyzeDiscard(ast, graph, consts, gens, func):
	#TODO check if correct
	analyze(ast.expr, graph, consts, gens, func)
	return None, None

def analyzeAssName(ast, graph, consts, gens, func):
	raise NotImplementedError

def analyzeAssign(ast, graph, consts, gens, func):
	rhs, lbl = analyze(ast.expr, graph, consts, gens, func)
	lhs = ast.nodes[0]
	if isinstance(lhs, Subscript):
		raise NotImplementedError
	else:
		#Connect rhs -> lhs
		addEdge(rhs, lhs.name, graph, lbl)
		#addEdge(lhs.name, rhs, graph, "assign")

def analyzeCallFunc(ast, graph, consts, gens, func):
	node, n_lbl = analyze(ast.node, graph, consts, gens, func)
	for i, arg in enumerate(ast.args):
		arg, lbl = analyze(arg, graph, consts, gens, func)
		addEdge(arg, node, graph, "arg_"+str(i))
	return node, "return"

def analyzeCallRuntime(ast, graph, consts, gens, func):
	#Assumes it is a call to input
	return "$Input", None

def analyzeCompare(ast, graph, consts, gens, func):
	return "$Bool", None

def analyzeOr(ast, graph, consts, gens, func):
	name = gens["or"].inc().name()
	rhs, r_lbl = analyze(ast.nodes[0], graph, consts, gens, func)
	lhs, l_lbl = analyze(ast.nodes[1], graph, consts, gens, func)
	addEdge(rhs, name, graph, r_lbl)
	addEdge(lhs, name, graph, l_lbl)
	return name, None

def analyzeNot(ast, graph, consts, gens, func):
	name = gens["not"].inc().name()
	expr, lbl = analyze(ast.expr, graph, consts, gens, func)
	addEdge(expr, name, graph, lbl)
	return name, None

def analyzeList(ast, graph, consts, gens, func):
	if len(ast.nodes) == 0:
		name = gens["const"].inc().name()
		consts[name] = TList(TNone())
	else:
		name = gens["list"].inc().name()
		for elm in ast.nodes:
			elm, lbl = analyze(elm, graph, consts, gens, func)
			addEdge(elm, name, graph, lbl)
	return name, None

def analyzeDict(ast, graph, consts, gens, func):
	if len(ast.items) == 0:
		name = gens["const"].inc().name()
		consts[name] = TDict(TNone(), TNone())
	else:
		name = gens["dict"].inc().name()
		for k, v in ast.items:
			k, k_lbl = analyze(k, graph, consts, gens, func)
			v, v_lbl = analyze(v, graph, consts, gens, func)
			addEdge(k, name, graph, "key")
			addEdge(v, name, graph, "value")
	return name, None

def analyzeSubscript(ast, graph, consts, gens, func):
	if ast.flags == "OP_ASSIGN":
		raise NotImplementedError
	else:
		name = gens["subR"].inc().name()
		sub, s_lbl = analyze(ast.subs[0], graph, consts, gens, func)
		expr, e_lbl = analyze(ast.expr, graph, consts, gens, func)
		#addEdge(sub, name, graph, "sub")
		addEdge(expr, name, graph, "source")
		return name, None

def analyzeIfExp(ast, graph, consts, gens, func):
	name = gens["or"].inc().name()
	then, t_lbl = analyze(ast.then, graph, consts, gens, func)
	else_, e_lbl = analyze(ast.else_, graph, consts, gens, func)
	addEdge(then, name, graph, t_lbl)
	addEdge(else_, name, graph, e_lbl)
	return name, None

def analyzeIf(ast, graph, consts, gens, func):
	name = gens["or"].inc().name()
	analyze(ast.tests[0][1], graph, consts, gens, func)
	analyze(ast.else_, graph, consts, gens, func)
	return name, None

def analyzeLambda(ast, graph, consts, gens, func):
	print ast
	name = gens["lambda"].inc().name()
	analyze(ast.code, graph, consts, gens, name)
	for i, arg in enumerate(ast.argnames):
		#add an arg edge from every arg to the func type
		addEdge(arg, name, graph, "arg_"+str(i))
	return name, None

def analyzeReturn(ast, graph, consts, gens, func):
	#Add a return edge from this type to the parent function type
	name, lbl = analyze(ast.value, graph, consts, gens, func)
	addEdge(name, func, graph, "up_return")
	return name, None

def analyzeWhile(ast, graph, consts, gens, func):
	return analyze(ast.body, graph, consts, gens, func), None

def analyzeAssAttr(ast, graph, consts, gens, func):
	raise NotImplementedError

def analyzeGetattr(ast, graph, consts, gens, func):
	raise NotImplementedError

#Returns the end node of the chain in the constraint graph
def analyze(ast, graph, consts, gens, func):
	return {
		Stmt:        analyzeStmt,
		Printnl:     analyzePrintnl,
		Const:       analyzeConst,
		UnarySub:    analyzeUnarySub,
		Add:         analyzeAdd,
		Discard:     analyzeDiscard,
		AssName:     analyzeAssName,
		Assign:      analyzeAssign,
		Name:        analyzeName,
		CallFunc:    analyzeCallFunc,
		CallRuntime: analyzeCallRuntime,
		Compare:     analyzeCompare,
		Or:          analyzeOr,
		And:         analyzeOr,
		Not:         analyzeNot,
		List:        analyzeList,
		Dict:        analyzeDict,
		Subscript:   analyzeSubscript,
		IfExp:       analyzeIfExp,
		If:          analyzeIf,
		Lambda:      analyzeLambda,
		Return:      analyzeReturn,
		While:       analyzeWhile,
		#AssAttr:     analyzeAssAttr,
		#Getattr:     analyzeGetattr,
	}[ast.__class__](ast, graph, consts, gens, func)

#Returns a list of tuples: (lambda name, new ast for the lambda)
def runAnalysis(ast):
	#The constraint graph that will need to be solved
	constGraph = {}
	#Name generators for nodes in the graph
	gens = {
			"const":  GenSym("$Const_"),
			"add":    GenSym("$Add_"),
			"neg":    GenSym("$Neg_"),
			"or":     GenSym("$Or_"),
			"not":    GenSym("$Not_"),
			"list":   GenSym("$List_"),
			"dict":   GenSym("$Dict_"),
			"lambda": GenSym("$Lambda_"),
			"subR":   GenSym("$SubR_"),
			"subW":   GenSym("$SubW_")
		   }
	#Mappings from constant names to types
	constTypes = {"$Bool":TBool(),"True":TBool(),"False":TBool(),"$Input":TInt()}
	
	analyze(ast.node, constGraph, constTypes, gens, None)
	print constGraph
	return propagate(constGraph, constTypes)

#Returns whether there any are big types
def anyBig(set):
	for t in set:
		if isinstance(t, TList) or isinstance(t, TDict) or isinstance(t, TFunc):
			return True
	return False

#Returns an array of 5 elements which indicates whether there types were ints, bools, lists, dicts, and/or funcs
def getTypes(s):
	ret = [False, False, False, False, False]
	for t in s:
		if   isinstance(t, TInt):
			ret[0] = True
		elif isinstance(t, TBool):
			ret[1] = True
		elif isinstance(t, TList):
			ret[2] = True
		elif isinstance(t, TDict):
			ret[3] = True
		elif isinstance(t, TFunc):
			ret[4] = True
	return ret

#Returns a set of types that would be returned from all iterable types
#Ex: getValues(set([TDict(TInt, TBool)])) == TBool
def getValues(s):
	ret = set()
	for t in s:
		if isinstance(t, TDict):
			ret.add(t.vtype)
		elif isinstance(t, TList):
			ret.add(t.typ)
	return ret

def getReturns(s):
	ret = set()
	for t in s:
		if isinstance(t, TFunc):
			ret.add(t.ret)
	return ret

def filter(s, type):
	ret = set()
	for t in s:
		if isinstance(t, type):
			ret.add(t)
	return ret

def propagate(graph, consts):
	#Init types dictionary
	types = {}
	for k in graph:
		types[k] = set()
	#Given a variable name, propagate the type of this variable to all neighbor nodes 
	#if the type of this node was updated
	def rec(node, t, label):
		recurse = False
		#Branch on different situations
		if node[:4] == "$Add":
			print "add"
			ints, bools, lists, dicts, funcs = getTypes(t)
			simple = ints + bools
			big = lists + dicts + funcs
			if simple > 0 and big == 0:
				print "some simple, no big"
				#int/bool + ? -> int | ?
				tint = TInt()
				recurse = tint not in types[node]
				types[node].add(tint)
			elif simple == 0 and big > 0:
				print "some big, no simple"
				#Give it TList(TAny) if any non-list bigs are possible
				if dicts + funcs > 0:
					tlist = TList(TAny())
					recurse = tlist not in types[node]
					types[node].add(tlist)
				#Give it all the TList types
				else:
					recurse = not (types[node] >= t)
					types[node] |= t
			else:
				print "both possible"
				#Both are possible, just give up on accuracy
				recurse = not (types[node] >= t)
				types[node] |= t
		elif node[:4] == "$Neg":
			if anyBig(t):
				tany = TAny()
				recurse = tany not in types[node]
				types[node] = tany
			else:
				tint = TInt()
				recurse = tint not in types[node]
				types[node].add(tint)
		elif node[:4] == "$Not":
			print "not"
			tbool = TBool()
			recurse = tbool not in types[node]
			types[node].add(tbool)
		elif node[:5] == "$List":
			print "list"
			t = set([TList(typ) for typ in t])
			recurse = not (types[node] >= t)
			types[node] |= t
		elif node[:5] == "$Dict":
			print "dict"
			if label == "key":
				t = set([TDict(typ, TNone()) for typ in t])
			else:
				t = set([TDict(TNone(), typ) for typ in t])
			recurse = not (types[node] >= t)
			types[node] |= t
		elif node[:5] == "$SubR":
			print "subr"
			if label == "sub":
				#TODO figure out this case
				pass
				#t = set([TIter(type, TNone()) for typ in t])
			else:
				t = getValues(t)
				print "getvalues:",t
				recurse = not (types[node] >= t)
				types[node] |= t
		#Propagates the return type of the function types
		elif label and label == "return":
			print "return label found"
			print t
			t = getReturns(t)
			recurse = not (types[node] >= t)
			types[node] |= t
		#Propagates the current type to the function types
		elif label and label == "up_return":
			print "up_return label found"
			print t
			t = set([TFunc((),typ) for typ in t])
			recurse = not (types[node] >= t)
			types[node] |= t
		#Update only function types
		#elif label and label == "assign":
		#	print "assign label found"
		#	print t
		#	#TODO check if this is sound
		#	t = filter(t, TFunc)
		#	recurse = not (types[node] >= t)
		#	types[node] |= t
		elif label and label[:3] == "arg":
			print "arg label"
			pos = int(label[4:])
			t = set([TFunc((TNone(),)*pos + (typ,), TNone()) for typ in t])
			recurse = not (types[node] >= t)
			types[node] |= t
		#Simply add the types
		elif t != types[node]:
			debug = False
			if debug:			
				print "simple case"
				print t
			recurse = not (types[node] >= t)
			types[node] |= t
		
		print "types: ",types,"\n"
		if recurse:
			#print "\nrecursing: ",types,"\n"
			#print node
			for name, label in graph[node]:
				#print "recursing on ",name, label, types
				rec(name, types[node], label)
				
	print consts
	print "types: ",types
	for constName in consts:
		#print "constName:", constName," ",consts[constName]
		#For each constant, recurse on its only neighbor
		types[constName] = set([consts[constName]])
		#check if const is actually used
		if constName in graph:
			for neighbor in graph[constName]:
				rec(neighbor[0], set([consts[constName]]), neighbor[1])
	return types

#Simplifies a set of types recursively
#Returns an array
def simplify(s):
	#print s
	ret = []
	maxArgs = 0
	retTFuncArgs = []
	retTFuncRet = []
	retTList = []
	retTDictKey = []
	retTDictVal = []
	for t in s:
		if   isinstance(t, TInt):
			ret.append(t)
		elif isinstance(t, TBool):
			ret.append(t)
		elif isinstance(t, TList):
			retTList.append(t.typ)
		elif isinstance(t, TDict):
			retTDictKey.append(t.ktyp)
			retTDictVal.append(t.vtyp)
		elif isinstance(t, TFunc):
			funcArgs = len(t.args)
			if funcArgs > maxArgs:
				#print "increasing maxArgs"
				retTFuncArgs.extend([[] for i in range(funcArgs - maxArgs)])
				maxArgs = funcArgs
			for i, arg in enumerate(t.args):
				retTFuncArgs[i].append(arg)
			#print retTFuncArgs
			retTFuncRet.append(t.ret)
	
	if retTList:
		retTList = simplify(retTList)
		ret.append(TList(retTList))
	
	if retTDictKey:
		retTDictKey = simplify(retTDictKey)
	else:
		retTDictKey = TNone()
	if retTDictVal:
		retTDictVal = simplify(retTDictVal)
	else:
		retTDictVal = TNone()
	if not isinstance(retTDictKey, TNone) and not isinstance(retTDictVal, TNone):
		ret.append(TDict(retTDictKey, retTDictVal))
	
	#print "retTFuncArgs:",retTFuncArgs
	retTFuncArgs = [(simplify(arg) if arg else TNone()) for arg in retTFuncArgs ]
	if retTFuncRet:
		retTFuncRet = simplify(retTFuncRet)
	else:
		retTFuncRet = TNone()
	if retTFuncArgs:
		ret.append(TFunc(retTFuncArgs, retTFuncRet))
	#if retTFuncArgs
	# retTDictKey = simplify(retTDictKey)
	# retTDictVal = simplify(retTDictVal)
	#print "returning:",ret
	return ret

def printReport(types, names, lines, filter):
	print "Report:"
	sys.stdout.write("Variable Name".ljust(20)+"Line".ljust(10)+"Types\n")
	sys.stdout.write("-"*60+"\n")
	for name, typeList in types.iteritems():
		if filter and name[0] == "$":
			continue
		line = str(lines[name]) if name in lines else ""
		name = names[name] if name in names else name
		
		types = simplify(typeList)
		
		sys.stdout.write(name.ljust(20)+line.ljust(10))
		if types:
			sys.stdout.write(str(types)+"\n")
		else:
			sys.stdout.write("\n")
	sys.stdout.flush()


##Type Check Step

def tcModule(ast,type_dict,assert_dict):
	new_node, assert_dist = type_check(ast.node, type_dict,assert_dict)
	ast.node = new_node

def tcStmt(ast, type_dict, assert_dict):
	new_assert_dict = assert_dict
	new_body = []
	for n in ast.nodes:
		new_expr, new_assert_dict = type_check(n,type_dict,new_assert_dict)
		new_body += new_expr
	return Stmt(new_body), new_assert_dict	

	
def tcAssign(ast, type_dict, assert_dict):
	anno_tag = ast.nodes[0].flags[2]
	name = ast.nodes[0].name
	#print "Annotation Tag:", anno_tag
	if anno_tag != 'NONE':
		assert_dict[name] = anno_tag
	new_ast = [ast]
	if name in assert_dict:
		type_array = getTypes(type_dict[name])
		type_mapping = {"INT" : 0, "BOOL" : 1, "LIST" : 2, "DICT" : 3, "FUNC" : 4}
		if (type_array[type_mapping[assert_dict[name]]] == False):
			raise TypeError
		
		possible_type_count = 0
		for type_val in type_array:
			if type_val == True:
				possible_type_count += 1
		if (possible_type_count > 1):
			#ADD RUNTIME NODE
			#Arguments: The py_object, Anno_Tag, the linenumber
			runtime_node = CallRuntime(Name("assert_type"),[Name(name),Name(assert_dict[name]),Const(ast.nodes[0].flags[1])])
			new_ast = [ast,runtime_node]

	return new_ast, assert_dict
	
def tcWhile(ast,type_dict,assert_dict):
	return type_check(ast.body, type_dict,assert_dict)

def tcIf(ast, type_dict, assert_dict):
	if_ast, if_ass_dict = type_check(ast.tests[0][1], type_dict, assert_dict)
	else_ast, else_ass_dict = type_check(ast.else_, type_dict, assert_dict)
	new_ast = IfExp(
		heapify(ast.test, names),
		heapify(ast.then, names),
		heapify(ast.else_, names)
	)
	return [new_ast], if_ass_dict + else_ass_dict

def tcLambda(ast, type_dict, assert_dict):
	#I didn't see this in the analysis
	return NotImplementedError

def tcPass(ast, type_dict, assert_dict):
	return [ast], assert_dict
	
	
def type_check(ast, type_dict, assert_dict):
	return {
		Module:      tcModule,
		Stmt:        tcStmt,
		Printnl:     tcPass,
		Const:       tcPass,
		UnarySub:    tcPass,
		Add:         tcPass,
		Discard:     tcPass,
		AssName:     tcPass,
		Assign:      tcAssign,
		Name:        tcPass,
		CallFunc:    tcPass,
		CallRuntime: tcPass,
		Compare:     tcPass,
		Or:          tcPass,
		And:         tcPass,
		Not:         tcPass,
		List:        tcPass,
		Dict:        tcPass,
		Subscript:   tcPass,
		IfExp:       tcPass,
		If:          tcIf,
		Lambda:      tcPass,
		Return:      tcPass,
		While:       tcWhile,
		#AssAttr:     analyzeAssAttr,
		#Getattr:     analyzeGetattr,
	}[ast.__class__](ast, type_dict, assert_dict)

	

