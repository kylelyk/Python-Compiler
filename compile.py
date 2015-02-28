import compiler, sys, re, astpp, os
from compiler.ast import *
import flattener
import colorGraph
import explicate
from x86AST import *

debug = True
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
	def get(self):
		return str(self.n)
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
	#print "prev was:",prev
	if isinstance(prev, tuple):
		s = set(prev[0])
	else:
		s = set(prev)
	s.discard(instr.reg2)
	condAdd(s, instr.reg1)
	#movl does not read reg2 but addl/subl do
	if not isinstance(instr, Movl):
		condAdd(s, instr.reg2)
	return s

def liveIf(instr, prev):
	liveThen = set(prev if prev else [])
	liveElse = set(prev if prev else [])
	#print "live set before then",liveThen
	#print "live set before else",liveElse
	instr.liveThen = liveness(instr.thenAssign, prev)
	instr.liveElse = liveness(instr.elseAssign, prev)
	#print "assign then:",instr.thenAssign
	#print "assign else:",instr.elseAssign
	#print "live then:",instr.liveThen
	#print "live else:",instr.liveElse
	return instr.liveThen[0] | instr.liveElse[0]

#takes in a set of instructions and a set of live variables after the set of instructions
def liveness(asm, live=set([])):
	#print "getting liveliness of:"
	#for instr in asm:
	#	print instr
	#print ""
	live_after = [0]*len(asm)
	l = len(live_after) - 1
	#live_after[l] = live
	#print "live passed in:",live
	#print "initialization:",live_after
	for index, instr in enumerate(reversed(asm)):
		#print "live_after:",live_after
		bases = instr.__class__.__bases__
		prev = live_after[l-index] if index != 0 else live
		if len(bases):
			#print "passing set:",prev
			#print "analysis on:",instr
			#compute the liveness of the instruction if it actually does anything to variables
			#instructions that do not inherit from OneArg, TwoArgs, or Node (If) are not considered
			#and the result is copied from the previous iteration
			live_after[l-index-1] = {
				OneArg:  liveOneArg,
				TwoArgs: liveTwoArgs,
				Node:    liveIf
				}[bases[0]](instr, prev)
		else:
			#print "ignoring analysis on:",instr
			#print "prev:",prev
			live_after[l-index-1] = prev
	#print "returning:",live_after
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

def interfereNegPop(instr, liveSet, graph):
	addNode(instr.reg, graph)
	t = instr.reg
	for v in liveSet:
		if v != t:
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereMov(instr, liveSet, graph):
	s = instr.reg1
	t = instr.reg2
	addNode(s, graph)
	addNode(t, graph)
	for v in liveSet:
		if v != t and v != s:
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereTwoArg(instr, liveSet, graph):
	s = instr.reg1
	t = instr.reg2
	addNode(s, graph)
	addNode(t, graph)
	for v in liveSet:
		if v != t:
			#print "adding edge",v,"to",t
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereCall(instr, liveSet, graph):
	for v in liveSet:
		addEdge("%eax", v, graph)
		addEdge("%ecx", v, graph)
		addEdge("%edx", v, graph)
		addEdge(v, "%eax", graph)
		addEdge(v, "%ecx", graph)
		addEdge(v, "%edx", graph)

def interfereIfStmt(instr, liveSet, graph):
	#print "in interfereIfStmt"
	#print instr
	print "liveset in interfereIfStmt:",liveSet
	t = instr.test.name
	#for v in liveSet[0]:
	#	if v != t:
	#		addEdge(t, v, graph)
	#		addEdge(v, t, graph)
	print "instr.liveThen",instr.liveThen
	print "instr.liveElse",instr.liveElse
	interfere(instr.thenAssign, instr.liveThen, graph)
	interfere(instr.elseAssign, instr.liveElse, graph)

def interfere(asm, liveness, graph):
	print "interference was called with liveness:",liveness
	interferePass = lambda i,l,g: None
	for index, instr in enumerate(asm):
		#print instr,instr.__class__
		#liveSet = liveness[index][0] if isinstance(liveness[index], tuple) else liveness[index]
		#print "
		{
			Pushl:   interferePass,
			Popl:    interfereNegPop,
			Negl:    interfereNegPop,
			Movl:    interfereMov,
			Addl:    interfereTwoArg,
			Subl:    interfereTwoArg,
			Orl:     interfereTwoArg,
			Andl:    interfereTwoArg,
			Cmpl:    interfereTwoArg,
			Call:    interfereCall,
			Leave:   interferePass,
			Ret:     interferePass,
			Newline: interferePass,
			IfStmt:   interfereIfStmt
		}[instr.__class__](instr, liveness[index], graph)
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
			elif isinstance(instr, IfStmt):
				thenSpilled, spill1 = spillCode(instr.thenAssign, graph, colors, gen)
				elseSpilled, spill2 = spillCode(instr.thenAssign, graph, colors, gen)
				spilled = spilled or spill1 or spill2
				newasm.append(IfStmt(
					instr.cond,
					elseSpilled,
					thenSpilled,
					spillCode(instr.elseAssign, graph, colors, gen),
					instr.liveThen,
					instr.liveElse
				))
			else:
				newasm.append(instr)
		else:
			newasm.append(instr)
	return newasm, spilled

def removeIf(asm, gen):
	newasm = []
	for instr in asm:
		if isinstance(instr, IfStmt):
			labelName1 = "elselbl_" + gen.inc().get()
			labelName2 = "endlbl_" + gen.get()
			newasm.append(Jne(labelName1))
			newasm.extend(removeIf(instr.thenAssign, gen))
			newasm.append(Jmp(labelName2))
			newasm.append(Label(labelName1))
			newasm.extend(removeIf(instr.elseAssign, gen))
			newasm.append(Label(labelName2))
		else:
			newasm.append(instr)
	return newasm

def locOneArg(instr, color):
	if instr.reg and instr.reg != "%esp" and instr.reg != "%ebp":
		if instr.reg in color:
			loc = color[instr.reg]
		else:
			print instr
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

def addDataSection():
	return '''.data
negError:
.asciz "Attempt to negate a non basic type.\n"
addError:
.asciz "Attempt to add a basic type to a non basic type.\n"
debugMsg1:
.asciz "Debug Message 1.\n"
debugMsg2:
.asciz "Debug Message 2.\n"
.text\n'''

def compile(ast):
	gen = GenSym()
	map = {}
	state = ()
	explicate.explicate(ast, gen)
	#print "explicated ast:"
	astpp.printAst(ast)
	newast = flattener.flatten(ast, None, gen, map)
	print "flattened ast:"
	astpp.printAst(newast)
	asm = []
	asm.append(Pushl(reg="%ebp"))
	asm.append(Movl(reg1="%esp", reg2="%ebp"))
	allocStmt = Subl(const1=0, reg2="%esp")
	asm.append(allocStmt)
	asm.append(Newline())
	asm.append(Movl(const1=0b001, reg2="False"))
	asm.append(Movl(const1=0b101, reg2="True"))
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
		print "liveness:",l
		g = interfere(asm, l, {})
		#printd("interfernce:\n"+str(g))
		colors = colorGraph.color_graph(g)
		printd("colors:\n"+str(colors))
		asm, cont = spillCode(asm, g, colors, gen)
	
	asm = removeIf(asm, GenSym())
	assignLocations(asm, colors)
	#printd("If's removed asm:")
	#for instr in asm:
	#	printd(instr)
	#return
	space = max(0, max(colors.values())-9)*4
	allocStmt.const1 = space
	asm = optimizePass1(asm)
	
	printd("\n\nfinal asm")
	for instr in asm:
		printd(instr)
	
	f = open(re.split("\.[^\.]*$", sys.argv[1])[0]+".s", "w")
	f.write(addDataSection())
	f.write(".globl main\nmain:\n")
	for instr in asm:
		f.write(str(instr)+"\n")
	
	f.close()

if len(sys.argv) != 2:
	print "Name of file is required"
	sys.exit(1)

ast = compiler.parseFile(sys.argv[1])
compile(ast)
