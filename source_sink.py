import re 
import sys
import concurrent.futures
import cxxfilt

sys.setrecursionlimit(500000)


#define source and sink nodes
#sources are defined as pairs with their corresponding sensor type
sources = set([("Node0x7fc4acb1dc60", "rangefinder"), ("Node0x7fc4acb1dd70", "rangefinder"), ("Node0x7fc4acb1de50", "rangefinder"), ("Node0x7fc4acb1df30", "rangefinder"), ("Node0x7fc4acb1e010", "rangefinder"), ("Node0x7fc4acb1e1d0", "rangefinder"), ("Node0x7fc4acb1e2b0", "rangefinder"), ("Node0x7fc4acb1e390", "rangefinder"), ("Node0x7fc4acb1e630", "rangefinder"), ("Node0x7fc4acb1e7a0", "rangefinder"), ("Node0x7fc4acb1e9a0", "rangefinder"), ("Node0x7fc4acb213f0", "rangefinder"), ("Node0x7fc4ad4a3e20", "opflow"), ("Node0x7fc4ad4a3f30", "opflow"), ("Node0x7fc4ad4a4010", "opflow"), ("Node0x7fc4ac11e320", "compass"), ("Node0x7fc4ac11e430", "compass"), ("Node0x7fc4ac11e510", "compass"), ("Node0x7fc4ac11e5f0", "compass"), ("Node0x7fc4ac11eb30", "compass"), ("Node0x7fc4ac11ec10", "compass"), ("Node0x7fc4ac11ecf0", "compass"), ("Node0x7fc4ac11edd0", "compass"), ("Node0x7fc4ac11eeb0", "compass"), ("Node0x7fc4ac11ef90", "compass"), ("Node0x7fc4ac11f0a0", "compass"), ("Node0x7fc4ac11f1b0", "compass"), ("Node0x7fc4ac11f610", "compass"), ("Node0x7fc4ac120410", "compass"), ("Node0x7fc4ac124b00", "compass")]) #AP_OpticalFlow::update(), AP_Proximity_RangeFinder::update(), Compass::read()
sinks = set(["Node0x7fc4b180da80"])

#regex definitions to parse 
destination_regex = re.compile("^.*? -> (.*)\[style.*$")
definition_regex = re.compile("^\s*(.*) \[shape.*$")
source_regex = re.compile("^\s*(.*?)(?::.*)? -> .*\[style.*$")
function_name_regex = re.compile("^\s*(Node.*?) \[shape.*nFun\[(.*?)\].*$")

#open the file 'svfg_final.dot' which should be located in the same directory 
f = open("./svfg_final.dot")
graph = f.read().splitlines()
f.seek(0)

#this will store a set of root nodes for trees representing data flow from a source to a sink
final_trees = set()



#dot_dict is a dictionary with node_ids as key values
#each key can access the node's dest (nodes it connects to)
#and the node's function (fn) if it corresponds to one
#this is what we use to represent the svfg instead of reading it from the file every time we want to access it
dot_dict = {}

#global nodes holds information about every function node
global_nodes = {}

#this will store the set of nodes that make up all of the function nodes up to and including the first time two sensor flows intersect
intersection_nodes = set()

#defines a particular source node and the sets of nodes making up flows from it
class Source:
    def __init__(self, _name):
        #nodes visited when algorithm is searching for sink
        self.visited_nodes = set()
        #all nodes that make up any of the flows from this source
        self.output_nodes = set()
        #stores the function name corresponding to the source node
        self.name = _name
        #holds the source node id
        self.source_node = 'fake_source_node_id'

#node class (used for )
class Node:
    def __init__(self, _fn, _id, _st):
        #all of the node's children
        self.children = set()
        #the node id as given in the svfg
        self.node_id = _id
        #the function that this node represents, if it represents a function
        self.fn = _fn
        #specifies which of rangefinder, compass, and opticalflow data flows from to this node
        self.source_type = _st




#pathfinder algorithm, finds all nodes that make up paths from a source to a sink 
#and stores them as a set in output_nodes for the passed in source
#this analysis also will build a tree composed of Nodes from a given root. 
#this tree will be comprised entirely of function nodes, and is built as the algorithm progresses with tree_node
#this is a depth first search, so the tree of functions is built from the bottom up (will make more sense when you read the code)
def GSTSEP(cur_node, tree_node, my_source):
    #we don't want to look at nodes we've already visited, that would just create infinite loops
    if cur_node in my_source.visited_nodes:
        #if we have visited but the node is already in the output nodes (leads to a sink node), we can just return true, this path is valid
        if cur_node not in my_source.output_nodes:
            #but if it isn't we just return false
            return False
        else:
            return True   
    else:
        #if we haven't visited this node, add it to the list of visited nodes
        my_source.visited_nodes.add(cur_node)

    #first we want to check if the node is a sink node, because we want to handle those differently
    if is_sink(cur_node):
        #add this node to the sources output nodes because it is part of the path to a sink (it is a sink lol)
        my_source.output_nodes.add(cur_node)
        print('found path!')
        #see if the node has a corresponding function (it always should if it is a sink node)
        my_fn_str = dot_dict[cur_node]['fn']
        if my_fn_str:
            #create a new function node
            new_fn_node = Node(my_fn_str, cur_node, my_source.name)
            #if there is a local root node (there should be), add this node as a child 
            if tree_node:
                tree_node.children.add(new_fn_node)
        #a sink has been found, return True
        return True
    else:
        isFn = False
        my_tree_node = tree_node
        #make sure the current node is in the dot-graph dictionary we created (it should be)
        if cur_node in dot_dict:
            
            my_fn_str = dot_dict[cur_node]['fn']
            #if the node has a corresponding function, create a Node to (maybe) be added to the function tree
            if my_fn_str:
                isFn = True
                my_tree_node = Node(dot_dict[cur_node]['fn'], cur_node, my_source.name)
        found = False

        #look at all of the nodes that connect to the current node we are looking at
        for x in get_connecting_nodes(cur_node):
            #if we haven't visited it yet, run the analysis on that node
            if x not in my_source.visited_nodes:
                if GSTSEP(x, my_tree_node, my_source):
                    #if running the analysis on a child returns to sink, the parent (current node) should also return true
                    found = True
            elif x in my_source.output_nodes:
                #if the parent connects to a node already in the output nodes, we have also found a path
                found = True

        #if we found a path, add the current node to our output
        if found:
            my_source.output_nodes.add(cur_node)
            #if the current node is also a function, add this node as a child to our current tree root
            if isFn:
                tree_node.children.add(my_tree_node)
            #return true (meaning we found a path)
            return True
        else:
            #if the current node is where we started, that means no paths from the given root connect to a sink
            if cur_node == "Node_Start":
                print("Path from source to sink not found")
            #return false (meaning we did not find a path)
            return False


        

#helper function that returns whether or not the given node is a sink
def is_sink(node):
    return node in sinks

#helper function that returns whether or not the given node is a leaf node
def is_leaf(node):
    return not (node in dot_dict)


#helper function that gets all nodes that connect to the given node
def get_connecting_nodes(node):
    if node in dot_dict:
        return dot_dict[node]['dest']
    else:
        return []


#given a set of output nodes, write the final output to a dot file        
def output_final_dot_graph(nodes, output_file_name):
    #open the file and write the standard SVFG header
    output_file = open(output_file_name, 'w')
    output_file.write('digraph "SVFG" {\n')
    output_file.write('\tlabel="SVFG";\n')

    #copy each line of the full graph to the new file if 
    #1. the line represents an edge connecting two nodes contained in the output
    #or
    #2. the line defines a node contained in our output
    for x in graph:
        node_def = definition_regex.match(x)
        node_src = source_regex.match(x)
        node_dest = destination_regex.match(x)
        if (node_def != None and node_def.group(1) in nodes) or ((node_src != None and node_src.group(1) in nodes) and (node_dest != node_dest.group(1) in nodes)):
            output_file.write(x + '\n')
    #write the end of file 
    output_file.write('}\n')

#helper function that gets everything ready for running the GSTSEP algorithm on a given source node
def GSTSEP_helper(my_source):
    print(my_source)
    #make a new Source object with the given source node id
    my_new_source = Source(my_source[1])
    my_new_source.source_node = my_source[0]

    #create a temporary 'start node' to serve as a the first linking edge
    dot_dict["Node_Start"] = {}
    dot_dict["Node_Start"]['dest'] = [my_source[0]]
    dot_dict["Node_Start"]['fn'] = ''
    #create a new node to serve as the root for the function flow graph
    my_new_node = Node(dot_dict[my_new_source.source_node]['fn'], my_new_source.source_node, my_source[1])

    #run the algorithm on the given node
    if GSTSEP("Node_Start", my_new_node, my_new_source):
        global final_trees
        #if a path is found, add the tree to final_trees
        final_trees.add(my_new_node)
        print('added to tree')


#this is function finds every intersection between two flows of different types
#given a source, this looks for all flows with a different sensor type that intersects with flows from the source
#recursively calls until an intersection is found for each path
def find_intersection(my_source):
    #check if the source is contained within the global set of function nodes
    if my_source in global_nodes:
        #check and see if the node contains more than 1 type, if so it is an intersection point
        if not len(global_nodes[my_source]['types']) > 1:
            #add each of the children to the node's dictionary entry
            for x in global_nodes[my_source]['children']:
                global_nodes[my_source]['node'].children.add(global_nodes[x]['node'])
            #call find_intersection on each of the children
            for x in global_nodes[my_source]['children']:
                if x != my_source:
                    find_intersection(x)
        #add the node to the set of nodes used to construct the pre-intersection graph
        intersection_nodes.add(global_nodes[my_source]['node'])


#writes a node label to a given output file
def write_node(output_file, node):
    node_id = node.node_id
    str_write = ''
    str_write += global_nodes[node_id]['fn'] +', '
    for z in global_nodes[node_id]['types']:
        str_write += z + ', '
    output_file.write('\t'+ node_id + ' [shape=record,color=black,label="{' + str_write.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt').replace('#', '&num').replace('?', '&quest').replace('{', '&lcub').replace('}', '&rcub') + ', ' + node_id + '}"];\n')
    for x in node.children:
        output_file.write('\t' + node_id + ' -> ' + x.node_id + '[style=solid];\n')

#scan a given node and add it to the global_nodes dictionary
def scan_node(my_node):
    if my_node.node_id not in global_nodes:
        global_nodes[my_node.node_id] = {}
        global_nodes[my_node.node_id]['fn'] = my_node.fn
        global_nodes[my_node.node_id]['children'] = set()
        global_nodes[my_node.node_id]['types'] = set()
        global_nodes[my_node.node_id]['node'] = my_node
    #add each of the node's children to the dictionary entry
    for x in my_node.children:
        global_nodes[my_node.node_id]['children'].add(x.node_id)
    global_nodes[my_node.node_id]['types'].add(my_node.source_type)
    #make dictionary entries for each of the node's children
    for x in my_node.children:
        scan_node(x)
    #reset the node object's children to be empty
    my_node.children = set()



#read all the lines of the svfg into the dot_dict
for line in f:
    #match line to regex
    src = source_regex.match(line)
    dest = destination_regex.match(line)
    fn = function_name_regex.match(line)
    #if it found a src match, that means it is an edge
    if src != None:
        #add the edge to the dot dict
        if src.group(1) in dot_dict:
            dot_dict[src.group(1)]['dest'] += [dest.group(1)]
        else:
            #if it's not already there add an entry for the given source of the edge
            dot_dict[src.group(1)] = {}
            dot_dict[src.group(1)]['fn'] = ''
            dot_dict[src.group(1)]['dest'] = [dest.group(1)]

    #if it doesn't match to src then it must be a defintion, check if a function is in the definition
    elif fn != None:
        #if it is, we want to add it as the function entry for the given node
        if fn.group(1) in dot_dict:
            dot_dict[fn.group(1)]['fn'] = cxxfilt.demangle(fn.group(2))
        else:
            #if it's not already there add an entry for the given source of the edge
            dot_dict[fn.group(1)] = {}
            dot_dict[fn.group(1)]['fn'] = cxxfilt.demangle(fn.group(2))
            dot_dict[fn.group(1)]['dest'] = []

#call the path-finding algorithm for every source node we defined
for x in sources:
    GSTSEP_helper(x)

#put each node in final_trees into global_nodes
for x in final_trees:
    scan_node(x)

#write the full tree to a dot file
output_file = open('./output/full_tree.dot', 'w')
output_file.write('digraph "SVFG" {\n')
output_file.write('\tlabel="SVFG";\n')

for x in global_nodes:
    str_write = ''
    str_write += global_nodes[x]['fn'] +', '
    for z in global_nodes[x]['types']:
        str_write += z + ', '
    output_file.write('\t'+ x + ' [shape=record,color=black,label="{' + str_write.replace('&', '&amp').replace('<', '&lt').replace('>', '&gt').replace('#', '&num').replace('?', '&quest').replace('{', '&lcub').replace('}', '&rcub') + '}"];\n')
    for y in global_nodes[x]['children']:
        output_file.write('\t' + x + ' -> ' + y + '[style=solid];\n')

output_file.write('}\n')
output_file.close()

#write the 'first intersection' tree to a dot file
output_file = open('./output/first_intersection.dot', 'w')
output_file.write('digraph "SVFG" {\n')
output_file.write('\tlabel="SVFG";\n')
for x in sources:
    find_intersection(x[0])
for x in intersection_nodes:
    write_node(output_file, x)
output_file.write('}\n')
output_file.close()