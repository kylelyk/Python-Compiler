int a = 3
a = 6
print a

bool b = true
b = false
print b

#AST: 
#Module(None, Stmt([Assign([AssName('a', ['OP_ASSIGN','INT'])], Const(3)), Assign([AssName('a', 'OP_ASSIGN')], Const(6)), Printnl([Name('a')], None), Assign([AssName('b', ['OP_ASSIGN','INT'])], Name('true')), Assign([AssName('b', 'OP_ASSIGN')], Name('false')), Printnl([Name('b')], None)]))
