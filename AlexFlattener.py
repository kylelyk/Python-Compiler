import compiler, sys, re

#Helper function, makes an assignment mode (which we make a lot of)
def make_assign(name, expr)
	return Assign(AssName(name, "OP_ASSIGN"),expr)

def flat_h(highvar, newAst, oldAst):
#returns the last variable assigned, and the updated new AST.
#oldAst should not be modified

	if isinstance(oldAst, Module):
		return flat_h(highvar, newAst, oldAst.node) 

	if isinstance(oldAst, Stmt):
		i = 0
		(n_highvar, n_newAst) = (highvar, newAst)
		while(isinstance(oldAst.nodes[i], ast)): 
			(n_highvar, n_newAst) = flat_h(n_highvar, n_newAst, oldAst.nodes[i])
			i = i + 1
		return (n_highvar, n_newAst)
		
	if isinstance(oldAst, Const):
		return (value, newAst)
	
	if isinstance(oldAst, Name):
		return (name, newAst)

	if isinstance(oldAst, Printnl):
		(n_hivar, n_newAst) = flat_h(highvar, newAst, oldAst.nodes)		
		n_printNode = Printnl(n_hivar, oldAst.dest)
		stmtNode = n_newAst.node.nodes
		stmtNode.append(n_printNode)
		return (n_hivar, n_newAst)
 	
	#The last variable returned should be the AssName
	if isinstance(oldAst, Assign):

	if isinstance(oldAst, AssName):
		return (oldAst.name, newAst)

	if isinstance(oldAst, Discard):
	
	#Currently assigns a temp variable to stuff like x = 1 + 2
	#Which works, but isn't particually elegant. 
	if isinstance(oldAst, Add):
		(left_highvar, partial_ast) = flat_h(highvar, newAst, oldAst.left)
		(right_highvar, combined_ast) = flat_h(highvar, partial_ast, oldAst.right)
		stmtNode = combined_ast.node.nodes
		newAdd = Add(Name(left_highvar),Name(right_highvar))
		stmtNode.append(make_assign(tmpx, newAdd))
		return (tmpx, combined_ast)
		#tmpx is placeholding for generic temp variable
		#Need to go back and fix later. 
		

	if isinstance(oldAst, UnarySub):
		(n_highvar, n_newAst) = flat_h(highvar, newAst, oldAst.expr)
		if (isinstance(n_highvar, int):
			newUnSub = UnarySub(Const(n_highvar))
			return (n_highvar,n_newAst)
		else:
			#If the direct node below isn't a constant, we'll return SOME variable.
			newUnSub = UnarySub(Name(n_highvar))
			stmtNode = n_newAst.node.nodes
			stmtNode.append(make_assign(tmpx,newUnSub))
			return (tmpx,n_newAst)		
			#tmpx is placeholding 
	
	#For now, we only have one function
	if isinstance(oldAst, CallFunc):
		stmtNode = newAst.node.nodes
		stmtNode.append(makeAssign(tmpx,oldAst))
		return (tmpx, newAst)
		#tmpx is placeholding
		
				
def flatten(ast): 
	retAst = Module([],Stmt([]))
	return flat_h(hivar, retAst, ast)
