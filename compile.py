import compiler, sys, re, astpp, os
from compiler.ast import *
import flattener
import colorGraph
from x86AST import *

debug = False
def printd(str):
	if debug:
		print str

class GenSym:
	def __init__(self):
		self.n = 0
	def inc(self):
		self.n += 1
		return self
	def name(self):
		return "__$tmp" + str(self.n)
	def invalidName(self):
		return "__$tmp_invalid"

#maps the values of colorgraph to the actual register names
reg_map = {0:"%eax", 1:"%ecx", 2:"%edx", 3:"%ebx", 4:"%esi", 5:"%edi", 6:"%esp", 7:"%ebp"}

def condAdd(set, elm):
	if elm is not None and elm[0] != "%":
		set.add(elm)

def liveOneArg(instr, prev):
	s = set(prev)
	#All instructions read from the var but negl and pushl writes to the var
	if not isinstance(instr, Pushl):
		s.discard(instr.reg)
	condAdd(s, instr.reg)
	return s

def liveTwoArgs(instr, prev):
	s = set(prev)
	s.discard(instr.reg2)
	condAdd(s, instr.reg1)
	#movl does not read reg2 but addl/subl do
	if not isinstance(instr, Movl):
		condAdd(s, instr.reg2)
	return s

def liveness(asm):
	live_after = [set([])]*len(asm)
	l = len(live_after) - 1
	for index, instr in enumerate(reversed(asm)):
		bases = instr.__class__.__bases__
		if index != l:
			#compute the liveness of the instruction if it actually does anything to variables
			#instructions that do not inherit from OneArg or TwoArgs are not considered
			#and the result is copied from the previous iteration
			live_after[l-index-1] = {
				OneArg:  liveOneArg,
				TwoArgs: liveTwoArgs,
				}[bases[0]](instr, live_after[l-index]) if len(bases) else live_after[l-index]
	return live_after

def addEdge(u, v, graph):
	if u in graph:
		graph[u][0].add(v)
	else:
		graph[u] = (set([v]), False)

#guarantees node exists in graph (assuming not %esp, or %ebp)
def addNode(reg, graph):
	if reg and not reg in graph and reg != "%esp" and reg != "%ebp":
		graph[reg] = (set(), False)

def interfereNegPop(instr, index, liveness, graph):
	addNode(instr.reg, graph)
	t = instr.reg
	for v in liveness[index]:
		if v != t:
			addEdge(t, v, graph)

def interfereMov(instr, index, liveness, graph):
	s = instr.reg1
	t = instr.reg2
	addNode(s, graph)
	addNode(t, graph)
	for v in liveness[index]:
		if v != t and v != s:
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereAddSub(instr, index, liveness, graph):
	s = instr.reg1
	t = instr.reg2
	addNode(s, graph)
	addNode(t, graph)
	for v in liveness[index]:
		if v != t:
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereCall(instr, index, liveness, graph):
	for v in liveness[index]:
		addEdge("%eax", v, graph)
		addEdge("%ecx", v, graph)
		addEdge("%edx", v, graph)
		addEdge(v, "%eax", graph)
		addEdge(v, "%ecx", graph)
		addEdge(v, "%edx", graph)

def interfere(asm, liveness):
	interferePass = lambda i,n,l,g: None
	graph = {}
	for index, instr in enumerate(asm):
		{
			Pushl:   interferePass,
			Popl:    interfereNegPop,
			Negl:    interfereNegPop,
			Movl:    interfereMov,
			Addl:    interfereAddSub,
			Subl:    interfereAddSub,
			Call:    interfereCall,
			Leave:   interferePass,
			Ret:     interferePass,
			Newline: interferePass
		}[instr.__class__](instr, index, liveness, graph)
	return graph

def spillCode(asm, graph, colors, gen):
	spilled = False
	newasm = []
	for index, instr in enumerate(asm):
		bases = instr.__class__.__bases__
		if len(bases) and bases[0] == TwoArgs:
			#Check if variables are on stack
			if instr.reg1 and instr.reg1 in colors and colors[instr.reg1] > 5 and instr.reg2 and instr.reg2 in colors and colors[instr.reg2] > 5:
				spilled = True
				spilledvar = gen.inc().name()
				newasm.append(Movl(reg1=instr.reg1,reg2=spilledvar))
				newasm.append(instr.__class__(reg1=spilledvar,reg2=instr.reg2))
			else:
				newasm.append(instr)
		else:
			newasm.append(instr)
	return newasm, spilled

def locOneArg(instr, color):
	if instr.reg and instr.reg != "%esp" and instr.reg != "%ebp":
		if instr.reg in color:
			loc = color[instr.reg]
		else:
			loc= colorGraph.reg_color[instr.reg]
		if loc > 5:
			instr.reg = "%ebp"
			instr.offset = -(loc-10+1)*4
		else:
			instr.reg = reg_map[loc]

def locTwoArgs(instr, color):
	if instr.reg1 and instr.reg1 != "%esp" and instr.reg1 != "%ebp":
		if instr.reg1 in color:
			loc = color[instr.reg1]
		else:
			loc= colorGraph.reg_color[instr.reg1]
		if loc > 5:
			instr.reg1 = "%ebp"
			instr.offset1 = -(loc-10+1)*4
		else:
			instr.reg1 = reg_map[loc]
	if instr.reg2 and instr.reg2 != "%esp" and instr.reg2 != "%ebp":
		if instr.reg2 in color:
			loc = color[instr.reg2]
		else:
			loc= colorGraph.reg_color[instr.reg2]
		if loc > 5:
			instr.reg2 = "%ebp"
			instr.offset2 = -(loc-10+1)*4
		else:
			instr.reg2 = reg_map[loc]


def assignLocations(asm, color):
	for instr in asm:
		bases = instr.__class__.__bases__
		if len(bases):
			{
				OneArg:  locOneArg,
				TwoArgs: locTwoArgs,
			}[bases[0]](instr, color)

#removes moves between the same registers
def optimizePass1(asm):
	newasm = []
	for instr in asm:
		if instr.__class__ != Movl or not (instr.reg1 and instr.reg2 and instr.reg1 == instr.reg2):
			newasm.append(instr)
	return newasm

def compile(ast):
	gen = GenSym()
	map = {}
	state = ()
	newast = flattener.flatten(ast, None, gen, map)
	#astpp.printAst(newast)
	asm = []
	asm.append(Pushl(reg="%ebp"))
	asm.append(Movl(reg1="%esp", reg2="%ebp"))
	allocStmt = Subl(const1=0, reg2="%esp")
	asm.append(allocStmt)
	asm.append(Newline())
	pyToAsm(newast, None, asm, map)
	asm.append(Newline())
	asm.append(Movl(const1=0, reg2="%eax"))
	asm.append(Leave())
	asm.append(Ret())
	
	printd("psuedo asm:")
	for instr in asm:
		printd(instr)
	
	cont = True
	maxiter = 4
	iter = 0
	while cont and iter != maxiter:
		iter += 1
		l = liveness(asm)
		g = interfere(asm, l)
		colors = colorGraph.color_graph(g)
		asm, cont = spillCode(asm, g, colors, gen)
	
	assignLocations(asm, colors)
	space = max(0, max(colors.values())-9)*4
	allocStmt.const1 = space
	
	asm = optimizePass1(asm)
	
	printd("final asm")
	for instr in asm:
		printd(instr)
	
	f = open(re.split("\.[^\.]*$", sys.argv[1])[0]+".s", "w")
	f.write(".globl main\nmain:\n")
	for instr in asm:
		f.write(str(instr)+"\n")
	
	f.close()

if len(sys.argv) != 2:
	print "Name of file is required"
	sys.exit(1)

ast = compiler.parseFile(sys.argv[1])
compile(ast)
