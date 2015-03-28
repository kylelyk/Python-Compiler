import compiler, astpp
from compiler.ast import *
from HelperClasses import *

def addComment(comment):
	return ("#" + comment) if comment else ""

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
		ret = ret.ljust(25)
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

class Call(OneArg):
	def __init__(self, offset = None, const = None, reg = None, star = False, comment = ""):
		super(Call, self).__init__(offset, const, reg, comment)
		self.setName("call ")
		self.star = star
	def __str__(self):
		s = super(Call, self).__str__()
		return s[:6]+("*" if self.star else " ")+s[7:]


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
		ret = ret.ljust(25)
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

class Cmovel(TwoArgs):
	def __init__(self, offset1 = None, const1 = None, reg1 = None, offset2 = None, const2 = None, reg2 = None, comment = ""):
		super(Cmovel, self).__init__(offset1, const1, reg1, offset2, const2, reg2, comment)
		self.setName("cmovel")

class Je():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return ("\tje " + self.label).ljust(25) + addComment(self.comment)

class Jne():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return ("\tjne " + self.label).ljust(25) + addComment(self.comment)
	
class Jl():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return ("\tjl " + self.label).ljust(25) + addComment(self.comment)

class Jmp():
	def __init__(self, label, comment = ""):
		self.label = label
		self.comment = comment
	def __str__(self):
		return ("\tjmp " + self.label).ljust(25) + addComment(self.comment)

class Label():
	def __init__(self, name, comment = ""):
		self.name = name
		self.comment = comment
	def __str__(self):
		return (self.name + ":").ljust(25) + addComment(self.comment) 


class Leave():
	def __init__(self, comment = ""):
		self.comment = comment
	def __str__(self):
		return "\tleave".ljust(25) + addComment(self.comment)

class Ret():
	def __init__(self, comment = ""):
		self.comment = comment
	def __str__(self):
		return "\tret".ljust(25) + addComment(self.comment)

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

def addInstr2(arg1, arg2, instr, asm, commentFunc):
	if isinstance(arg1, Const):
		if isinstance(arg2, Const):
			asm.append(instr(const1=arg1.value, const2=arg2.value,comment=commentFunc(str(arg1.value),str(arg2.value))))
		else:
			asm.append(instr(const1=arg1.value, reg2=arg2.name,comment=commentFunc(str(arg1.value),str(arg2.name))))
	else:
		if isinstance(arg2, Const):
			asm.append(instr(reg1=arg1.name, const2=arg2.value,comment=commentFunc(str(arg1.name),str(arg2.value))))
		else:
			asm.append(instr(reg1=arg1.name, reg2=arg2.name,comment=commentFunc(str(arg1.name),str(arg2.name))))

def addInstr1(arg, instr, asm, commentFunc):
	if isinstance(arg, Const):
		asm.append(instr(const=arg.value, comment=commentFunc(str(arg.value))))
	else:
		asm.append(instr(reg=arg.name, comment=commentFunc(str(arg.name))))

def toAsmStmt(ast, assign, asm, map):
	return reduce(lambda acc, n : acc + toAsm(n, assign, asm, map), ast.nodes, [])

def toAsmPrintnl(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmConst(ast, assign, asm, map):
	moveInto(ast, assign, asm, map)
	return []

def toAsmUnarySub(ast, assign, asm, map):
	addInstr2(ast.expr, Name(assign), Movl, asm, lambda a, b : "- "+a)
	asm.append(Negl(reg=assign))
	return []

def toAsmAdd(ast, assign, asm, map):
	moveInto(ast.right, assign, asm, map)
	addInstr2(ast.left, Name(assign), Addl, asm, lambda a, b : a+" + "+b)
	return []

def toAsmAssign(ast, assign, asm, map):
	return toAsm(ast.expr, ast.nodes[0].name, asm, map)

def toAsmName(ast, assign, asm, map):
	moveInto(ast, assign, asm, map)
	return []

def toAsmCallFunc(ast, assign, asm, map, star=True):
	comment = ast.node.name+"("
	for arg in ast.args:
		comment += str(arg.value)+", " if isinstance(arg, Const) else arg.name+", "
	if len(ast.args) > 0:
		comment = comment[:-2]
	comment += ")"
	for arg in reversed(ast.args):
		addInstr1(arg, Pushl, asm, lambda a: None)
	asm.append(Call(reg=ast.node.name,comment=comment,star=star))
	#Don't do anything with eax if there is no assign
	if assign:
		asm.append(Movl(reg1="%eax",reg2=assign, comment="%eax -> "+assign))
	asm.append(Addl(const1=len(ast.args)*4,reg2="%esp"))
	return []

def toAsmCallRuntime(ast, assign, asm, map):
	return toAsmCallFunc(ast, assign, asm, map, False)

def toAsmCompare(ast, assign, asm, map):
	'''
	Compare two basic values.
	Should not be called with complex values.
	'''
	lhs = ast.expr
	op, rhs = ast.ops[0]
	addInstr2(lhs, rhs, Cmpl, asm, lambda a, b : "cmp "+a+", "+b)
	if op == "!=":
		asm.append(Movl(reg1="True", reg2=assign))
		asm.append(Cmovel(reg1="False",reg2=assign))
	else:
		asm.append(Movl(reg1="False", reg2=assign))
		asm.append(Cmovel(reg1="True",reg2=assign))
	return []

#Assumes both arguments are metalanguage int types (no tag) 
#since this node should be generated by explicate/flatten only
def toAsmOr(ast, assign, asm, map):
	moveInto(ast.nodes[0], assign, asm, map)
	addInstr2(ast.nodes[1], Name(assign), Orl, asm, lambda a, b : a+" bitor "+b)
	return []

def toAsmAnd(ast, assign, asm, map):
	moveInto(ast.nodes[0], assign, asm, map)
	addInstr2(ast.nodes[1], Name(assign), Andl, asm, lambda a, b : a+" bitand "+b)
	return []

def toAsmNot(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError
	return []

def toAsmBitxor(ast, assign, asm, map):
	moveInto(ast.nodes[0], assign, asm, map)
	addInstr2(ast.nodes[1], Name(assign), Xorl, asm, lambda a, b : a+" bitxor "+b)
	return []

def toAsmList(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmDict(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmSubscript(ast, assign, asm, map):
	#Code should never reach here
	raise NotImplementedError

def toAsmIfStmt(ast, assign, asm, map):
	#Only generate statements inside the if statement, do not flatten yet
	new1 = []
	new2 = []
	asm.append(Newline())
	addInstr2(Name("True"), ast.test, Cmpl, asm, lambda a, b : "Start of if("+b+" == True)")
	l = []
	reduce(lambda acc, n : acc + toAsm(n, assign, new1, map), ast.thenAssign, l)
	reduce(lambda acc, n : acc + toAsm(n, assign, new2, map), ast.elseAssign, l)
	#use this line to debug the branching of if statements
	#[Pushl(const="debugMsg1"),Call(reg="puts"),Addl(const1=4,reg2="%esp")] +
	ast.thenAssign = new1
	ast.elseAssign = new2
	asm.append(ast)
	asm.append(Newline())
	return l

def toAsmLambda(ast, assign, asm, map):
	asm.append(Pushl(reg="%ebp"))
	asm.append(Movl(reg1="%esp", reg2="%ebp"))
	allocStmt = Subl(const1=0, reg2="%esp")
	asm.append(allocStmt)
	asm.append(Pushl(reg="%ebx"))
	asm.append(Pushl(reg="%edi"))
	asm.append(Pushl(reg="%esi"))
	asm.append(Movl(const1=0b001, reg2="False"))
	asm.append(Movl(const1=0b101, reg2="True"))
	for i, arg in enumerate(ast.argnames):
		asm.append(Movl(offset1=(i+2)*4, reg1="%ebp", reg2=arg, comment=arg))
	asm.append(Newline())
	return [allocStmt] + toAsm(ast.code, assign, asm, map)

def toAsmReturn(ast, assign, asm, map):
	addInstr2(ast.value, Name("%eax"), Movl, asm, lambda a, b : a + " -> " + b)
	asm.append(Newline())
	asm.append(Popl(reg="%esi"))
	asm.append(Popl(reg="%edi"))
	asm.append(Popl(reg="%ebx"))
	allocStmt = Addl(const1=0, reg2="%esp")
	asm.append(allocStmt)
	asm.append(Leave())
	asm.append(Ret())
	return [allocStmt]

#Returns a list of references to asm instructions that either 
#allocate or deallocate stack space in the lambda
def toAsm(ast, assign, asm, map):
	return {
		Stmt:        toAsmStmt,
		Printnl:     toAsmPrintnl,
		Const:       toAsmConst,
		UnarySub:    toAsmUnarySub,
		Add:         toAsmAdd,
		Assign:      toAsmAssign,
		Name:        toAsmName,
		CallFunc:    toAsmCallFunc,
		CallRuntime: toAsmCallRuntime,
		Compare:     toAsmCompare,
		Or:          toAsmOr,
		And:         toAsmAnd,
		Not:         toAsmNot,
		Bitxor:      toAsmBitxor,
		List:        toAsmList,
		Dict:        toAsmDict,
		Subscript:   toAsmSubscript,
		IfStmt:      toAsmIfStmt,
		Lambda:      toAsmLambda,
		Return:      toAsmReturn
	}[ast.__class__](ast, assign, asm, map)

#Returns a list of tuples: (funcName, func asm body, [ref1, ref2, ...])
#where ref1 and ref2 are references to the move stack pointer instructions
#that will need to be update once register allocation is done
def pyToAsm(ast, asm, map):
	for n, a in ast:
		funcAsm = []
		funcAsm.append(Label(n))
		allocs = toAsm(a, None, funcAsm, map)
		asm.append((n, funcAsm, allocs))
