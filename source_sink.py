# Imports
from __future__ import with_statement
import re 
import sys

# TODO: turn this into file input
# Specify sources and sinks
sources = set( ["Node0x7f629345e2f0"] )
sources_old = set( [
                    "Node0x7f62940fa5c0",
                    "Node0x7f6294096c10",
                    "Node0x7f6294275a60",
                    "Node0x7f62937f65e0",
                    "Node0x7f629345e2f0",
                    "Node0x7f6293bf4160",
                    "Node0x7f62940c07f0"
                   ] )
sinks = set( ["Node0x7f62940e02b0"] )

# Regex for edges and node definitions
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )
# Captures id of node definition
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

class def GSTSEP(cur_node, my_source):
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

#==============================================================================

def is_sink( node ):
    return ( node in sinks )

def is_leaf( node ):
    return ( [] == graph_dict[node] )

def get_child_nodes( node ):
    return graph_dict[node] 

def get_edge_source( edge ):
    return ( edge.group( 1 ) )

def get_edge_dest( edge ):
    return ( edge.group( 2 ) )

def get_node_id( node ):
    return ( node.group( 1 ) )

def track_taint( current_nodes, output_nodes ):
    for node in current_nodes:
        output_nodes.append( node )
        track_taint( get_child_nodes( node ), output_nodes )

#=============

def find_missing_fusion(nodes):
    #what
    print('test')

if __name__ == '__main__':
    # Check command line args
    if ( ( len( sys.argv ) < 3 ) \
         or ( sys.argv[1] != 'taint' and sys.argv[1] != 'sts' ) ) :
        print( 'Please use a correct-command line argument' )
        print( '\tpython3 ' + sys.argv[0] + ' [sts or taint] [file name]' )
        exit( 1 )

    # Get analysis type and file to analyze
    analysis_type = sys.argv[1]
    file_name = sys.argv[2]

    # Graph data
    graph_dict = {}

    # Open file and create graph structure to analyze
    with open( file_name, 'r' ) as input_file:
        for line in input_file:
            # Try and match regex on current line
            node = node_definition_regex.match( line )
            edge = edge_regex.match( line )
            
            # If Node definition, create empty list of edges 
            if ( None != node ):
                node_id = get_node_id( node )
                graph_dict[node_id] = []

            # Else if is an edge, add destination node to edge list
            elif ( None != edge ):
                src = get_edge_source( edge )
                dest = get_edge_dest( edge )

                graph_dict[src].append(dest)

    # Create list of valid output nodes
    output_nodes = []

    # Check if analysis is taint or sts
    if ( 'taint' == analysis_type ):
        track_taint( sources, output_nodes )
    else:
        print( "lol" )
    # TODO: Implement sts with graph traversal algorithms
    # TODO: based on output nodes modify the output file
