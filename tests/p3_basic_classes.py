globl = 0
x = 0
class C:
	print x
	x = 3
	#print x
	
	def __init__(self, param):
		print param
		print self.x
		self.param = param
		#return 0
	if True:
		def foo(self, y):
			print self.x
			print 1
			return 0
	else:
		def foo(self, y):
			print 1
			print y
			return 0
		#w = 3
		#print globl
		#return y + w
		#z = x + 9
	#else:
	#	9
	#def foo(self, y):
	#	return self.x + y
	#print 1

#print C.x
#C.x = 0
#print C.x
o = C(7)
print o.param
#print o.x
print o.foo(1)