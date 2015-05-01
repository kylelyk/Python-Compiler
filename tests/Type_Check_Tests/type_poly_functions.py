def bool_or_int(): 
	return 3 if input() else false
	
int a = bool_or_int()
bool b = bool_or_int()

print a
print b

#AST:
#Module(None, Stmt([Function(None, 'bool_or_int', (), (), 0, None, Stmt([Return(IfExp(CallFunc(Name('input'), [], None, None), Const(3), Name('false')))])), Assign([AssName('a', ['OP_ASSIGN','INT'])], CallFunc(Name('bool_or_int'), [], None, None)), Assign([AssName('b', ['OP_ASSIGN', 'BOOL'])], CallFunc(Name('bool_or_int'), [], None, None)), Printnl([Name('a')], None), Printnl([Name('b')], None)]))
