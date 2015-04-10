globl = 0
x = 0

x = 32
y = True
class D():
	def foo2(self):
		print 443
		return 1

class E():
	y = 9
	print y
	def foo2(self):
		print 665
		return 0

class C(D,E):
	#print x
	x = 3
	#print x
	
	def __init__(self, param):
		print param
		print self.x
		print E.y
		self.param = param
		#return 0
	#if input():
	#	def foo(self, y):
	#		print self.x
	#		print 1
	#		return 0
	#else:
	def foo(self, y):
		print 1
		print y
		return 0
	w = 3
	#print globl
	print y + w
	z = x + 9
	print z
	#else:
	#	9
	def foo2(self, y):
		return self.x + y
	print 1

print C.x
C.x = 0
print C.x

o = C(7)
print o.param
print o.x
print o.foo(1)
print o.foo2(4)