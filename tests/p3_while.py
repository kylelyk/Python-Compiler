def mult(x, y):
	i = 0
	acc = 0
	notused = 9
	while i != y:
		acc = acc + x
		i = i + 1
		print notused
	print notused
	return acc

print mult(6,9)