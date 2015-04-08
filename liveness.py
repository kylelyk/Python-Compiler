from x86AST import *

def condAdd(set, elm):
	if elm is not None and elm[0] != "%":
		set.add(elm)

def liveOneArg(instr, prev):
	s = set(prev)
	#All instructions read from the var but negl and popl writes to the var
	if not isinstance(instr, Pushl):
		s.discard(instr.reg)
	
	#Regular calls should not add an edge
	if not isinstance(instr, Call) or instr.star:
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

def liveIf(instr, prev):
	liveThen = set(prev if prev else [])
	liveElse = set(prev if prev else [])
	instr.liveThen = liveness(instr.thenAssign, prev)
	instr.liveElse = liveness(instr.elseAssign, prev)
	#TODO remove this hack
	part1 = liveness([instr.thenAssign[0]], instr.liveThen[0])
	part2 = liveness([instr.elseAssign[0]], instr.liveElse[0])
	return part1[0] | part2[0]

#L4 = Lafter
#L1 = L4 U L2 U {guard}
#L0 = Lbefore(test, L1)
#L3 = Lbefore(test, L1)
#L2 = Lbefore(body, L3)
#return L0
def liveWhile(instr, prev):
	#If a variable is live at any time during the while loop,
	#it needs to be live during the whole loop
	guard = instr.test.name
	test = instr.testAssign
	body = instr.bodyAssign
	print "\n\nbody ast:",
	for inst in body:
		print inst
	print "\n\ntest ast:"
	for inst in test:
		print inst
	updated = True
	lCur = [set(), set(), set(), set(), set(prev)]
	lPrev = []
	while updated:
		print "body liveness:",liveness(body, lCur[3])
		lPrev = list(lCur)
		lCur[0] = liveness(test, lCur[1])[0]
		lCur[1] = lCur[4] | lCur[2] | set([guard])
		lCur[2] = liveness(body, lCur[3])[0]
		lCur[3] = liveness(test, lCur[1])[0]
		lCur[4] = set(prev)
		updated = lCur != lPrev
	instr.liveTest = liveness(test, lCur[1])
	instr.liveBody = liveness(body, lCur[3])
	for c in lCur:
		print c
	return lCur[0]

#Finds the liveness of custom nodes
def liveCustom(instr, prev):
	return {
		IfStmt:   liveIf,
		ModWhile: liveWhile
	}[instr.__class__](instr, prev)

#takes in a set of instructions and a set of live variables after the set of instructions
def liveness(asm, live=set()):
	live_after = [0]*len(asm)
	l = len(live_after) - 1
	for index, instr in enumerate(reversed(asm)):
		bases = instr.__class__.__bases__
		prev = live_after[l-index] if index != 0 else live
		if len(bases):
			#compute the liveness of the instruction if it actually does anything to variables
			#instructions that do not inherit from OneArg, TwoArgs, or Node (If) are not considered
			#and the result is copied from the previous iteration
			live_after[l-index-1] = {
				OneArg:  liveOneArg,
				TwoArgs: liveTwoArgs,
				Node:    liveCustom
				}[bases[0]](instr, prev)
		else:
			live_after[l-index-1] = prev
	return live_after