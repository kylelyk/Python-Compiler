def rec(x, stop):
	return rec(x+1,stop) + x if x != stop else 0
print(rec(0,input()))
