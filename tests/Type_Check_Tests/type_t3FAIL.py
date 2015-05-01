bool b = false
a = 7
z = lambda x: 6
b = a + 5 + (-z(1)) #an integer
print b

#AST:
#Module(None, Stmt([Assign([AssName('b', ['OP_ASSIGN','BOOL'])], Name('false')), Assign([AssName('a', 'OP_ASSIGN')], Const(7)), Assign([AssName('z', 'OP_ASSIGN')], Lambda(['x'], [], 0, Const(6))), Assign([AssName('b', 'OP_ASSIGN')], Add((Add((Name('a'), Const(5))), UnarySub(CallFunc(Name('z'), [Const(1)], None, None))))), Printnl([Name('b')], None)]))
