import compiler, sys, re, astpp, os
from compiler.ast import *
import flattener
from x86AST import *


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

def condAdd(set, elm):
	if elm is not None and elm[0] != "%":
		set.add(elm)

def liveOneArg(instr, prev):
	s = set([])
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
			#print l-index, instr, live_after[l - index]

def addEdge(u, v, graph):
	if u in graph:
		graph[u].add(v)
	else:
		graph[u] = set([v])

def interfereNegPop(instr, index, liveness, graph):
	t = instr.reg
	for v in liveness[index]:
		if v != t:
			addEdge(t, v, graph)

def interfereMov(instr, index, liveness, graph):
	s = instr.reg1
	t = instr.reg2
	for v in liveness[index]:
		if v != t and v != s:
			addEdge(t, v, graph)

def interfereAddSub(instr, index, liveness, graph):
	s = instr.reg1
	t = instr.reg2
	for v in liveness[index]:
		if v != t and v != s:
			addEdge(t, v, graph)

def interfereCall(instr, index, liveness, graph):
	for v in liveness[index]:
		addEdge("%eax", v, graph)
		addEdge("%ecx", v, graph)
		addEdge("%edx", v, graph)

def interfere(asm, liveness):
	interferePass = lambda(i,n,l,g): pass
	graph = {}
	for index, instr in enumerate(asm):
		{
			Pushl:   interferePass
			Popl:    interfereNegPop
			Negl:    interfereNegPop
			Movl:    interfereMov
			Addl:    interfereAddSub
			Subl:    interfereAddSub
			Call:    interfereCall
			Leave:   interferePass
			Ret:     interferePass
			Newline: interferePass
		}[bases[0]](instr, index, liveness, graph)


def compile(ast):
	gen = GenSym()
	map = {}
	state = ()
	newast = flattener.flatten(ast, None, gen, map)
	astpp.printAst(newast)
	asm = [
		Movl(const1=4,reg2="z"),
		Movl(const1=0,reg2="w"),
		Movl(const1=1,reg2="z"),
		Movl(reg1="w",reg2="x"),
		Addl(reg1="z",reg2="x"),
		Movl(reg1="w",reg2="y"),
		Addl(reg1="x",reg2="y"),
		Movl(reg1="y",reg2="w"),
		Addl(reg1="x",reg2="w"),
		]
	'''asm.append(Pushl(reg="%ebp"))
	asm.append(Movl(reg1="%esp", reg2="%ebp"))
	asm.append(Subl(const1=len(map)*4, reg2="%esp"))
	#asm.append(Newline())
	pyToAsm(newast, None, asm, map)
	asm.append(Movl(const1=0, reg2="%eax"))
	asm.append(Leave())
	asm.append(Ret())'''
	#for instr in asm:
	#	print instr
	liveness(asm)
	return
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
