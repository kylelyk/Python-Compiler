
reg_color = {"%eax":0, "%ecx":1, "%edx":2, "%ebx":3, "%esi":4, "%edi":5, "%esp":6, "%ebp":7}
reg_map =   {0:"%eax", 1:"%ecx", 2:"%edx", 3:"%ebx", 4:"%esi", 5:"%edi", 6:"%esp", 7:"%ebp"}
memStart = 10

def color_graph(graph):
    #Starting location of "memory"

    #Dictionary of sets of ints
    adj_colors = {}
    #Dictionary of ints
    color = {}
    #Dictionary of ints
    saturation = {}
    for var in graph:
        adj_colors[var] = set([])
        # Unassigned color is -1, registers are 0-5, memory is 10.
        color[var] = -1
        saturation[var] = 10000*graph[var][1]
    
    #assign locations to registers
    for reg, c in reg_color.iteritems():
        if reg in color:
            color[reg] = c
            for neighbor in graph[reg][0]:
                saturation[neighbor] += 1
                adj_colors[neighbor].add(c)
            del saturation[reg]
    
    while len(saturation):
        #find correct color
        n = max(saturation, key=saturation.get)
        adj = adj_colors[n]
        i = 0
        while True:
            if 5 < i < memStart:
                i += 1
                continue
            if i not in adj_colors[n]:
                #found it, loop through neighbors
                color[n] = i
                for neighbor in graph[n][0]:
                    if i not in adj_colors[neighbor]:
                        if neighbor in saturation:
                            saturation[neighbor] += 1
                        adj_colors[neighbor].add(i)
                break
            i += 1
        del saturation[n]
    return color