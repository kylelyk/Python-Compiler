import compiler
from compiler.ast import *
from flattener import IfStmt

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

class Orl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Orl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("orl")

class Xorl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Xorl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("xorl")

class Andl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Andl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("andl")

class Cmpl(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Cmpl, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("cmpl")

class Je():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return "\tje " + self.label + addComment(self.comment)

class Jne():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return "\tjne " + self.label + addComment(self.comment)

class Jmp():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return "\tjmp " + self.label + addComment(self.comment)

class Label():
	def __init__(self, name, comment = ""):
		self.name = name
		self.comment = comment
	def __str__(self):
		return self.name + ":" + addComment(self.comment) 

class Call():
	def __init__(self, name, comment = ""):
		self.name = name
		self.comment = comment
	def __str__(self):
		#print "self.name: "
		#print self.name
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
		asm.append(Movl(const1=node.value, reg2=reg, comment=str(node.value)+" -> "+reg))
	else:
		asm.append(Movl(reg1=node.name, reg2=reg, comment=node.name+" -> "+reg))

def toAsmStmt(ast, assign, asm, map):
	#print "\nassign:",assign
	#print "stmt"
	for n in ast.nodes:
		pyToAsm(n, assign, asm, map)
		#asm.append(Newline())

def toAsmPrintnl(ast, assign, asm, map):
	#print "\nassign:",assign
	#print ast
	n = ast.nodes[0]
	if isinstance(n, Const):
		asm.append(Pushl(const=n.value, comment=str(n.value)))
	else:
		asm.append(Pushl(reg=n.name, comment=n.name))
	asm.append(Call("print_any"))
	asm.append(Addl(const1=4, reg2="%esp"))

def toAsmConst(ast, assign, asm, map):
	#print ast
	#print "\nassign:",assign
	#print "const"
	moveInto(ast, assign, asm, map)

def toAsmUnarySub(ast, assign, asm, map):
	#print "UnarySub"
	if isinstance(ast.expr, Const):
		asm.append(Movl(const1=ast.expr.value, reg2=assign, comment="- "+str(ast.expr.value)))
	else:
		asm.append(Movl(reg1=ast.expr.name, reg2=assign, comment="- "+str(ast.expr.name)))
	asm.append(Negl(reg=assign))

def toAsmAdd(ast, assign, asm, map):
	#print "Add"
	moveInto(ast.right, assign, asm, map)
	if isinstance(ast.left, Const):
		asm.append(Addl(const1=ast.left.value, reg2=assign, comment=str(ast.left.value)+" + "+assign))
	else:
		asm.append(Addl(reg1=ast.left.name, reg2=assign, comment=ast.left.name+" + "+assign))

def toAsmAssign(ast, assign, asm, map):
	#print "Assign"
	pyToAsm(ast.expr, ast.nodes[0].name, asm, map)

def toAsmName(ast, assign, asm, map):
	moveInto(ast, assign, asm, map)

def toAsmCallFunc(ast, assign, asm, map):
	comment = ast.node+"("
	for arg in ast.args:
		comment += str(arg.value)+", " if isinstance(arg, Const) else arg.name+", "
	if len(ast.args) > 0:
		comment = comment[:-2]
	comment += ")"
	for arg in reversed(ast.args):
		if isinstance(arg, Const):
			asm.append(Pushl(const=arg.value))
		else:
			asm.append(Pushl(reg=arg.name))
	#print "call is given:",ast
	asm.append(Call(ast.node,comment=comment))
	asm.append(Movl(reg1="%eax",reg2=assign, comment="%eax -> "+assign))
	asm.append(Addl(const1=len(ast.args)*4,reg2="%esp"))

def toAsmCompare(ast, assign, asm, map):
	#print "Compare"
	lhs = ast.expr
	op, rhs = ast.ops[0]
	
	if isinstance(lhs, Const):
		asm.append(Pushl(const=lhs.value, comment=str(lhs.value)))
	else:
		asm.append(Pushl(reg=lhs.name, comment=lhs.name))
	if isinstance(rhs, Const):
		asm.append(Pushl(const=rhs.value, comment=str(rhs.value)))
	else:
		asm.append(Pushl(reg=rhs.name, comment=rhs.name))
	if op == "==":
		asm.append(Call("equal"))
	elif op == "!=":
		asm.append(Call("not_equal"))
	asm.append(Pushl(reg1="%eax"))
	asm.append(Call("inject_bool"))
	asm.append(Movl(reg1="%eax", reg2=assign, comment="%eax -> "+assign))
	asm.append(Subl(const1=12,reg2="%esp"))

#Assumes both arguments are metalanguage int types (no tag) 
#since this node should be generated by explicate/flatten only
def toAsmOr(ast, assign, asm, map):
	moveInto(ast.nodes[0], assign, asm, map)
	if isinstance(ast.nodes[1], Const):
		asm.append(Orl(const1=ast.nodes[1].value, reg2=assign, comment=str(ast.nodes[1].value)+" bitor "+assign))
	else:
		asm.append(Orl(reg1=ast.nodes[1].name, reg2=assign, comment=ast.nodes[1].name+" bitor "+assign))

def toAsmAnd(ast, assign, asm, map):
	moveInto(ast.nodes[0], assign, asm, map)
	if isinstance(ast.nodes[1], Const):
		asm.append(Andl(const1=ast.nodes[1].value, reg2=assign, comment=str(ast.nodes[1].value)+" bitand "+assign))
	else:
		asm.append(Andl(reg1=ast.nodes[1].name, reg2=assign, comment=ast.nodes[1].name+" bitand "+assign))

def toAsmNot(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmBitxor(ast, assign, asm, map):
	moveInto(ast[0], assign, asm, map)
	if isinstance(ast.nodes[1], Const):
		asm.append(Xorl(const1=ast.nodes[1].value, reg2=assign, comment=str(ast.nodes[1].value)+" bitxor "+assign))
	else:
		asm.append(Xorl(reg1=ast.nodes[1].name, reg2=assign, comment=ast.nodes[1].name+" bitxor "+assign))

def toAsmList(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmDict(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmSubscript(ast, assign, asm, map):
	raise NotImplementedError

def toAsmIfStmt(ast, assign, asm, map):
	#Only generate statements inside the if statement, do not flatten yet
	new1 = []
	new2 = []
	asm.append(Newline())
	asm.append(Cmpl(reg1="True",reg2=ast.test.name,comment="Start of if("+ast.test.name+" == True)"))
	for n in ast.thenAssign:
		pyToAsm(n, assign, new1, map)
	for n in ast.elseAssign:
		pyToAsm(n, assign, new2, map)
	ast.thenAssign = new1
	ast.elseAssign = new2
	asm.append(ast)
	asm.append(Newline())

def pyToAsm(ast, assign, asm, map):
	#print "\n\n",ast
	#print "pyToAsm:",assign
	#print "ast:", ast
	return {
		Stmt:      toAsmStmt,
		Printnl:   toAsmPrintnl,
		Const:     toAsmConst,
		UnarySub:  toAsmUnarySub,
		Add:       toAsmAdd,
		Assign:    toAsmAssign,
		Name:      toAsmName,
		CallFunc:  toAsmCallFunc,
		Compare:   toAsmCompare,
		Or:        toAsmOr,
		And:       toAsmAnd,
		Not:       toAsmNot,
		Bitxor:    toAsmBitxor,
		List:      toAsmList,
		Dict:      toAsmDict,
		Subscript: toAsmSubscript,
		IfStmt:    toAsmIfStmt
	}[ast.__class__](ast, assign, asm, map)
