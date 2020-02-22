# Imports
from __future__ import with_statement
import re 
import sys

# Specify sources and sinks
sources = set(["Node0x7f629345e2f0"])
# sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60", "Node0x7f62937f65e0", "Node0x7f629345e2f0", "Node0x7f6293bf4160", "Node0x7f62940c07f0"])
sinks = set(["Node0x7f62940e02b0"])

# Regex for edges and node definitions
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )
# Captures id of node definition
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

# Read dot file?
#f = open("./SVF/svfg_final.dot")
#graph = f.read().splitlines()
#f.seek(0)


class Source:
    def __init__(self):
        self.visited_nodes = []
        self.output_nodes = []
        self.source_node = 'fake_source_node_id' 
        self.sink_node = 'fake_sink_node_id'

def GSTSEP(cur_node, my_source):
    if cur_node in my_source.visited_nodes:
        my_source.output_nodes.remove(cur_node)
        return False
    else:
        my_source.visited_nodes += [cur_node]
    if is_sink(cur_node):
        my_source.sink_node = cur_node
        return True
    else:
        for x in get_connecting_nodes(cur_node):
            if x not in my_source.output_nodes:
                my_source.output_nodes += [x]
                if GSTSEP(x, my_source):
                    return True
        if cur_node == "Node_Start":
            print("Path from source to sink not found")
            return False
        my_source.output_nodes.remove(cur_node)
        return False

def find_missing_fusion(nodes):
    #what
    print('test')


def show_taint(cur_node, my_source):
    for x in get_connecting_nodes(cur_node):
        if x not in my_source.output_nodes:
            my_source.output_nodes += [x]
            show_taint(x, my_source)

def is_sink(node):
    return node in sinks

def is_leaf(node):
    return not (node in dot_dict)

def get_connecting_nodes(node):
    if node in dot_dict:
        return dot_dict[node]
    else:
        return []
        
def output_final_dot_graph(nodes):
    output_file = open('output.dot', 'w')
    output_file.write('digraph "SVFG" {\n')
    output_file.write('\tlabel="SVFG";\n')
    
    for x in graph:
        node_def = definition_regex.match(x)
        node_src = source_regex.match(x)
        node_dest = destination_regex.match(x)
        if (node_def != None and node_def.group(1) in nodes) or ((node_src != None and node_src.group(1) in nodes) and (node_dest != node_dest.group(1) in nodes)):
            output_file.write(x + '\n')
    output_file.write('}\n')


def check_for_circular_relationships():
    for x in dot_dict:
        for i in dot_dict[x]:
            if i == x:
                print("circuler relationship detected at node " + x)

#dot_dict = {}
#for line in f:
#    src = source_regex.match(line)
#    if src != None:
#        dot_dict[src.group(1)] = []
#f.seek(0)
#for line in f:
#    src = source_regex.match(line)
#    dest = destination_regex.match(line)
#    if dest != None:
#        dot_dict[src.group(1)] += [dest.group(1)]
#
#final_nodes = set()
#for x in sources:
#    print(x)
#    my_new_source = Source()
#    my_new_source.source_node = x
#    dot_dict["Node_Start"] = [x]
#    if sys.argv[1] == 'taint':
#        show_taint("Node_Start", my_new_source)
#    elif sys.argv[1] == 'sts':
##        GSTSEP("Node_Start", my_new_source)
#    final_nodes = final_nodes.union(my_new_source.output_nodes)
#output_final_dot_graph(final_nodes)

def get_edge_source( edge ):
    return ( edge.group( 1 ) )

def get_edge_dest( edge ):
    return ( edge.group( 2 ) )

def get_node_id( node ):
    return ( node.group( 1 ) )

if __name__ == '__main__':
    # Check command line args
    if ( ( len( sys.argv ) < 3 ) \
         or ( sys.argv[1] != 'taint' and sys.argv[1] != 'sts' ) ) :
        print( 'Please use a correct-command line argument, try\n\tpython3 ' + sys.argv[0] + ' [sts or taint] [file name]\n' )
        exit( 1 )

    # Get analysis type and file to analyze
    analysis_type = sys.argv[1]
    file_name = sys.argv[2]

    # Graph data
    graph_dict = {}

    # Open file and create graph structure to analyze
    with open( file_name, 'r' ) as input_file:
        for line in input_file:
            node = node_definition_regex.match( line )
            edge = edge_regex.match( line )
            
            if ( None != node ):
                node_id = get_node_id( node )
                graph_dict[node_id] = []
            
            elif ( None != edge ):
                src = get_edge_source( edge )
                dest = get_edge_dest( edge )

                graph_dict[src].append(dest)

    for key, value in graph_dict.items():
        print ( key, '->', value )

    # TODO: Implement taint and sts with graph traversal algorithms
    # TODO: based on output nodes modify the output file
