# Imports
from __future__ import with_statement
import re 
import sys

# TODO: turn this into file input
# Specify sources and sinks
sources = set( ["Node0x55dbdfa1af10", "Node0x55dbdfa1afe0"] )
sinks = set( ["Node0x55dbdfa1c1b0", "Node0x55dbdfa36f20"] )

# Regex for edges and node definitions
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )
# Captures id of node definition
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

# TODO: check for loops in source to sink and taint
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

def source_to_sink( sources, output_nodes ):
    for node in sources:
        path = []
        find_paths( node, path, output_nodes )

def find_paths( curr_node, curr_path, output_nodes ):
    if ( is_sink( curr_node ) ):
        output_nodes.append( curr_node )
        return True
    elif ( is_leaf( curr_node ) ):
        return False
    else:
        found_path = False
        for child in get_child_nodes( curr_node ):
            if ( find_paths( child, curr_path.copy(), output_nodes ) ):
                found_path = True

        if ( found_path ):
            output_nodes.append( curr_node )

        return found_path

def output_final_dot_graph( valid_nodes, input_file_name ):
    with open( 'output.dot', 'w' ) as output_file:
        output_file.write('digraph "SVFG" {\n')
        output_file.write('\tlabel="SVFG";\n')

        with open( input_file_name, 'r' ) as input_file:
            for line in input_file:
                # Try and match regex on current line
                node = node_definition_regex.match( line )
                edge = edge_regex.match( line )

                line_has_valid_nodes = ( None != node and get_node_id( node ) in valid_nodes )
                line_has_valid_nodes = line_has_valid_nodes or \
                                       ( None != edge \
                                         and get_edge_source( edge ) in valid_nodes \
                                         and get_edge_dest( edge ) in valid_nodes )
                
                if ( line_has_valid_nodes ):
                    output_file.write( line + '\n' )

        output_file.write('}\n')
                    
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
        source_to_sink( sources, output_nodes )

    # Write to output file
    output_final_dot_graph( output_nodes, file_name )
