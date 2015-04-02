a = 9
b = 10

def f(y):
	if y != 0:
		a = 4
		print a
		return 6
	else:
		b = 8
		print b
		return 1

print a
print b
print f(0)
print a
print b
print f(1)
print a
print b