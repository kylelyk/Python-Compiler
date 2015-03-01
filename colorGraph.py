#Color_Nodes have the following structures:
#1. Its adjacency List.
#2. A boolean array denotating whether an adjacent node has that color
#3. Its color
#4. Its saturation (the number of trues in #1 array)
#5. Whether it's "unspillable", apparently relevant in the third part.
# Unassigned color is -1, registers are 0-5, memory is 10.
       
reg_color = {"%eax":0, "%ecx": 1, "%edx": 2, "%ebx":3, "%esi":4, "%edi":5}

#Returns the key of the next node to be colored
def choose_next_node(graph, saturation, color, path):
	
	(next_node, max_sat) = ("NO FREE", -10)
	
	#If our path is empty, just pick a high priority node
	if(not path):
		for k in range(len(graph.keys())):
			c_node = graph.keys()[k]
        #unspillable nodes are given priority, followed by saturation.
			sat = graph[c_node][1]*10000 + saturation[c_node]
			is_colored = (color[c_node] != -1)
			if (sat > max_sat and not is_colored):
				(next_node, max_sat) = (c_node, sat)
		return next_node
		 
	adj_list = graph[path[0]][0]
	for adj_node in adj_list:
		is_colored = (color[adj_node] != -1)
		if (not is_colored):
			sat = graph[adj_node][1]*10000 + saturation[adj_node]
			is_colored = (color[adj_node] != -1)
			if sat > max_sat:
				(next_node, max_sat) = (adj_node, sat)
    
    #If there's no valid node at our location, go back a step in the path
    #And search for nodes there
	if (next_node == "NO FREE"):
		path.first() #Pops off first element of path (one we're looking at)
		next_node = choose_next_node(graph, saturation, color, path)
		
	return next_node
#Returns a map, w/ node names as key and color as info.
def color_graph(graph):
    #Starting location of "memory"
    to_mem = 10

    #1,2 and 6 are built into the nodes themselves.

    #3
    adj_colors = {}
    for i in range(len(graph.keys())):
        #False = No bordering node has that color assigned to it
        adj_colors[graph.keys()[i]] = [False, False, False, False, False, False]

    #4
    color = {}
    for i in range(len(graph.keys())):
        #False = No bordering node has that color assigned to it
        color[graph.keys()[i]] = -1

    #5
    saturation = {}
    for i in range(len(graph.keys())):
        saturation[graph.keys()[i]] = 0
        
    
    reg_color = {"%eax":0, "%ecx": 1, "%edx": 2, "ebx":3, "esi":4, "edi":5}

    node_count = len(graph)
    
    #We color special nodes first, if they exist.
    #Only first three should be spotted atm, but that can change.
    
    for i in range (len(reg_color.keys())):
        if reg_color.keys()[i] in graph:
            curr_node = reg_color.keys()[i]
            col = reg_color[reg_color.keys()[i]]
            color[curr_node] = col
            #Once colored, update the info of its neighbors.
            adj_list = graph[curr_node][0]
            for name in adj_list:
                adj_colors[name][col] = True
                saturation[name] += 1
            node_count -= 1
        
    #curr_node has the last node visited in the above loop


    #While a node isn't colored
    while(node_count > 0):
        path = []
        curr_node = choose_next_node(graph, saturation, color, path)
    
        for col in range(0,6):
            #Picks the first available color
            if adj_colors[curr_node][col] == False:
                color[curr_node] = col
                #Once colored, update the info of its neighbors.
                adj_list = graph[curr_node][0]
                for adj_node in adj_list:
                    adj_colors[adj_node][col] = True
                    saturation[adj_node] += 1
                break
        
            #If no colors are available, assign to a memory location
            elif col == 5:
                color[curr_node] = to_mem
                to_mem += 1
                #Assign to the free memory slot, then increment

        node_count -= 1

    return color
