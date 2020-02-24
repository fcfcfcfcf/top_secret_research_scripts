# Imports
from __future__ import with_statement
import json
import re 
import sys

# Initialize empty sources and sinks sets
sources = set()
sinks = set()

#============= Regex for edges and node definitions ===========================
# Capture group 1 is source node id and group 2 is destination node id
edge_regex = re.compile( "^\s*(.*?)(?::.*)? -> (.*)\[style.*$" )

# Captures id of node definition
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
# Check if cycle is a shifted version of existing cycle
def is_shifted_cycle( test_cycle, cycles_seen ):
    # For each stored cycle
    for cycle in cycles_seen:
        # Convert arrays of nodes into strings
        test_cycle_str = ''.join( test_cycle )
        cycle_str = ''.join( cycle )

        # If test cycle is a substring of cycle string * 2
        # then it is a shifted cycle
        # Ex. test_cycle = cab, cycle_str = abc
        # cycle_str * 2 = abcabc
        # test_cycle is a substring
        if ( test_cycle_str in ( cycle_str * 2 ) ):
            return True

    # If test cycle is not a shifted version of the stored cycles
    return False

# Check if path is entering a repeated loop
# ie. if it is looping over a loop it has already traversed
def is_path_in_repeated_loop( path, cycles ):
    # Check for each seen cycle
    for cycle in cycles:
        path_len = len( path )
        cycle_len = len( cycle )
        
        # Check if end of current path is equal to a cycle already seen
        end_of_path = path[( path_len - cycle_len ):path_len]
        if ( cycle == end_of_path ):
            return True

    return False
 
#========================== Taint analysis functions ==========================
# Track traint through all nodes
def track_taint( current_nodes, output_nodes ):
    """ Track taint through nodes
    current_nodes: list of nodes to track taint through
        - initially this is the list of sources
    output_nodes: list of nodes in paths from sources
    """
    # Loop through current nodes to track taint
    for node in current_nodes:
        # If already seen node, skip
        if ( node in output_nodes ):
            continue

        # Else add node to list and track taint through child nodes
        else:
            output_nodes.append( node )
            track_taint( get_child_nodes( node ), output_nodes )

# Get nodes in paths from every source to every sink
def source_to_sink( sources, output_nodes ):
    """ Get valid nodes in paths from sources to sinks
    sources: list of source nodes
    output_nodes: list of nodes that will contain all nodes in path
        from sources to sinks

    Calls find_paths for each source node and passes in:
        - node: node id string
        - curr_path: each path being traversed will maintain a list of nodes
            it has passed
        - output_nodes: list of nodes in all paths
        - cycles_seen: list of cycles that have been seen while traversing a
            path so we can avoid infinite loops

    curr_path and cycles_seen are empty as there are no nodes in the current
    path yet and there have been no cycles yet
    """
    for node in sources:
        find_paths( node, [], output_nodes, [] )

# Find paths from source to sink
def find_paths( curr_node, curr_path, output_nodes, cycles_seen ):
    """ Find paths from current node to all sinks if possible
    curr_node: node id string of current node in path
    curr_path: list of all nodes seen so far in traversal
    output_nodes: list of all nodes in valid paths from sources to sinks
    cycles_seen: list of all cycles seen in current path
        ex. cycles_seen = [['a', 'b', 'c'], ['e', 'f', 'g', 'h']]

    Algorithm:
        - Add current node to current path
        - Current node falls into one of three cases:
            1) Node is a sink
                - If node is a sink, we want to save that node to the list of
                valid nodes ( output_nodes )
                - There is a chance that the sink has children of its own that
                also lead to more sinks
                    - As a result, we run find_paths on the children of the
                    sink as though they were the root of their own tree
                    since the path above them is a valid one
                - We then return true to indicate to all the nodes leading to
                the sink that they should be added to output_nodes since they
                lead to a sink
            2) Node is a leaf
                - If the node is a leaf, it has not led to a sink and therefore
                the path is not a valid one and we should return false
                    - This signals all the previous nodes to not add themselves
                    to output_nodes for this particular path 
            3) Node is a neither a sink or leaf
                - If the node is not a sink or a leaf, then we have to
                determine if it is a valid node
                    - The node is valid if any one of its children leads to a
                    sink
                - However, before we can track taint through each child node
                we need to check to make sure we do not encounter any cycles
                that could cause infinite loops:
                    i) We first check if moving to the next child node results
                    in retraversing a cycle in the graph
                        - If we are retraversing a cycle, then we want to skip
                        the current path as we know we have already travelled
                        this loop
                    ii) We then check if moving to the next child node creates
                    a cycle we have not traversed yet
                        - Add list of nodes in cycle to cycles seen only if
                        it is not a shifted version of a cycle already in
                        cycles_seen
                - Afterwards, we can call find_path on the child node with
                copies of the current path and cycles seen in current path
                - If any of the child paths leads to a sink, we can add the
                current node to output_nodes  
    """
    # Update current path with current node
    curr_path.append( curr_node )

    # Current node is a sink
    if ( is_sink( curr_node ) ):
        # Add node to output nodes list 
        output_nodes.append( curr_node )
        
        # Call find paths for each child node of sink
        # This is so we can get multiple sinks in a path
        for child in get_child_nodes( curr_node ):
            # Treat these paths as new trees since the previous path was valid
            # Copy current path and cycles seen so that each path has its own
            # copy to modify and keep track of
            path_copy = curr_path.copy()
            cycles_copy = cycles_seen.copy() 
            find_paths( child, path_copy, output_nodes, cycles_copy )
        
        # Indicate that the path found was valid
        return True
    
    # Current node is a leaf node
    elif ( is_leaf( curr_node ) ):
        # Indicate that the path is not valid since it did not reach a sink
        return False

    # If current node has children, find paths through them
    else:
        # Start with assuming no child leads to a sink
        has_found_path = False

        # Loop through each child node
        for child in get_child_nodes( curr_node ):
            next_path = curr_path + [child]
            # Check if moving to child results in repeated loop
            # and skip current path if it is
            if ( is_path_in_repeated_loop( next_path, cycles_seen ) ):
                continue

            # Check if we have traversed a new loop
            # Next node has already been seen in current path
            if ( child in curr_path ):
                start_of_cycle_idx = curr_path.index( child )
                end_of_cycle_idx = len( curr_path )

                # Get cycle from current path
                cycle = curr_path[start_of_cycle_idx:end_of_cycle_idx]

                # If cycle is not a shifted version of an existing cycle
                # add it to the seen cycles list
                if ( False == is_shifted_cycle( cycle, cycles_seen ) ):
                    cycles_seen.append( cycle )

            # Check if path from child node leads to sink
            # Copy current path and cycles seen so that each path has its own
            # copy to modify and keep track of
            path_copy = curr_path.copy()
            cycles_copy = cycles_seen.copy()
            if ( find_paths( child, path_copy, output_nodes, cycles_copy ) ):
                has_found_path = True

        # If any child led to a sink, add current node to path
        if ( has_found_path ):
            output_nodes.append( curr_node )

        # Return if any child node led to a sink
        return has_found_path

# TODO: should this be a new python script that analyzes the output dot?
def find_missing_fusion(nodes):
    #what
    print('test')

#====================== Create output file function ===========================

# Create output file with only valid nodes from analysis
def output_final_dot_graph( valid_nodes, input_file_name, output_file_name ):
    # Open output file with write
    with open( output_file_name, 'w' ) as output_file:
        # Write dot file preamble
        output_file.write('digraph "SVFG" {\n')
        output_file.write('\tlabel="SVFG";\n')

        # Open input file so we can copy over lines that contain valid nodes
        with open( input_file_name, 'r' ) as input_file:
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
                    output_file.write( line + '\n' )

        # Write dot file epilog
        output_file.write('}\n')

#============================== Main setup ====================================
if __name__ == '__main__':
    # Check command line args
    if ( ( len( sys.argv ) < 4 ) \
         or ( sys.argv[1] != 'taint' and sys.argv[1] != 'sts' ) ) :
        print( 'Please use a correct-command line argument:' )
        print( '\tpython3 ' + sys.argv[0] + ' [sts or taint] [dot_file.dot] [sources_and_sinks.json]' )
        exit( 1 )

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

    # Create list of valid output nodes
    output_nodes = []

    # Check if analysis is taint or sts
    if ( 'taint' == analysis_type ):
        track_taint( sources, output_nodes )
    else:
        source_to_sink( sources, output_nodes )

    # Write to output file
    output_final_dot_graph( output_nodes, dot_file_name, output_file_name )
