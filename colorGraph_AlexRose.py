#At the moment, I create a special graph just for the coloring, w/ metadata stored within the nodes.
#Originally I had a good reason for this, but that turned out unecessary as I worked through the problem
#So now there's no reason not to just store all the metadata in seperate dictionaries and leave the original graph alone.
#Which would probably be less of a headache.


#Color_Nodes have the following structures:
#1. Its adjacency List.
#2. A boolean array denotating whether an adjacement node has that color
#3. Its color
#4. Its saturation (the number of trues in #1 array)
#5. Whether it's "unspillable", apparently relevant in the third part.
# Unassigned color is -1, registers are 0-5, memory is 10.

to_mem = 10

class color_node:

    adj_list = {}
    adj_colors = [False, False, False, False, False, False]
    color = -1
    saturation = 0
    is_unspill = False

#Adds meta info to your original graph structure
#Also doesn't work atm.
def Graph_to_MetaInfoGraph(graph):

    meta_graph = {}
    for i in range(len(graph)):
        new_node = color_node()
        new_node.adj_list = graph[i]
        meta_graph.append(new_node)

    return Graph_to_MetaInfoGraph
        

def choose_next_node(graph):
    (next_node, max_sat) = (-1, -10)
    
    for k in range(len(graph)):
        #unspillable nodes are given priority, followed by saturation.
        sat = graph[k].is_unspill*10000 + graph[k].saturation
        is_colored = (graph[k].color != -1)
        if (sat > max_sat and !is_colored):
            (next_node, max_sat) = (adj_node, sat)

    return next_node
        

def color_graph(graph):

    node_count = len(graph)

    #While a node isn't colored
    while(node_count > 0):
        
        curr_node = choose_next_node(graph)
    
        for col in range(0,6):
            #Picks the first available color
            if (curr_node.adj_colors[col] = False):
                curr_node.color = col
                #Once colored, update the info of its neighbors.
                for k in range(len(curr_node.adj_list)):
                    curr_node.adj_list[k].adj_colors[col] = True
                    curr_node.adj_list[k].saturation += 1
                break
        
            #If no colors are available, assign to a memory location
            else if(col = 5):
                curr_node.color = to_mem
                #Placeholder for memory location name. At the moment, it assigns all the mem locations to "10".

        node_count -= 1

    return graph


###
##Ignore the below.           
###

#
    #1 and 2 are built into the nodes themselves.

    #3
 #   adj_colors = []
   # for i in range(len(graph)):
        #False = No bordering node has that color assigned to it
   #     adj_colors.append([False, False, False, False, False, False])

   # #4
   # color = []
    #for i in range(len(graph)):
   #     color.append(-1)

    #5
  #  saturation = []
   # for i in range(len(graph)):
   #     saturation.append(0)

    #6
   # is_unspillable = []
   # for i in range(len(graph)):
    #    is_unspillable.append(False)
        #This needs to be changed later, but for now nothing is unspillable
