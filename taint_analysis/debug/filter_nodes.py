# Imports
from __future__ import with_statement
import re 
import sys

#============= Regex for edges and node definitions ===========================
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )

# Captures node definition ( group 1 is node id )
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

#==================== Node and edge helper functions ==========================
# Get Id string of node source in edge
def get_edge_source( edge ):
    return ( edge.group( 1 ) )

# Get Id string of node destination in edge
def get_edge_dest( edge ):
    return ( edge.group( 2 ) )

# Get Id string of node definition
def get_node_id( node ):
    return ( node.group( 1 ) )

#============================== Main setup ====================================
if __name__ == '__main__':
    # Check command line args
    if ( 4 > len( sys.argv ) ) :
        print( 'Please use a correct-command line argument:' )
        print( '\tpython3 ' + sys.argv[0] + ' [node_list.txt] [dot_file.dot] [output_file.dot]' )
        exit( 1 )

    # Get file with list of sources and sinks and output json file
    node_list_file_name = sys.argv[1]
    dot_input_file_name = sys.argv[2]
    dot_output_file_name = sys.argv[3]

    # Initialize set for valid nodes
    valid_nodes = set()

    # Open node list file to get valid nodes
    with open( node_list_file_name, 'r' ) as input_file:
        for line in input_file:
            valid_nodes.add( line.strip() )

    # Open output file and write lines from input dot file containing only valid nodes
    with open( dot_output_file_name, 'w' ) as output_file:
        # Write dot file preamble
        output_file.write( 'digraph "SVFG" {\n' )
        output_file.write( '\tlabel="SVFG";\n' )

        # Open input file so we can copy over lines that contain valid nodes
        with open( dot_input_file_name, 'r' ) as input_file:

            for line in input_file:
                # Try and match regex on current line
                node = node_definition_regex.match( line )
                edge = edge_regex.match( line )

                valid_node_def = ( None != node \
                                   and get_node_id( node ) in valid_nodes )
                valid_edge = ( None != edge \
                               and get_edge_source( edge ) in valid_nodes \
                               and get_edge_dest( edge ) in valid_nodes )

                # If line contains valid nodes, write line to output file
                line_has_valid_nodes = valid_node_def or valid_edge
                if ( line_has_valid_nodes ):
                    output_file.write( line )

        # Write dot file epilog
        output_file.write( '}\n' )