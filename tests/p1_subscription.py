print {9:0,true:false}[true]
print [0,1,2,3][-2]
obj = [
   [], 
   {3:true,true:5},
   {
      {3:4}:34,
      4:{4:4},
      []:{5:5},
      [true,5,9]:[0,1,2]
   },
   [2,23,234,2345]
]
print obj[2][[true,5,9]][1]
print obj[2][{3:4}]
print obj[3][3]