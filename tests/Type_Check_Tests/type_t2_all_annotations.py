#Modify the input file to make cases pass or fail:
#1 for pass, 0 for fail.

class test_class:
	x = 5

int a = 4 if input() else false
bool b = true if input() else 8
list l = [2,11] if input() else 8
dict d = {2:6} if input() else 8
lambda f = (lambda x: x + 5) if input() else 8
#test_class c = test_class() if input() else 8

print(a)
print(b)
print(l[1])
print(d[2])
print(f(7))
#print(c.x)
