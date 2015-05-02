#Modify the input file to make cases pass or fail:
#1 for pass, 0 for fail.


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

#AST:
#Module(None, Stmt([Assign([AssName('a', ['OP_ASSIGN','INT'])], IfExp(CallFunc(Name('input'), [], None, None), Const(4), Name('false'))), Assign([AssName('b', ['OP_ASSIGN','BOOL'])], IfExp(CallFunc(Name('input'), [], None, None), Name('true'), Const(8))), Assign([AssName('l', ['OP_ASSIGN','LIST'])], IfExp(CallFunc(Name('input'), [], None, None), List([Const(2), Const(11)]), Const(8))), Assign([AssName('d', ['OP_ASSIGN','DICT'])], IfExp(CallFunc(Name('input'), [], None, None), Dict([(Const(2), Const(6))]), Const(8))), Assign([AssName('f['OP_ASSIGN','LAMBDA'])], IfExp(CallFunc(Name('input'), [], None, None), Lambda(['x'], [], 0, Add((Name('x'), Const(5)))), Const(8))), Printnl([Name('a')], None), Printnl([Name('b')], None), Printnl([Subscript(Name('l'), 'OP_APPLY', [Const(1)])], None), Printnl([Subscript(Name('d'), 'OP_APPLY', [Const(2)])], None), Printnl([CallFunc(Name('f'), [Const(7)], None, None)], None)]))
