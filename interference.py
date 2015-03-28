from x86AST import *

def addEdge(u, v, graph):
	if u in graph:
		graph[u][0].add(v)
	else:
		graph[u] = (set([v]), False)

#guarantees node exists in graph
def addNode(reg, graph):
	if reg and not reg in graph:
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
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereCall(instr, liveSet, graph):
	t = instr.reg
	for v in liveSet:
		addEdge("%eax", v, graph)
		addEdge("%ecx", v, graph)
		addEdge("%edx", v, graph)
		addEdge(v, "%eax", graph)
		addEdge(v, "%ecx", graph)
		addEdge(v, "%edx", graph)
		if instr.star and v != t:
			addEdge(t, v, graph)
			addEdge(v, t, graph)

def interfereIfStmt(instr, liveSet, graph):
	interfere(instr.thenAssign, instr.liveThen, graph)
	interfere(instr.elseAssign, instr.liveElse, graph)

def interfere(asm, liveness, graph):
	interferePass = lambda i,l,g: None
	for index, instr in enumerate(asm):
		{
			Pushl:   interferePass,
			Popl:    interfereNegPop,
			Negl:    interfereNegPop,
			Movl:    interfereMov,
			Addl:    interfereTwoArg,
			Subl:    interfereTwoArg,
			Orl:     interfereTwoArg,
			Andl:    interfereTwoArg,
			Xorl:    interfereTwoArg,
			Cmpl:    interfereTwoArg,
			Cmovel:  interfereTwoArg,
			Call:    interfereCall,
			Leave:   interferePass,
			Ret:     interferePass,
			Newline: interferePass,
			Label:   interferePass,
			IfStmt:  interfereIfStmt
		}[instr.__class__](instr, liveness[index], graph)
	return graph