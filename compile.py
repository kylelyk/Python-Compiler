import compiler, sys, re, astpp, os
sys.path.insert(0, 'Project_Parser')
from compiler.ast import *
from HelperClasses import *
from x86AST import *
from Project_Parser import *
import python_yacc, debugInfo, declassify, uniquify, analysis, heapify, explicate, closure, flattener, liveness, interference, colorGraph

debug = False
def printd(str):
	if debug:
		print str

def separator(name):
	return "="*80 + "\n"+" "*(40-(len(name)/2)) +name +"\n"+"="*80

def needsSpill(instr, colors):
	spill = [False, False]
	spill[0] = (instr.reg1 and instr.reg1 in colors and colors[instr.reg1] > 7) or (instr.reg1 and instr.offset1)
	spill[1] = (instr.reg2 and instr.reg2 in colors and colors[instr.reg2] > 7) or (instr.reg2 and instr.offset2)
	return spill[0] and spill[1]

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
		elif isinstance(instr, ModWhile):
			testSpilled, spill2 = spillCode(instr.testAssign, graph, colors, gen)
			bodySpilled, spill1 = spillCode(instr.bodyAssign, graph, colors, gen)
			spilled = spilled + spill1 + spill2
			newasm.append(ModWhile(
				instr.test,
				testSpilled,
				bodySpilled,
				instr.liveTest,
				instr.liveBody
			))
		elif len(bases) and bases[0] == TwoArgs:
			if isinstance(instr, Cmovel) and instr.reg2 and colors[instr.reg2] > 7:
				#Apparently, cmovel does not allow a displacement in the destination location
				spilledvar = gen.inc().name()
				spilled.append(spilledvar)
				if instr.const1:
					newasm.append(Cmovel(const1=instr.const1, reg2=spilledvar))
				else:
					newasm.append(Cmovel(reg1=instr.reg1, reg2=spilledvar))
				newasm.append(Movl(reg1=spilledvar, reg2=instr.reg2,comment="spilled "+instr.reg2+" into "+spilledvar))
			elif needsSpill(instr, colors):
				spilledvar = gen.inc().name()
				spilled.append(spilledvar)
				
				newasm.append(Movl(offset1=instr.offset1,reg1=instr.reg1,reg2=spilledvar,comment="spilled "+instr.reg2+" into "+spilledvar))
				newasm.append(instr.__class__(reg1=spilledvar,offset2=instr.offset2,reg2=instr.reg2))
			else:
				newasm.append(instr)
		else:
			newasm.append(instr)
	return newasm, spilled

def remove(asm, gen):
	newasm = []
	for instr in asm:
		if isinstance(instr, IfStmt):
			labelName1 = "elselbl_" + gen.inc().get()
			labelName2 = "endlbl_" + gen.get()
			newasm.append(Jl(labelName1))
			newasm.extend(remove(instr.thenAssign, gen))
			newasm.append(Jmp(labelName2))
			newasm.append(Label(labelName1))
			newasm.extend(remove(instr.elseAssign, gen))
			newasm.append(Label(labelName2))
		elif isinstance(instr, ModWhile):
			labelName1 = "whilelbl_" + gen.inc().get()
			labelName2 = "checklbl_" + gen.get()
			newasm.append(Jmp(labelName2))
			newasm.append(Label(labelName1))
			newasm.extend(remove(instr.bodyAssign, gen))
			newasm.append(Label(labelName2))
			newasm.extend(remove(instr.testAssign, gen))
			newasm.append(Je(labelName1))
		else:
			newasm.append(instr)
	return newasm

def locOneArg(instr, color):
	if isinstance(instr, Call) and not instr.star:
		return
	
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
		elif isinstance(instr, Call) and instr.star:
			locCall(instr, color)

#Add spilled flags to vars in new graph
#Spilled is a list of spilled variables
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

def addDataSection(allocs):
	s = '''.data
negError:
.asciz "Attempt to negate a non basic type.\\n"
addError:
.asciz "Attempt to add a basic type to a non basic type.\\n"
debugMsg1:
.asciz "Debug Message 1.\\n"
debugMsg2:
.asciz "Debug Message 2.\\n"\n'''
	for a in allocs:
		s += '''%s:
.asciz "%s"
''' % (a, a)
	#s += "program:\n.asciz \""+open(sys.argv[1]).read().replace("\n","; ")+"\"\n\n"
	s += "\n.text\n"
	return s

def mainLoop(asm, gen):
	newasm = []
	spilled = False
	for n, a, colors, allocs, prevSpillList in asm:
		l = liveness.liveness(a)
		printd("liveness:\n"+str(l))
		g = interference.interfere(a, l, {})
		printd("interfernce:\n"+str(g))
		assignSpilled(g, prevSpillList)
		printd("interfernce:\n"+str(g))
		colors = colorGraph.color_graph(g)
		printd("colors:\n"+str(colors))
		a, spillList = spillCode(a, g, colors, gen)
		printd("spillList:"+str(spillList))
		spilled |= spillList != []
		prevSpillList = prevSpillList + spillList
		newasm.append((n, a, colors, allocs, prevSpillList))
	return newasm, spilled

def compile(ast):
	gen = GenSym("__$tmp")
	map = {}
	state = ()
	strings = set(["INT","BOOL","LIST","DICT","FUNC"])
	
	
	
	astpp.printAst(ast)
	printd(separator("Declassify Pass"))
	declassify.declassify(ast, gen, None, strings)
	printd(separator("Uniquify Pass"))
	
	_, names = uniquify.runUniquify(ast)
	#print names
	#Needs to be done after uniquifying all variables
	lines = {"True":0,"False":0}
	typeAnno = {}
	debugInfo.lines(ast, lines)
	debugInfo.types(ast, typeAnno)
	print lines
	print typeAnno
	astpp.printAst(ast)
	
	printd(separator("Analysis Pass"))
	types = analysis.runAnalysis(ast)
	types = {k:analysis.simplify(v) for k,v in types.iteritems()}
	print types
	analysis.printReport(types, names, lines, False)
	assertTypes = {k:v for k,v in typeAnno.iteritems() if not analysis.checkSoundness(typeAnno[k], types[k], names[k], lines[k])}
	print "Types that need to have runtime checks:",assertTypes
	analysis.addAssert(ast, assertTypes)
	
	printd(separator("Explicate Pass"))
	explicate.explicate(ast, gen)
	printd(separator("Heapify Pass"))
	heapify.runHeapify(ast)
	printd(separator("Closure Pass"))
	ast = closure.closure(ast, gen, GenSym("$lambda"))
	printd(separator("Flatten Pass"))
	newast = flattener.runFlatten(ast, gen, map, strings)
	#for n, a in ast:
	#	print "\n\n",n,"= ",astpp.printAst(a)
	
	printd(separator("Instruction Selection Pass"))
	asm = []
	pyToAsm(newast, asm, map)
	printd("psuedo asm:")
	newasm = []
	for n, a, alloc in asm:
		newasm.append((n, a, {}, alloc, []))
		for instr in a:
			printd(instr)
	
	#newasm[-1][1].insert(3, Addl(const1=4,reg2="%esp"))
	#newasm[-1][1].insert(3, Call(reg="puts"))
	#newasm[-1][1].insert(3, Pushl(const="program"))
	
	printd(separator("Looping Algorithms"))
	asm = newasm
	maxiter = 10
	iter = 1
	asm, cont = mainLoop(asm, gen)
	while cont and iter != maxiter:
		iter += 1
		printd ("Iteration: "+str(iter))
		asm, cont = mainLoop(asm, gen)
	if iter == maxiter:
		print maxiter,"iterations was not enough to assign spilt variables"
		sys.exit(1)
	
	printd(separator("Last Passes"))
	newasm = []
	rmGen = GenSym("")
	for n, a, colors, alloc, spill in asm:
		a = remove(a, rmGen)
		assignLocations(a, colors)
		space = max(0, max(colors.values())-9)*4
		for instr in alloc:
			instr.const1 = space
		#a = optimizePass1(a)
		newasm.append((n, a))
	asm = newasm
	printd("\n\nfinal asm")
	for _, func in asm:
		printd("")
		for instr in func:
			printd(instr)
	
	f = open(re.split("\.[^\.]*$", sys.argv[1])[0]+".s", "w")
	f.write(addDataSection(strings))
	f.write(".globl ")
	for n, _ in asm:
		f.write(n+",")
	f.seek(-1,1)
	f.write("\n")
	for _, func in asm:
		for instr in func:
			f.write(str(instr)+"\n")
	
	f.close()

if len(sys.argv) != 2:
	print "Name of file is required"
	sys.exit(1)

use_project_parser = True

if use_project_parser:
	text = open(sys.argv[1]).read()

	ast = python_yacc.parse(text, sys.argv[1])
else:
	ast = compiler.parseFile(sys.argv[1])
compile(ast)
