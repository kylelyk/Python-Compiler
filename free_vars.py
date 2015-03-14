#merges a list of sets into one set
def combine_set_list(set_list):
	#reduce is python's foldLeft function
    return reduce(lambda a,b: a | b, set_list, set([]))

def free_vars_stmt(stmt):
    fv = set([])
    bv = set([])
    for n in stmt.nodes:
        #In a statement, we need to keep track of the bound variables,
        #rather than just excluding them from the exp's free var list.
        if isinstance(n, Assign):
            fv = fv | free_vars(n.expr)
            for ass_node in n.nodes:
                bv = bv | set([ass_node.name])
        elif isinstance(n, Lambda) or isinstance(n,Function):
            fv = fv | free_vars(n.code)
            bv = bv | set(n.argnames)
        else:
            fv = fv | free_vars(n)
    return fv - bv
    
    
#returns a tuple of sets, one free_vars and one bound_vars
def free_vars(n):
    if isinstance(n, Module):
        return free_vars(n.node)
        #This should always return an empty set. (Useful for debug?)
        
    if isinstance(n,Stmt):
        return free_vars_stmt(n)
        
    if isinstance(n, Const):
		return (set([]))
    elif isinstance(n, Name):
		if n.name == 'True' or n.name == 'False':
			return set([])
		else:
			return set([n.name])
            
    elif isinstance(n, Printnl):
        printd('In Printnl path')
        return free_vars(n.nodes[0])
        
    elif isinstance(n, UnarySub):
        return free_vars(n.expr)
        
    elif isinstance(n, Add):
		return free_vars(n.left) | free_vars(n.right)
        
    elif isinstance(n, Discard):
        return free_vars(n.expr)
        
    elif isinstance(n, CallFunc):
		fv_args = [free_vars(e) for e in n.args]
		free_in_args = combine_set_list(fv_args)
		return (free_vars(n.node) | free_in_args) - set(['input'])
	#special casing input for the moment.
        
    elif isinstance(n, Assign):
        return free_vars(n.expr) - set(n.nodes)
    
    elif isinstance(n, Compare):
        return free_vars(n.expr) | free_vars(n.ops[0][1])
        
        
    elif isinstance(n, Or) or isinstance(n, And):
        fv = [free_vars(e) for e in n.nodes]
        return combine_set_list(fv)
    
    elif isinstance(n, Not):
        return free_vars(n.expr)
        
    elif isinstance(n, List):
        fv = [free_vars(e) for e in n.nodes]
        return combine_set_list(fv)
        
    elif isinstance(n, Dict):
        fv = [ free_vars(k) | free_vars(v) for (k, v) in n.items]
        return combine_set_list(fv)
        
    elif isinstance(n, Subscript):
        fv = [free_vars(sub) for sub in n.subs]
        return combine_set_list(fv) | free_vars(n.expr)
        
    elif isinstance(n, IfExp):
        return free_vars(n.test) | free_vars(n.then) | free_vars(n.else_)
   
    #Function declarations
    elif isinstance(n, Lambda) or isinstance(n,Function):
		return free_vars(n.code) - set(n.argnames) 
        #n.code is an expression w/ Lambda and a Stmt with Func
    elif isinstance(n, Return):
		return free_vars(n.value)
    
    else: 
        return set([])
