import compiler
from compiler.ast import *

def addComment(comment):
	return ("\t\t#" + comment) if comment else ""

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

class Addl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Addl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("addl")

class Subl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Subl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("subl")


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

def getStackLoc(key, map):
	return -(map[key] + 1) * 4
	
def moveInto(node, reg, asm, map):
	if isinstance(node, Const):
		asm.append(Movl(const1=node.value, reg2=reg))
	else:
		asm.append(Movl(reg1=node.name, reg2=reg))

def toAsmStmt(ast, assign, asm, map):
	for n in ast.nodes:
		pyToAsm(n, assign, asm, map)
		#asm.append(Newline())

def toAsmPrintnl(ast, assign, asm, map):
	n = ast.nodes[0]
	if isinstance(n, Const):
		asm.append(Pushl(const=n.value))
	else:
		asm.append(Pushl(reg=n.name))
	asm.append(Call("print_int_nl"))
	asm.append(Addl(const1=4, reg2="%esp"))

def toAsmConst(ast, assign, asm, map):
	moveInto(ast, assign, asm, map)

def toAsmUnarySub(ast, assign, asm, map):
	if isinstance(ast.expr, Const):
		asm.append(Movl(const1=ast.expr.value, reg2=assign))
	else:
		asm.append(Movl(reg1=ast.expr.name, reg2=assign))
	asm.append(Negl(reg=assign))

def toAsmAdd(ast, assign, asm, map):
	moveInto(ast.right, assign, asm, map)
	if isinstance(ast.left, Const): 
		asm.append(Addl(const1=ast.left.value, reg2=assign))
	else:
		asm.append(Addl(reg1=ast.left.name, reg2=assign))
	

def toAsmAssign(ast, assign, asm, map):
	pyToAsm(ast.expr, ast.nodes[0].name, asm, map)

def toAsmName(ast, assign, asm, map):
	moveInto(ast, assign, asm, map)

def toAsmCallFunc(ast, assign, asm, map):
	asm.append(Call("input"))
	asm.append(Movl(reg1="%eax",reg2=assign))

def pyToAsm(ast, assign, asm, map):
	return {
		Stmt:     toAsmStmt,
		Printnl:  toAsmPrintnl,
		Const:    toAsmConst,
		UnarySub: toAsmUnarySub,
		Add:      toAsmAdd,
		Assign:   toAsmAssign,
		Name:     toAsmName,
		CallFunc: toAsmCallFunc
	}[ast.__class__](ast, assign, asm, map)