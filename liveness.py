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

#takes in a set of instructions and a set of live variables after the set of instructions
def liveness(asm, live=set([])):
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
				Node:    liveIf
				}[bases[0]](instr, prev)
		else:
			live_after[l-index-1] = prev
	return live_after