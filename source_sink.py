import re 

f = open("./SVF/svfg_final.dot")
graph = f.read().splitlines()

sources = set(["Node0x7ffff32794e0"])
sinks = set(["Node0x7ffff34baa90"])

destination_regex = re.compile("^.*? -> (.*)\[style.*$")
definition_regex = re.compile("^\s*(.*) \[shape.*$")
source_regex = re.compile("^\s*(.*) -> .*\[style.*$")

def GSTSEP(curEdge, edges):
    if connectsToSink(curEdge):
        return edges + [curEdge]
    elif isLeaf(curEdge):
        return []
    else:
        for x in getConnectingEdges(curEdge):
            foundEdges = GSTSEP(x, edges + [curEdge])
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
        if (node_def is not None and curEdge is not None) and (node_def.group(1) == curEdge.group(1)):
            if definition_regex.match(graph[x+1]) is not None:
                return True
    return False

def getConnectingEdges(edge):
    edges = []
    curEdge = destination_regex.match(edge)
    for x in range(len(graph)):
        node_src = source_regex.match(graph[x])
        if (node_src is not None and curEdge is not None) and (node_src.group(1) == curEdge.group(1)):
            edges += [graph[x]]
    return edges
        
def output_final_dot_graph(edges):
    output_file = open('output.dot', 'w')
    nodes = get_nodes_from_edges(edges)
    
    for x in graph:
        node_def = definition_regex.match(x)
        if (node_def != None and node_def.group(1) in nodes) or (x in edges):
            output_file.write(x + '\n')
        #if ( (edge_src != None) and (edge_src.group(1) in nodes) ) \
         #   or ( (edge_dest != None) and (edge_dest.group(1) in nodes) ) \
          #  or ( (node_def != None) and (node_def.group(1) in nodes) ):
           #     output_file.write(x + '\n')

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
    first_edge = x + " -> " + x + "[style=solid];"
    final_edges = final_edges.union(GSTSEP(first_edge, []))

output_final_dot_graph(final_edges)