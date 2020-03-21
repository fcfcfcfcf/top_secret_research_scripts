# Imports
from __future__ import with_statement
import json
import re 
import sys

# Global for logging
is_logging = False

# Increase recursive limit for large graphs
sys.setrecursionlimit( 500000 )

# Initialize empty sources and sinks sets
sources = set()
sinks = set()

# Initialize empty valid and visited nodes
output_nodes = set()
visited_nodes = set()

# Initialize empty set of seen cycles
cycles_seen = []

#============= Regex for edges and node definitions ===========================
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )

# Captures node definition ( group 1 is node id )
node_definition_regex = re.compile( "^\s*(.*) \[shape.*$" )

#==================== Node and edge helper functions ==========================
# Check if node is a sink
def is_sink( node ):
    return ( node in sinks )

# Check if node is a leaf
def is_leaf( node ):
    return ( [] == graph_dict[node] )

# Get connecting nodes from current node
def get_child_nodes( node ):
    return graph_dict[node] 

# Get Id string of node source in edge
def get_edge_source( edge ):
    return ( edge.group( 1 ) )

# Get Id string of node destination in edge
def get_edge_dest( edge ):
    return ( edge.group( 2 ) )

# Get Id string of node definition
def get_node_id( node ):
    return ( node.group( 1 ) )
 
#=============== Source to sink analysis helper functions =====================
# Check if any of the cycles seen while traversing the graph lead to a sink
def validate_cycles():
    for cycle in cycles_seen:
        last_node = cycle[-1]
        
        # If the node that lead to a cycle leads to sink, add all the nodes in
        # the cycle to the valid nodes set
        if ( last_node in output_nodes ):
            output_nodes.update( cycle )

#========================== Taint analysis functions ==========================
# Track traint through all nodes
def track_taint( current_nodes ):
    """ Track taint through nodes
    current_nodes: list of nodes to track taint through
        - initially this is the list of sources
    """
    # Loop through current nodes to track taint
    for node in current_nodes:
        # If already seen node, skip
        if ( node in output_nodes ):
            continue

        # Else add node to list and track taint through child nodes
        else:
            output_nodes.add( node )
            track_taint( get_child_nodes( node ) )

# Get nodes in paths from every source to every sink
def source_to_sink( sources ):
    """ Get valid nodes in paths from sources to sinks
    sources: list of source nodes

    Calls find_paths for each source node and passes in:
        - node: node id string
        - curr_path: each path being traversed will maintain a list of nodes
            it has passed

    curr_path is empty as there are no nodes in the current
        path yet
    """
    for node in sources:
        find_paths( node, [] )

# Find paths from source to sink
def find_paths( curr_node, curr_path ):
    """ Find paths from current node to all sinks if possible
    curr_node: node id string of current node in path
    curr_path: list of all nodes seen so far in traversal

    Algorithm:
        - Add current node to current path
        - Check if we have already seen the current node
            - If we have seen it already, add the cycle to the
                list of cycles seen
            - Return false ( we will check if this path leads to a sink
                after the graph traversal is completed )
        - If node is a sink
            - We want to save that node to the list of 
                valid nodes ( output_nodes )
            - There is a chance that the sink has children of its own that
                also lead to more sinks
                - As a result, we run find_paths on the children of the
                    sink
            - We then return true to indicate to all the nodes leading to
                the sink that they should be added to output_nodes
        - If node is a leaf
            - It has not led to a sink and therefore the path is not a 
                valid one and we should return false
                - This signals all the previous nodes to not add themselves
                    to output_nodes for this particular path 
        - If node is a neither a sink or leaf
                - We have to determine if it is a valid node
                    - The node is valid if any one of its children leads to a
                        sink
                - We can call find_path on each child node with
                    - If any of the child paths leads to a sink, we can add the
                        current node to output_nodes
    """
    # If logging, output node
    if ( is_logging ):
        print( curr_node )

    # Update current path with current node
    curr_path.append( curr_node )

    # Have I seen this node before
    if ( curr_node in visited_nodes ):
        # We must be in a cycle so add path to cycles_seen and return false
        cycles_seen.append( curr_path )
        return False

    # Mark current node as visited
    visited_nodes.add( curr_node )

    # Is current node a sink
    if ( is_sink( curr_node ) ):
        # Add node to output nodes list 
        output_nodes.add( curr_node )
        
        # Call find paths for each child node of sink
        # This is so we can get multiple sinks in a path
        for child in get_child_nodes( curr_node ):
            # Treat these paths as new trees since the previous path was valid
            find_paths( child, curr_path.copy() )
        
        # Indicate that the path found was valid
        return True
    
    # Is current node a leaf node
    elif ( is_leaf( curr_node ) ):
        # Indicate that the path is not valid since it did not reach a sink
        return False

    # If current node has children, find paths through them
    else:
        # Start with assuming no child leads to a sink
        has_found_path = False

        # Loop through each child node
        for child in get_child_nodes( curr_node ):
            # Check if path from child node leads to sink
            if ( find_paths( child, curr_path.copy() ) ):
                has_found_path = True

        # If any child led to a sink, add current node to path
        if ( has_found_path ):
            output_nodes.add( curr_node )

        # Return if any child node led to a sink
        return has_found_path

#====================== Create output file function ===========================
# Create output file with only valid nodes from analysis
def output_final_dot_graph( input_file_name, output_file_name ):
    # Open output file with write
    with open( output_file_name, 'w' ) as output_file:
        # Write dot file preamble
        output_file.write( 'digraph "SVFG" {\n' )
        output_file.write( '\tlabel="SVFG";\n' )

        # Open input file so we can copy over lines that contain valid nodes
        with open( input_file_name, 'r' ) as input_file:
            for line in input_file:
                # Try and match regex on current line
                node = node_definition_regex.match( line )
                edge = edge_regex.match( line )

                valid_node_def = ( None != node \
                                   and get_node_id( node ) in output_nodes )
                valid_edge = ( None != edge \
                               and get_edge_source( edge ) in output_nodes \
                               and get_edge_dest( edge ) in output_nodes )

                # If line contains valid nodes, write line to output file
                line_has_valid_nodes = valid_node_def or valid_edge
                if ( line_has_valid_nodes ):
                    output_file.write( line )

        # Write dot file epilog
        output_file.write( '}\n' )

#============================== Main setup ====================================
if __name__ == '__main__':
    # Check command line args
    if ( ( len( sys.argv ) < 4 ) \
         or ( sys.argv[1] != 'taint' and sys.argv[1] != 'sts' ) ) :
        print( 'Please use a correct-command line argument:' )
        print( '\tpython3 ' + sys.argv[0] + ' [sts, taint] [dot_file.dot] [ss_ids.json]' )
        exit( 1 )

    # Check if logging
    if ( 5 == len( sys.argv ) and '-log' == sys.argv[4] ):
        is_logging = True

    # Get analysis type, file to analyze and list of sources and sinks
    analysis_type = sys.argv[1]
    dot_file_name = sys.argv[2]
    sources_and_sinks_file_name = sys.argv[3]
    output_file_name = 'output-' + analysis_type + '.dot'

    # Graph data
    graph_dict = {}

    # Open file and create graph structure to analyze
    with open( dot_file_name, 'r' ) as input_file:
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

    # Read in sources and sinks
    with open( sources_and_sinks_file_name ) as sources_and_sinks_file:
        sources_and_sinks = json.load( sources_and_sinks_file )

    sources.update( sources_and_sinks['sources'] )
    sinks.update( sources_and_sinks['sinks'] )

    # Check if analysis is taint or sts
    if ( 'taint' == analysis_type ):
        track_taint( sources )
    else:
        source_to_sink( sources )

        # Check if any cycle seen while traversing graph leads to a sink
        # If it does, add those nodes to valid set
        validate_cycles()

    # Write to output file
    output_final_dot_graph( dot_file_name, output_file_name )
