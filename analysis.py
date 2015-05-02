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
	raise NotImplementedError

def analyzeConst(ast, graph, consts, gens):
	name = gens["const"].inc().name()
	consts[name] = TInt()
	return name

def analyzeName(ast, graph, consts, gens):
	return ast.name

def analyzeUnarySub(ast, graph, consts, gens):
	name = gens["sub"].inc().name()
	addEdge(analyze(ast.expr, graph, consts, gens), name, graph)
	return name

def analyzeAdd(ast, graph, consts, gens):
	rhs = analyze(ast.right, graph, consts, gens)
	lhs = analyze(ast.left,  graph, consts, gens)
	addNode = gens["add"].inc().name()
	addEdge(rhs, addNode, graph)
	addEdge(lhs, addNode, graph)
	return addNode

def analyzeDiscard(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeAssName(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeAssign(ast, graph, consts, gens):
	rhs = analyze(ast.expr, graph, consts, gens)
	lhs = ast.nodes[0]
	if isinstance(lhs, Subscript):
		raise NotImplementedError
	else:
		#Connect rhs -> lhs
		addEdge(rhs, lhs.name, graph)

def analyzeCallFunc(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeCallRuntime(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeCompare(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeOr(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeAnd(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeBitxor(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeNot(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeList(ast, graph, consts, gens):
	if len(ast.nodes) == 0:
		name = gens["const"].inc().name()
		consts[name] = TList(TNone())
		return name
	else:
		name = gens["list"].inc().name()
		for elm in ast.nodes:
			addEdge(analyze(elm, graph, consts, gens), name, graph)
		return name

def analyzeDict(ast, graph, consts, gens):
	if len(ast.items) == 0:
		name = gens["const"].inc().name()
		consts[name] = TDict(TNone(), TNone())
		return name
	else:
		raise NotImplementedError

def analyzeSubscript(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeIfExp(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeLambda(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeReturn(ast, graph, consts, gens):
	raise NotImplementedError

def analyzeWhile(ast, graph, consts, gens):
	raise NotImplementedError

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
		And:         analyzeAnd,
		Bitxor:      analyzeBitxor,
		Not:         analyzeNot,
		List:        analyzeList,
		Dict:        analyzeDict,
		Subscript:   analyzeSubscript,
		IfExp:       analyzeIfExp,
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
			"sub":   GenSym("$Sub_"),
			"list":  GenSym("$List_")
		   }
	#Mappings from constant names to types
	constTypes = {"True":TBool(),"False":TBool()}
	
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
def getTypes(set):
	ret = [False, False, False, False, False]
	for t in set:
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
		if node[0] == "$":
			if node[:4] == "$Add":
				ints, bools, lists, dicts, funcs = getTypes(t)
				simple = ints + bools
				big = lists + dicts + funcs
				if simple > 0 and big == 0:
					print "some simple, no big"
					#int/bool + ? -> int | ?
					tint = TInt()
					recurse = tint in types[node]
					types[node].add(tint)
				elif simple == 0 and big > 0:
					print "some big, no simple"
					#Give it TList(TAny) if any non-list bigs are possible
					if dicts + funcs > 0:
						tlist = TList(TAny())
						recurse = tlist in types[node]
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
			elif node[:4] == "$Sub":
				if anyBig(t):
					tany = TAny()
					recurse = tany in types[node]
					types[node] = tany
				else:
					tint = TInt()
					recurse = tint in types[node]
					types[node].add(tint)
			elif node[:5] == "$List":
				t = set([TList(typ) for typ in t])
				recurse = not (types[node] >= t)
				types[node] |= t
		#Simply add the types
		elif t != types[node]:
			recurse = not (types[node] >= t)
			types[node] |= t
		
		if recurse:
			print "recursing"
			print node
			for name, label in graph[node]:
				print name, label
				rec(name, types[node], label)
				
	print consts
	for constName in consts:
		#print "constName:", constName," ",consts[constName]
		#For each constant, recurse on its only neighbor
		types[constName] = set([consts[constName]])
		#check if const is actually used
		if constName in graph:
			for neighbor in graph[constName]:
				rec(neighbor[0], set([consts[constName]]), neighbor[1])
	return types
	
def printReport(types):
	sys.stdout.write("Variable Name".ljust(20)+"Line".ljust(10)+"Types\n")
	for name, typeList in types.iteritems():
		sys.stdout.write(name.ljust(20)+"".ljust(10))
		if len(typeList) == 1:
			sys.stdout.write(str(typeList.pop())+"\n")
			#print
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