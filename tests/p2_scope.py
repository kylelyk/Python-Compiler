x = 5

def f(x):
	y = x + 2
	return lambda x: x+y

def g(x):
	return x

print(f(15)(29))
print(g(7))
