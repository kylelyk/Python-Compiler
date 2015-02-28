print {9:0,True:False}[True]
print [0,1,2,3][-2]
obj = [
   [], 
   {3:True,True:5},
   {
      3:34,
      4:{4:4},
      7:{5:5},
      True:[0,1,2]
   },
   [2,23,234,2345]
]
print obj[2][True][1]
print obj[2][3]
print obj[3][3]
