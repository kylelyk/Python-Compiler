from compiler.ast import *

#Flattened version of IfExp
#Is reused for both python ast and asm instructions
class IfStmt(Node):
	def __init__(self, test, thenAssign, elseAssign, ret, liveThen, liveElse):
		'''test needs to be a name but is made into an instruction in 
		pyToAsm (spillCode function needs this);
		ret needs to be a variable name;
		thenAssign and elseAssign need to be lists of assignments/asm instructions
		that would be executed on that branch.'''
		self.test = test
		self.thenAssign = thenAssign
		self.elseAssign = elseAssign
		self.ret = ret
		self.liveThen = liveThen
		self.liveElse = liveElse
	def getChildren(self):
		return (self.test, self.thenAssign, self.elseAssign, self.ret, self.liveThen, self.liveElse)
	def __str__(self):
		ret = "if "+str(self.test)+":\n"
		for instr in self.thenAssign:
			ret += str(instr) + "\n"
		ret += "\treturn "+str(self.ret)
		ret += "\nelse:\n"
		for instr in self.elseAssign:
			ret += str(instr) + "\n"
		ret += "\treturn "+str(self.ret)
		ret += "\nendif"
		return ret

class GetTag(Node):
	def __init__(self, arg):
		self.arg = arg
	def getChildren(self):
		return (self.arg,)
	def __str__(self):
		return "GetTag("+str(self.arg)+")"
class InjectFrom(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
	def __str__(self):
		return "InjectFrom("+str(self.typ)+", "+str(self.arg)+")"
class ProjectTo(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
	def __str__(self):
		return "ProjectTo("+str(self.typ)+", "+str(self.arg)+")"
class Let(Node):
	def __init__(self, var, rhs, body):
		self.var = var
		self.rhs = rhs
		self.body = body
	def getChildren(self):
		return (self.var, self.rhs, self.body)
	def __str__(self):
		return "Let("+str(self.var)+", "+str(self.rhs)+", "+str(self.body)+")"
class IsType(Node):
	def __init__(self, typ, arg):
		self.typ = typ
		self.arg = arg
	def getChildren(self):
		return (self.typ, self.arg)
	def __str__(self):
		return "IsType("+str(self.typ)+", "+str(self.arg)+")"
class ThrowError(Node):
	def __init__(self, msg):
		self.msg = msg
	def getChildren(self):
		return (self.msg,)
	def __str__(self):
		return "ThrowError("+str(self.msg)+")"
class CallRuntime(Node):
	def __init__(self, node, args):
		self.node = node
		self.args = args
	def getChildren(self):
		return (self.node, self.args)
	def __str__(self):
		return "CallRuntime("+str(self.node)+", "+str(self.args)+")"
