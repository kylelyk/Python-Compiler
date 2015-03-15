import compiler, sys, re, astpp, os
from compiler.ast import *
from x86AST import *
import explicate
import flattener
import liveness
import interference
import colorGraph

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
	def get(self):
		return str(self.n)
	def invalidName(self):
		return "__$tmp_invalid"
		
#Stuff for uniquify, generates unique renames (in spirit of GenSym)		
class GenName:
	def __init__(self):
		self.n = 0
	def inc(self):
		self.n += 1
		return self
	def new_name(self, name):
		self.inc()
		return name + "_" + str(self.n)

gen_n = GenName()

def spillCode(asm, graph, colors, gen):
	spilled = []
	newasm = []
	for index, instr in enumerate(asm):
		bases = instr.__class__.__bases__
		if isinstance(instr, IfStmt):
			thenSpilled, spill1 = spillCode(instr.thenAssign, graph, colors, gen)
			elseSpilled, spill2 = spillCode(instr.elseAssign, graph, colors, gen)
			spilled = spilled + spill1 + spill2
			newasm.append(IfStmt(
				instr.test,
				thenSpilled,
				elseSpilled,
				instr.ret,
				instr.liveThen,
				instr.liveElse
			))
		elif len(bases) and bases[0] == TwoArgs:
			if isinstance(instr, Cmovel) and instr.reg2 and colors[instr.reg2] > 7:
				#Apparently, cmovel does not allow a displacement in the destination location
				spilledvar = gen.inc().name()
				spilled.append(spilledvar)
				printd( "in spilled cmovel "+spilledvar)
				if instr.const1:
					newasm.append(Cmovel(const1=instr.const1, reg2=spilledvar))
				else:
					newasm.append(Cmovel(reg1=instr.reg1, reg2=spilledvar))
				newasm.append(Movl(reg1=spilledvar, reg2=instr.reg2,comment="spilled "+instr.reg2+" into "+spilledvar))
			elif instr.reg1 and instr.reg1 in colors and colors[instr.reg1] > 7 and instr.reg2 and instr.reg2 in colors and colors[instr.reg2] > 7:
				spilledvar = gen.inc().name()
				spilled.append(spilledvar)
				
				newasm.append(Movl(reg1=instr.reg1,reg2=spilledvar,comment="spilled "+instr.reg2+" into "+spilledvar))
				newasm.append(instr.__class__(reg1=spilledvar,reg2=instr.reg2))
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
			newasm.append(Jl(labelName1))
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
			loc= colorGraph.reg_color[instr.reg]
		if loc > 7:
			instr.reg = "%ebp"
			instr.offset = -(loc-10+1)*4
		else:
			instr.reg = colorGraph.reg_map[loc]

def locTwoArgs(instr, color):
	if instr.reg1 and instr.reg1 != "%esp" and instr.reg1 != "%ebp":
		if instr.reg1 in color:
			loc = color[instr.reg1]
		else:
			loc= colorGraph.reg_color[instr.reg1]
		if loc > 7:
			instr.reg1 = "%ebp"
			instr.offset1 = -(loc-10+1)*4
		else:
			instr.reg1 = colorGraph.reg_map[loc]
	if instr.reg2 and instr.reg2 != "%esp" and instr.reg2 != "%ebp":
		if instr.reg2 in color:
			loc = color[instr.reg2]
		else:
			loc= colorGraph.reg_color[instr.reg2]
		if loc > 7:
			instr.reg2 = "%ebp"
			instr.offset2 = -(loc-10+1)*4
		else:
			instr.reg2 = colorGraph.reg_map[loc]


def assignLocations(asm, color):
	for instr in asm:
		bases = instr.__class__.__bases__
		if len(bases):
			{
				OneArg:  locOneArg,
				TwoArgs: locTwoArgs,
			}[bases[0]](instr, color)

#Spilled is an array of spilled variables
def assignSpilled(g, spilled):
	for k in spilled:
		g[k] = (g[k][0] if k in g else set([]), True)

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
.asciz "Attempt to negate a non basic type.\\n"
addError:
.asciz "Attempt to add a basic type to a non basic type.\\n"
debugMsg1:
.asciz "Debug Message 1.\\n"
debugMsg2:
.asciz "Debug Message 2.\\n"
.text\n'''

def mainLoop(asm, g, spilled, gen):
	l = liveness.liveness(asm)
	#printd("liveness:\n"+str(l))
	g = interference.interfere(asm, l, {})
	#add spilled flag to vars in new graph
	#printd("interfernce:\n"+str(g))
	assignSpilled(g, spilled)
	#printd("interfernce:\n"+str(g))
	colors = colorGraph.color_graph(g)
	#printd("colors:\n"+str(colors))
	asm, s = spillCode(asm, g, colors, gen)
	spilled = spilled + s
	return asm, g, spilled, colors, bool(s)

def compile(ast):
	gen = GenSym()
	map = {}
	state = ()
	explicate.explicate(ast, gen)
	#print "explicated ast:"
	#astpp.printAst(ast)
	newast = flattener.flatten(ast, None, gen, map)
	#print "flattened ast:"
	#astpp.printAst(newast)
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
	#print(gen.name())

	maxiter = 10
	iter = 1
	asm, g, spilled, colors, cont = mainLoop(asm, {}, [], gen)
	while cont and iter != maxiter:
		iter += 1
		#print ("Iteration: "+str(iter))
		asm, g, spilled, colors, cont = mainLoop(asm, g, spilled, gen)
	
	if iter == maxiter:
		print maxiter,"iterations was not enough to assign spilt variables"
		sys.exit(1)
	
	asm = removeIf(asm, GenSym())
	assignLocations(asm, colors)
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
