import compiler, sys, re

class GenSym:
	def __init__(self):
		self.n = 0
	def inc(self):
		self.n += 1
	def name(self):
		return "__$tmp" + str(self.n)

def addInst(output, inst, comment=None):
	output+="\t"+inst+(("\t\t#"+comment) if comment else "")+"\n"

def addLabl(output, label, comment=None):
	output+=label+":"+(("\t\t#"+comment) if comment else "")+"\n"
	
def flatModule(ast):
	pass

def flatten(ast, gen):
	nodelist = getattr(ast, "nodes",None) or [getattr(ast, "node",None)]
	
	if nodelist != [None]:
		for node in nodelist:
			flatten(node, gen)
	print str(ast) + "\n"
	'''print {
		None: lambda: 5,
		[] : lambda l: len(l)
	}.get(getattr(ast, "nodes",None),lambda:4)()'''
	return ast

def compile(ast):
	gen = GenSym()
	ast = flatten(ast, gen)
	print ast
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
	f = open(re.split("\.", sys.argv[1])[0]+".s", "w")
	f.write(output)
	f.close()

if len(sys.argv) != 2:
	print "Name of file is required"
	sys.exit(1)
	

ast = compiler.parseFile(sys.argv[1])

compile(ast)
