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

class TNone:
	def __class__(self):
		return TNone
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TNone"

class TInt:
	def __class__(self):
		return TInt
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TInt"

class TBool:
	def __class__(self):
		return TBool
	def __eq__(self, other):
		return other.__class__ == self.__class__
	def __hash__(self):
		return hash(self.__class__)
	def __str__(self):
		return "TBool"

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

def analyzeStmt(ast, graph, consts, gens):
	for n in ast.nodes:
		analyze(n, graph, consts, gens)

def analyzePrintnl(ast, graph, consts, gens):
	return None, None

def analyzeConst(ast, graph, consts, gens):
	name = gens["const"].inc().name()
	consts[name] = TInt()
	return name, None

def analyzeName(ast, graph, consts, gens):
	return ast.name, None

def analyzeUnarySub(ast, graph, consts, gens):
	name = gens["neg"].inc().name()
	expr, lbl = analyze(ast.expr, graph, consts, gens)
	addEdge(expr, name, graph, lbl)
	return name, None

def analyzeAdd(ast, graph, consts, gens):
	rhs, r_lbl = analyze(ast.right, graph, consts, gens)
	lhs, l_lbl = analyze(ast.left,  graph, consts, gens)
	name = gens["add"].inc().name()
	addEdge(rhs, name, graph, r_lbl)
	addEdge(lhs, name, graph, l_lbl)
	return name, None

def analyzeDiscard(ast, graph, consts, gens):
	#TODO check if correct
	analyze(ast.expr, graph, consts, gens)
	return None, None

def analyzeAssName(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeAssign(ast, graph, consts, gens):
	rhs, lbl = analyze(ast.expr, graph, consts, gens)
	lhs = ast.nodes[0]
	if isinstance(lhs, Subscript):
		raise NotImplementedError
	else:
		#Connect rhs -> lhs
		addEdge(rhs, lhs.name, graph, lbl)

def analyzeCallFunc(ast, graph, consts, gens):
	node, n_lbl = analyze(ast.node, graph, consts, gens)
	for i, arg in enumerate(ast.args):
		arg, lbl = analyze(arg, graph, consts, gens)
		addEdge(arg, node, graph, "arg_"+str(i))
	return node, "return"

def analyzeCallRuntime(ast, graph, consts, gens):
	#Assumes it is a call to input
	return "$Input", None

def analyzeCompare(ast, graph, consts, gens):
	return "$Bool", None

def analyzeOr(ast, graph, consts, gens):
	name = gens["or"].inc().name()
	rhs, r_lbl = analyze(ast.nodes[0], graph, consts, gens)
	lhs, l_lbl = analyze(ast.nodes[1], graph, consts, gens)
	addEdge(rhs, name, graph, r_lbl)
	addEdge(lhs, name, graph, l_lbl)
	return name, None

def analyzeNot(ast, graph, consts, gens):
	name = gens["not"].inc().name()
	expr, lbl = analyze(ast.expr, graph, consts, gens)
	addEdge(expr, name, graph, lbl)
	return name, None

def analyzeList(ast, graph, consts, gens):
	if len(ast.nodes) == 0:
		name = gens["const"].inc().name()
		consts[name] = TList(TNone())
	else:
		name = gens["list"].inc().name()
		for elm in ast.nodes:
			elm, lbl = analyze(elm, graph, consts, gens)
			addEdge(elm, name, graph, lbl)
	return name, None

def analyzeDict(ast, graph, consts, gens):
	if len(ast.items) == 0:
		name = gens["const"].inc().name()
		consts[name] = TDict(TNone(), TNone())
	else:
		name = gens["dict"].inc().name()
		for k, v in ast.items:
			k, k_lbl = analyze(k, graph, consts, gens)
			v, v_lbl = analyze(v, graph, consts, gens)
			addEdge(k, name, graph, k_lbl)
			addEdge(v, name, graph, v_lbl)
	return name, None

def analyzeSubscript(ast, graph, consts, gens):
	if ast.flags == "OP_ASSIGN":
		raise NotImplementedError
	else:
		name = gens["subR"].inc().name()
		sub, s_lbl = analyze(ast.subs[0], graph, consts, gens)
		expr, e_lbl = analyze(ast.expr, graph, consts, gens)
		#addEdge(sub, name, graph, "sub")
		addEdge(expr, name, graph, "source")
		return name, None

def analyzeIfExp(ast, graph, consts, gens):
	name = gens["or"].inc().name()
	then, t_lbl = analyze(ast.then, graph, consts, gens)
	else_, e_lbl = analyze(ast.else_, graph, consts, gens)
	addEdge(then, name, graph, t_lbl)
	addEdge(else_, name, graph, e_lbl)
	return name, None

def analyzeIf(ast, graph, consts, gens):
	name = gens["or"].inc().name()
	analyze(ast.tests[0][1], graph, consts, gens)
	analyze(ast.else_, graph, consts, gens)
	return name, None

def analyzeLambda(ast, graph, consts, gens):
	print ast
	name = gens["lambda"].inc().name()
	
	return

def analyzeReturn(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeWhile(ast, graph, consts, gens):
	return analyze(ast.body, graph, consts, gens), None

def analyzeAssAttr(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeGetattr(ast, graph, consts, gens):
	raise NotImplementedError

#Returns the end node of the chain in the constraint graph
def analyze(ast, graph, consts, gens):
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
	}[ast.__class__](ast, graph, consts, gens)

#Returns a list of tuples: (lambda name, new ast for the lambda)
def runAnalysis(ast):
	#The constraint graph that will need to be solved
	constGraph = {}
	#Name generators for nodes in the graph
	gens = {
			"const": GenSym("$Const_"),
			"add":   GenSym("$Add_"),
			"neg":   GenSym("$Neg_"),
			"or":    GenSym("$Or_"),
			"not":   GenSym("$Not_"),
			"list":  GenSym("$List_"),
			"dict":  GenSym("$Dict_"),
			"subR":  GenSym("$SubR_"),
			"subW":  GenSym("$SubW_")
		   }
	#Mappings from constant names to types
	constTypes = {"$Bool":TBool(),"True":TBool(),"False":TBool(),"$Input":TInt()}
	
	analyze(ast.node, constGraph, constTypes, gens)
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

def filter(set, type):
	ret = set()
	for t in set:
		if isinstance(t, type):
			ret.add(t)
	return ret

def propagate(graph, consts):
	# print TInt() == TInt()
	# print TFunc([TInt()],TInt()) == TFunc([TInt()],TInt())
	# raise NotImplementedError


	#Init types dictionary
	types = {}
	for k in graph:
		types[k] = set()
	#Given a variable name, propagate the type of this variable to all neighbor nodes 
	#if the type of this node was updated
	def rec(node, t, label):
		recurse = False
		#Node is special so do special operations
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
		elif label and label == "return":
			print "return label"
			t = getReturns(t)
			recurse = not (types[node] >= t)
			types[node] |= t
		elif label and label[:3] == "arg":
			print "arg label"
			pos = int(label[4:])
			t = set([TFunc((TNone(),)*pos + (typ,), TNone()) for typ in t])
			recurse = not (types[node] >= t)
			types[node] |= t
		#Simply add the types
		elif t != types[node]:
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
	
def printReport(types, names, lines, filter):
	names = {v: k for k, v in names.items()}
	sys.stdout.write("Variable Name".ljust(20)+"Line".ljust(10)+"Types\n")
	sys.stdout.write("-"*60+"\n")
	for name, typeList in types.iteritems():
		if filter and name[0] == "$":
			continue
		line = str(lines[name]) if name in lines else ""
		name = names[name] if name in names else name
		
		sys.stdout.write(name.ljust(20)+line.ljust(10))
		if len(typeList) == 1:
			sys.stdout.write(str(typeList.pop())+"\n")
		elif len(typeList) > 1:
			sys.stdout.write("[ ")
			for i, t in enumerate(typeList):
				sys.stdout.write(str(t))
				if i < len(typeList) - 1:
					sys.stdout.write(", ")
			sys.stdout.write(" ]\n")
		else:
			sys.stdout.write("\n")
	sys.stdout.flush()
