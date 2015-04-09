def mult(x, y):
	i = 0
	acc = 0
	notused = 9
	while i != y:
		acc = acc + x
		i = i + 1
	notused = 10
	return acc

def lessThan(x, y):
	if x == 0:
		return y != 0
	else:
		if y == 0:
			return False
		else:
			return lessThan(x+(-1),y+(-1))

def exp(b, e):
	if e == 0:
		return 1
	else:
		if e == 1:
			return b
		else:
			0
	i = 1
	acc = 1
	while e:
		if lessThan(b, acc):
			acc = mult(acc, b)
		else:
			acc = mult(b, acc)
		e = e + (-1)
	
	return acc

#print mult(6, 9)
print exp(5, 3)
