#Color_Nodes have the following structures:
#1. Its adjacency List.
#2. A boolean array denotating whether an adjacement node has that color
#3. Its color
#4. Its saturation (the number of trues in #1 array)
#5. Whether it's "unspillable", apparently relevant in the third part.
# Unassigned color is -1, registers are 0-5, memory is 10.

to_mem = 10

'''class color_node:

    adj_list = {}
    adj_colors = [False, False, False, False, False, False]
    color = -1
    saturation = 0
    is_unspill = False
'''        

#Returns the key of the next node to be colored
def choose_next_node(graph, saturation, color):
    (next_node, max_sat) = ("NO FREE NODE", -10)
    
    for k in range(len(graph.keys())):
        c_node = graph.keys()[k]
        #unspillable nodes are given priority, followed by saturation.
        sat = graph[c_node][1]*10000 + saturation[c_node]
        is_colored = (color[c_node] != -1)
        if (sat > max_sat and not is_colored):
            (next_node, max_sat) = (c_node, sat)

    return next_node
        

def color_graph(graph):

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


    node_count = len(graph)

    #While a node isn't colored
    while(node_count > 0):
        
        curr_node = choose_next_node(graph, saturation, color)
    
        for col in range(0,6):
            #Picks the first available color
            if (adj_colors[curr_node] = False):
                color[curr_node] = col
                #Once colored, update the info of its neighbors.
		        adj_list = graph[curr_node][0]
                for k in range(len(adj_list)):
                    adj_colors[adj_list[k]][col] = True
                    saturation[adj_list[k]] += 1
                break
        
            #If no colors are available, assign to a memory location
            elif (col = 5):
                color[curr_node] = to_mem
                #Placeholder for memory location name. At the moment, it assigns all the mem locations to "10".

        node_count -= 1

    return color
