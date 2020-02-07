import re 
import sys

if sys.argv[1] != 'taint' and sys.argv[1] != 'sts':
    print('please use a correct-command line argument, try\npython3 source_sink.py sts\nor\npython3 source_sink.py taint\n')
    exit(42069)

sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60"])
sinks = set(["Node0x7f62940e02b0"])

destination_regex = re.compile("^.*? -> (.*)\[style.*$")
definition_regex = re.compile("^\s*(.*) \[shape.*$")
source_regex = re.compile("^\s*(.*?)(?::.*)? -> .*\[style.*$")

f = open("./SVF/svfg_final.dot")
graph = f.read().splitlines()
f.seek(0)

class Source:
    def __init__(self):
        self.visited_edges = []
        self.output_edges = []

def GSTSEP(cur_edge, my_source):
    if cur_edge in my_source.visited_edges:
        my_source.output_edges.remove(cur_edge)
        return False
    else:
        my_source.visited_edges += [cur_edge]
    print(cur_edge)
    if is_sink(cur_edge):
        return True
    else:
        for x in getConnectingEdges(cur_edge):
            if x not in my_source.output_edges:
                my_source.output_edges += [x]
                if GSTSEP(x, my_source):
                    return True
        if cur_edge == "Node_Start":
            print("Path from source to sink not found")
            exit()
        my_source.output_edges.remove(cur_edge)
        return False

def show_taint(cur_edge, my_source):
    for x in getConnectingEdges(cur_edge):
        if x not in my_source.output_edges:
            my_source.output_edges += [x]
            show_taint(x, my_source)

def is_sink(edge):
    return edge in sinks

def isLeaf(edge):
    return not (edge in dot_dict)

def getConnectingEdges(edge):
    if edge in dot_dict:
        return dot_dict[edge]
    else:
        return []
        
def output_final_dot_graph(edges):
    output_file = open('output.dot', 'w')
    output_file.write('digraph "SVFG" {\n')
    output_file.write('\tlabel="SVFG";\n')
    
    for x in graph:
        node_def = definition_regex.match(x)
        node_src = source_regex.match(x)
        node_dest = destination_regex.match(x)
        if (node_def != None and node_def.group(1) in edges) or ((node_src != None and node_src.group(1) in edges) and (node_dest != node_dest.group(1) in edges)):
            output_file.write(x + '\n')
    output_file.write('}\n')


def check_for_circular_relationships():
    for x in dot_dict:
        for i in dot_dict[x]:
            if i == x:
                print("circuler relationship detected at node " + x)

dot_dict = {}
for line in f:
    src = source_regex.match(line)
    if src != None:
        dot_dict[src.group(1)] = []
f.seek(0)
for line in f:
    src = source_regex.match(line)
    dest = destination_regex.match(line)
    if dest != None:
        dot_dict[src.group(1)] += [dest.group(1)]

final_nodes = set()
for x in sources:
    my_new_source = Source()
    dot_dict["Node_Start"] = [x]
    if sys.argv[1] == 'taint':
        show_taint("Node_Start", my_new_source)
    elif sys.argv[1] == 'sts':
        GSTSEP("Node_Start", my_new_source)
    final_nodes = final_nodes.union(my_new_source.output_edges)
output_final_dot_graph(final_nodes)