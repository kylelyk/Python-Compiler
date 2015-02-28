x = 0
y = True
z = [0]
print 1 if x or y or z[99] else 0

x = 1
y = False
z = [0]
print 1 if x and y and z[99] else 0