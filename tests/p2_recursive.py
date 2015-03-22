def rec(x, stop):
	return rec(x+1,stop) + x if x != stop else 0
y = input()
y = y if y > 0 else 42
print(rec(0,input()))
