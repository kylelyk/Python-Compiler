same_a  = [0,2,3]
same_b  = [0,2,3]

print (same_a is same_b)
print (same_a == same_b)

same_a[0] = 1
print (same_a[0] == same_b[0])

#aliasing

alias_a = [0,1,2]

alias_b = alias_a
pritn (alias_a is alias_b)

