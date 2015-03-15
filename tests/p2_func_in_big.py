listA = [lambda a: a+1,lambda b: b + 7]
print(listA[1](2))

dictA = {1: lambda a: a + a, 5: lambda a: a+8}
print(dictA[1](25))
