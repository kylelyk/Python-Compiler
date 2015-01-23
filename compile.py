import compiler, sys, re, astpp
from compiler.ast import *

class GenSym:
	def __init__(self):
		self.n = 0
	def inc(self):
		self.n += 1
		return self
	def name(self):
		return "__$tmp" + str(self.n)
		
def addComment(comment):
	return ("\t\t#" + comment) if comment else ""

class TwoArgs(object):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		self.offset1 = offset1
		self.const1 = const1
		self.reg1 = reg1
		self.offset2 = offset2
		self.const2 = const2
		self.reg2 = reg2
		self.comment = comment
	def setName(self, name):
		self.name = name
	def __str__(self):
		ret = "\t" + self.name + " "
		ret += ("$" + str(self.const1)) if self.const1 is not None else (str(self.offset1) + "(" + self.reg1 + ")" if self.offset1 else self.reg1)
		ret += ", "
		ret += ("$" + str(self.const2)) if self.const2 is not None else (str(self.offset2) + "(" + self.reg2 + ")" if self.offset2 else self.reg2)
		ret += addComment(self.comment)
		return  ret

class Movl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Movl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("movl")

class Subl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Subl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("subl")

class Addl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Addl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("addl")

class OneArg(object):
	def __init__(self, offset = None, const = None, reg = None, comment = ""):
		self.offset = offset
		self.const = const
		self.reg = reg
		self.comment = comment
	def setName(self, name):
		self.name = name
	def __str__(self):
		ret = "\t" + self.name + " "
		ret += ("$" + str(self.const) if self.const is not None else (str(self.offset) + "(" + self.reg + ")" if self.offset else self.reg))
		ret += addComment(self.comment)
		return  ret

class Pushl(OneArg):
	def __init__(self, offset = None, const = None, reg = None, comment = ""):
		super(Pushl, self).__init__(offset, const, reg, comment)
		self.setName("pushl")

class Popl(OneArg):
	def __init__(self, offset = None, const = None, reg = None, comment = ""):
		super(Popl, self).__init__(offset, const, reg, comment)
		self.setName("popl")

class Negl(OneArg):
	def __init__(self, offset = None, const = None, reg = None, comment = ""):
		super(Negl, self).__init__(offset, const, reg, comment)
		self.setName("negl")

class Call():
	def __init__(self, name, comment = ""):
		self.name = name
		self.comment = comment
	def __str__(self):
		return "\tcall " + self.name + addComment(self.comment)

class Leave():
	def __init__(self, comment = ""):
		self.comment = comment
	def __str__(self):
		return "\tleave" + addComment(self.comment)

class Ret():
	def __init__(self, comment = ""):
		self.comment = comment
	def __str__(self):
		return "\tret" + addComment(self.comment)

class Newline():
	def __init__(self, comment = ""):
		self.comment = comment
	def __str__(self):
		return addComment(self.comment)

def addStmt(node, newast, gen, map, name = None):
	if not name:
		name = gen.inc().name()
		map[name] = len(map)
	newnode = Assign([AssName(name, 'OP_ASSIGN')], node)
	newast.nodes.append(newnode)
	return Name(name)

def flatModule(ast, newast, gen, map):
	return flatten(ast.node, newast, gen, map)

def flatStmt(ast, newast, gen, map):
	newast = Stmt([])
	for node in ast.nodes:
		flatten(node, newast, gen, map)
	return newast

def flatPrintnl(ast, newast, gen, map):
	simple = flatten(ast.nodes[0], newast, gen, map)
	return newast.nodes.append(Printnl([simple], None))
	
def flatConst(ast, newast, gen, map):
	return ast

def flatName(ast, newast, gen, map):
	return ast

def flatUnarySub(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	if isinstance(simple, Const):
		return Const(-simple.value)
	return addStmt(UnarySub(simple), newast, gen, map)

def flatAdd(ast, newast, gen, map):
	s1 = flatten(ast.left, newast, gen, map)
	s2 = flatten(ast.right, newast, gen, map)
	return addStmt(Add((s1, s2)), newast, gen, map)

def flatDiscard(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	return 0#addStmt(Discard(simple), newast, gen, map)

def flatAssign(ast, newast, gen, map):
	simple = flatten(ast.expr, newast, gen, map)
	map[ast.nodes[0].name] = len(map)
	return addStmt(simple, newast, gen, map, ast.nodes[0].name)

def flatCallFunc(ast, newast, gen, map):
	return addStmt(ast, newast, gen, map)

def flatten(ast, newast, gen, map):
	return {
		Module:   flatModule,
		Stmt:     flatStmt,
		Printnl:  flatPrintnl,
		Const:    flatConst,
		UnarySub: flatUnarySub,
		Add:      flatAdd,
		Discard:  flatDiscard,
		Assign:   flatAssign,
		Name:     flatName,
		CallFunc: flatCallFunc
	}[ast.__class__](ast, newast, gen, map)

def getStackLoc(key, map):
	return -(map[key] + 1) * 4
	
def moveInto(node, reg, asm, map):
	if isinstance(node, Const):
		asm.append(Movl(const1=node.value, reg2=reg))
	else:
		asm.append(Movl(getStackLoc(node.name, map), None, "%ebp", None, None, reg))

def toAsmStmt(ast, asm, map):
	for n in ast.nodes:
		pyToAsm(n, asm, map)
		asm.append(Newline())

def toAsmPrintnl(ast, asm, map):
	n = ast.nodes[0]
	if isinstance(n, Const):
		asm.append(Pushl(const=n.value))
	else:
		asm.append(Pushl(getStackLoc(n.name, map), None, "%ebp"))
	asm.append(Call("print_int_nl"))
	asm.append(Addl(const1=4, reg2="%esp"))

def toAsmConst(ast, asm, map):
	moveInto(ast, "%ebx", asm, map)

def toAsmUnarySub(ast, asm, map):
	moveInto(ast.expr, "%ebx", asm, map)
	asm.append(Negl(reg="%ebx"))

def toAsmAdd(ast, asm, map):
	moveInto(ast.left, "%eax", asm, map)
	moveInto(ast.right,"%ebx", asm, map)
	asm.append(Addl(reg1="%eax", reg2="%ebx"))
	

def toAsmAssign(ast, asm, map):
	pyToAsm(ast.expr, asm, map)
	asm.append(Movl(None, None, "%ebx", getStackLoc(ast.nodes[0].name, map), None, "%ebp"))

def toAsmName(ast, asm, map):
	moveInto(ast, "%ebx", asm, map)

def toAsmCallFunc(ast, asm, map):
	asm.append(Call("input"))
	asm.append(Movl(reg1="%eax",reg2="%ebx"))

def pyToAsm(ast, asm, map):
	return {
		Stmt:     toAsmStmt,
		Printnl:  toAsmPrintnl,
		Const:    toAsmConst,
		UnarySub: toAsmUnarySub,
		Add:      toAsmAdd,
		Assign:   toAsmAssign,
		Name:     toAsmName,
		CallFunc: toAsmCallFunc
	}[ast.__class__](ast, asm, map)

def compile(ast):
	gen = GenSym()
	map = {}
	state = ()
	newast = flatten(ast, None, gen, map)
	asm = []
	asm.append(Pushl(reg="%ebp"))
	asm.append(Movl(reg1="%esp", reg2="%ebp"))
	asm.append(Subl(const1=len(map)*4, reg2="%esp"))
	asm.append(Newline())
	'''pushl %ebp
movl %esp, %ebp
subl $12,%esp
	'''
	#print "\n\nNew AST:"
	#print newast
	#astpp.printAst(newast)
	pyToAsm(newast, asm, map)
	asm.append(Movl(const1=0, reg2="%eax"))
	asm.append(Leave())
	asm.append(Ret())
	#print "\n\nASM:"
	f = open(re.split("\.", sys.argv[1])[0]+".s", "w")
	f.write(".globl main\nmain:\n")
	for instr in asm:
		f.write(str(instr)+"\n")
	output = '''.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	leave
	ret
	'''
	output = '''.globl main
main:
	pushl %ebp
	movl %esp, %ebp
	subl $4, %esp
	call input
	negl %eax
	movl %eax, -4(%ebp)
	call input
	addl -4(%ebp), %eax
	pushl %eax
	call print_int_nl
	addl $4, %esp
	movl $0, %eax
	leave
	ret
	'''
	
	f.close()

if len(sys.argv) != 2:
	print "Name of file is required"
	sys.exit(1)
	

ast = compiler.parseFile(sys.argv[1])
compile(ast)
