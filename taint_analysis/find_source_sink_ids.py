# Imports
from __future__ import with_statement
import json
import re 
import sys

# Captures node definition ( group 1 is node id )
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

#==================== Node and edge helper functions ==========================
# Get Id string of node definition
def get_node_id( node ):
    return ( node.group( 1 ) )

#============================== Main setup ====================================
if __name__ == '__main__':
    # Check command line args
    if ( 4 > len( sys.argv ) ) :
        print( 'Please use a correct-command line argument:' )
        print( '\tpython3 ' + sys.argv[0] + ' [ss_func_names.txt] [dot_file.dot] [ss_ids.json]' )
        exit( 1 )

    # Get file with list of sources and sinks and output json file
    ss_func_file_name = sys.argv[1]
    dot_file_name = sys.argv[2]
    ss_output_file_name = sys.argv[3]

    # Initialize lists for source and sinks
    source_func_names = []
    sink_func_names = []

    sources = set()
    sinks = set()

    # Open sources and sinks file to get function names
    with open( ss_func_file_name, 'r' ) as input_file:
        sources_line = input_file.readline()
        source_func_names = sources_line.strip().split( ',' )

        sinks_line = input_file.readline()
        sink_func_names = sinks_line.strip().split( ',' )

    # Open dot file to get nodes ids for sources and sinks
    with open( dot_file_name, 'r' ) as dot_file:
        # Loop through each line in dot file
        for line in dot_file:
            # If line is a node definition
            node = node_definition_regex.match( line )
            if ( None != node ):
                # Check if node is a source
                for source in source_func_names:
                    if ( source in line ):
                        # Add to source list
                        sources.add( get_node_id( node ) )

                # Check if node is a sink
                for sink in sink_func_names:
                    if ( sink in line and node not in sources ):
                        # Add to sink list
                        sinks.add( get_node_id( node ) )

    # Output node ids to json files
    output_data = { 'sources': list( sources ), 'sinks': list( sinks ) }
    with open( ss_output_file_name, 'w' ) as output_file:
        json.dump( output_data, output_file, indent=4 )