x = 4
class A:
	x = 2

class B(A):
	print x
	#if False:
	#	x = 3
	#else:
	#	0
	#print x
	def __init__(self):
		print 0
		print self.x

print 42
o = B()
