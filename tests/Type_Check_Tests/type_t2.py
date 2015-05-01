int a = (3 if input() else false)
print a

#AST:
#Module(None, Stmt([Assign([AssName('a', ['OP_ASSIGN','INT'])], IfExp(CallFunc(Name('input'), [], None, None), Const(3), Name('false'))), Printnl([Name('a')], None)]))
