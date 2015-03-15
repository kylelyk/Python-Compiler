####Put this in compile.py when uniquify is intergrated

class GenName:
    def __init__(self):
        self.n = 0
    def inc(self):
        self.n += 1
        return self
    def new_name(self, name): 
        self.inc() 
        return name + "_" + str(self.n)

gen = GenName()
###


#makes the variable mapping
def make_name_dict(b_set):
    name_dict = {}
    for name in b_set:
        name_dict[name] = gen.new_name(name)
    return name_dict
    

def combine_set_list(set_list):
	#reduce is python's foldLeft function
    return reduce(lambda a,b: a | b, set_list, set([]))

#Two things we're trying to find in uni_trav
#a. The bound assign variables i.e The bound variables exluding those in function arguments.
#b. The functions themselves, which we apply uniquify to them.
def uni_trav(n, b_list = set([])):
   
    if isinstance(n, Module):
        return uni_trav(n.node)
   
    elif isinstance(n,Stmt):
        bd_args = [uni_trav(e) for e in n.nodes]
        return combine_set_list(bd_args)
        
    elif isinstance(n, Const):
		return (set([]))
    
    elif isinstance(n, Name):
		return (set([]))
            
    elif isinstance(n, Printnl):
        return uni_trav(n.nodes[0])
        
    elif isinstance(n, UnarySub):
        return uni_trav(n.expr)
        
    elif isinstance(n, Add):
		return uni_trav(n.left) | uni_trav(n.right)
        
    elif isinstance(n, Discard):
        return uni_trav(n.expr)
        
    elif isinstance(n, CallFunc):
		bd_args = [uni_trav(e) for e in n.args]
		bound_in_args = combine_set_list(bd_args)
		return (uni_trav(n.node) | bound_in_args)
        
    elif isinstance(n, Assign):
        bv = set([])
        for ass_node in n.nodes:
                bv = bv | set([ass_node.name])
        return bv | uni_trav(n.expr)
        
    elif isinstance(n, Compare):
        return uni_trav(n.expr) | uni_trav(n.ops[0][1])
        
    elif isinstance(n, Or) or isinstance(n, And):
        bv = [uni_trav(e) for e in n.nodes]
        return combine_set_list(bv)
    
    elif isinstance(n, Not):
        return uni_trav(n.expr)
        
    elif isinstance(n, List):
        bv = [uni_trav(e) for e in n.nodes]
        return combine_set_list(bv)
        
    elif isinstance(n, Dict):
        bv = [ uni_trav(k) | uni_trav(v) for (k, v) in n.items]
        return combine_set_list(bv)
        
    elif isinstance(n, Subscript):
        bv = [uni_trav(sub) for sub in n.subs]
        return combine_set_list(bv) | uni_trav(n.expr)
        
    elif isinstance(n, IfExp):
        return uni_trav(n.test) | uni_trav(n.then) | uni_trav(n.else_)
   
    #We want to do the renaming inside a function BEFORE we rename in the larger scope
    elif isinstance(n, Lambda) or isinstance(n,Function):
        bd_list = set(n.argnames)
        func_dict = uniquify_wrap(n.code, bd_list)
        #And rename the arguments to whatever we named inside uni. wrap 
        new_arg_list = [func_dict[e] for e in n.argnames if e in func_dict]
        n.argnames = new_arg_list
        return set([])
    elif isinstance(n, Return):
		return uni_trav(n.value)
    
    else: 
        return set([])

def rename(n, name_dict):
    #Name and Assign are the only nodes in which something happens
    if isinstance(n, Name):
        if n.name in name_dict:
            n.name = name_dict[n.name]
            
    elif isinstance(n, Assign):
        rename(n.expr, name_dict)
        for ass_node in n.nodes:
                if ass_node.name in name_dict:
                    ass_node.name = name_dict[ass_node.name]
                    
    #The rest of this is just traversal
   
    elif isinstance(n, Module):
        rename(n.node, name_dict)
   
    elif isinstance(n,Stmt):
        for e in n.nodes:
            rename(e, name_dict)
            
    elif isinstance(n, Const):
        return

    elif isinstance(n, Printnl):
        return rename(n.nodes[0], name_dict)
        
    elif isinstance(n, UnarySub):
        rename(n.expr, name_dict)
        
    elif isinstance(n, Add):
      rename(n.left, name_dict) 
      rename(n.right, name_dict)
        
    elif isinstance(n, Discard):
        rename(n.expr, name_dict)
        
    elif isinstance(n, CallFunc):
        for e in n.args:
            rename(e, name_dict)
        rename(n.node, name_dict)
        
    elif isinstance(n, Compare):
        rename(n.expr, name_dict)
        rename(n.ops[0][1], name_dict)
        
    elif isinstance(n, Or) or isinstance(n, And):
        for e in n.nodes:
            rename(e, name_dict)
    
    elif isinstance(n, Not):
        rename(n.expr, name_dict)
        
    elif isinstance(n, List):
        for e in n.nodes:
            rename(e, name_dict)
        
    elif isinstance(n, Dict):
        for (k,v) in n.items:
            rename(k, name_dict)
            rename(v, name_dict)
        
    elif isinstance(n, Subscript):
        for sub in n.subs:
            rename(sub, name_dict)
        rename(n.expr, name_dict)
        
    elif isinstance(n, IfExp):
        rename(n.test, name_dict)
        rename(n.then, name_dict)
        rename(n.else_, name_dict)
   
    #Function declarations
    elif isinstance(n, Lambda) or isinstance(n,Function):
        #The arguments should already be renamed, so we skip checking them
        rename(n.code, name_dict) 
    elif isinstance(n, Return):
		rename(n.value, name_dict)

def uniquify_wrap(n, b_list = set([])):
    b_list = uni_trav(n) | b_list
    name_dict = make_name_dict(b_list)
    rename(n,name_dict)
    return name_dict
    

def uniquify(n):
    return uniquify_wrap(n)
