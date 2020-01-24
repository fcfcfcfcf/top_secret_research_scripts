import re 

f = open("./SVF/callgraph_final.dot")
graph = f.read().splitlines()

sources = set(["Node0x7f4c7e57bcd0"])
sinks = set(["Node0x7f4c7e59d870"])

destination_regex = re.compile("^.*?-> (.*)\[color.*$")
definition_regex = re.compile("^\s+(.*) \[shape.*$")
source_regex = re.compile("^\s+(.*):.* ->.*\[color.*$")

def GSTSEP(curEdge, edges):
    if connectsToSink(curEdge):
        return edges + curEdge
    elif isLeaf(curEdge):
        return []
    else:
        for x in getConnectingEdges(curEdge):
            foundEdges = GSTSEP(x, edges + curEdge)
            if foundEdges != []:
                return foundEdges
        return []


def connectsToSink(edge):
    curEdge = destination_regex.match(edge)
    return (curEdge is not None) and (curEdge.group(1) in sinks)
    

def isLeaf(edge):
    curEdge = destination_regex.match(edge)
    for x in range(len(graph)):
        node_def = destination_regex.match(graph[x])
        if (node_def is not None) and (node_def.group(1) == curEdge.group(1)):
            if definition_regex.match(graph[x+1]) is not None:
                return True
    return False

def getConnectingEdges(edge):
    edges = []
    curEdge = destination_regex.match(edge)
    for x in range(len(graph)):
        node_src = source_regex.match(graph[x])
        if (node_src is not None) and (node_src.group(1) == curEdge.group(1)):
            edges += graph[x]
    return edges

def getDefinitions(edges):
    defs = []
    i = 0
    for x in edges:
        #while(graph[i])
        edge_src = source_regex.match(x)
        edge_dest = destination_regex.match(x)
        while definition_regex(graph[i]) != edge_src.group(1):
            i += 1
        defs += graph[i]
        
def output_final_dot_graph(edges):
    output_file = open('output.dot', 'w')
    nodes = get_nodes_from_edges(edges)
    
    for x in graph:
        edge_src = source_regex.match(x)
        edge_dest = destination_regex.match(x)
        node_def = definition_regex.match(x)

        if ( (edge_src != None) and (edge_src.group(1) in nodes) ) \
            or ( (edge_dest != None) and (edge_dest.group(1) in nodes) ) \
            or ( (node_def != None) and (node_def.group(1) in nodes) ):
                output_file.write(x + '\n')

def get_nodes_from_edges(edges):
    nodes = set()
    for edge in edges:
        edge_src = source_regex.match(edge)
        edge_dest = destination_regex.match(edge)

        if (edge_src != None):
            nodes.add(edge_src.group(1))
        
        if(edge_dest != None):
            nodes.add(edge_dest.group(1))
        
    return nodes

final_edges = set()
for x in sources:
    first_edge = x + ":s0 -> " + x + "[color=black];"
    final_edges = final_edges.union(GSTSEP(first_edge, []))

output_final_dot_graph(final_edges)