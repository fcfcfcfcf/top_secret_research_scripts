import re 
import sys
import concurrent.futures

sys.setrecursionlimit(500000)

if sys.argv[1] not in ['taint', 'sts', 'fusion', 'backslice']:
    print('please use a correct-command line argument, try\npython3 source_sink.py sts\nor\npython3 source_sink.py taint\n')
    exit(42069)
#sources = set(["Node0x7f62940fa5c0"])
#sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60"])
sources = set(["Node0x7fc4ad3c4210", "Node0x7fc4ad3c4320", "Node0x7fc4ad3c4400", "Node0x7fc4ad3c44e0", "Node0x7fc4ad3c45c0", "Node0x7fc4ad3c46a0", "Node0x7fc4ad3c4780", "Node0x7fc4ad3c4860", "Node0x7fc4ad3c4940", "Node0x7fc4ad3c4a80", "Node0x7fc4ad3c4bc0", "Node0x7fc4ad3c4d30", "Node0x7fc4ad3c5ce0", "Node0x7fc4ad3c7aa0", "Node0x7fc4ad3ca4f0"])

# sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60", "Node0x7f62937f65e0", "Node0x7f629345e2f0", "Node0x7f6293bf4160", "Node0x7f62940c07f0"])
sinks = set(["Node0x7fc4a1c928f0", "Node0x7fc4abf64780", "Node0x7fc4abf64890", "Node0x7fc4abf64970", "Node0x7fc4abf64a50", "Node0x7fc4abf64b30", "Node0x7fc4abf64c70", "Node0x7fc4abf64d80", "Node0x7fc4abf64f20", "Node0x7fc4abf67970", "Node0x7fc4a1e8f700", "Node0x7fc4a1e8f810", "Node0x7fc4a1e8f8f0", "Node0x7fc4a1e8f9d0", "Node0x7fc4a1e8fab0", "Node0x7fc4a1e8fbf0", "Node0x7fc4a1e8fd00", "Node0x7fc4a1e8fea0"])

destination_regex = re.compile("^.*? -> (.*)\[style.*$")
definition_regex = re.compile("^\s*(.*) \[shape.*$")
source_regex = re.compile("^\s*(.*?)(?::.*)? -> .*\[style.*$")

f = open("./SVF/svfg_final.dot")
graph = f.read().splitlines()
f.seek(0)

GSTSEP_counter = 0

class Source:
    def __init__(self):
        self.visited_nodes = set()
        self.output_nodes = set()
        self.leaf_nodes = []
        self.source_node = 'fake_source_node_id'
        self.sink_node = 'fake_sink_node_id'



def GSTSEP(cur_node, my_source):
    if cur_node in my_source.visited_nodes:
        if cur_node not in my_source.output_nodes:
            return False
        else:
            return True   
    else:
        my_source.visited_nodes.add(cur_node)
    if is_sink(cur_node):
        my_source.sink_node = cur_node
        my_source.output_nodes.add(cur_node)
        print('found path!')
        return True
    else:
        found = False
        for x in get_connecting_nodes(cur_node):
            if x not in my_source.visited_nodes:
                if GSTSEP(x, my_source):
                    found = True
            elif x in my_source.output_nodes:
                found = True

        if found:
            my_source.output_nodes.add(cur_node)
            return True
        else:
            if cur_node == "Node_Start":
                print("Path from source to sink not found")
            return False

    

def find_missing_fusion(my_flows):
    tagged_nodes = set()
    tagged_twice_nodes =set()
    for flow in my_flows:
        for x in flow:
            if x not in tagged_nodes:
                tagged_nodes.add(x)
            elif x not in tagged_twice_nodes:
                tagged_twice_nodes.add(x)
    for x in tagged_twice_nodes:
        tagged_nodes.remove(x)
    tagged_nodes_list = list(tagged_nodes) + list(sinks)
    output_final_dot_graph(tagged_nodes_list, 'fusion.dot')
        
                

def show_taint(cur_node, my_source):
    for x in get_connecting_nodes(cur_node):
        if x not in my_source.output_nodes:
            my_source.output_nodes.add(x)
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

        
def output_final_dot_graph(nodes, output_file_name):
    output_file = open(output_file_name, 'w')
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

dot_dict = {}
# dot_dict_back = {}
for line in f:
    src = source_regex.match(line)
    dest = destination_regex.match(line)
    if src != None:
        if src.group(1) in dot_dict:
            dot_dict[src.group(1)] += [dest.group(1)]
        else:
            dot_dict[src.group(1)] = [dest.group(1)]


final_nodes = set()
flows = []


def GSTSEP_helper(my_source):
    print(my_source)
    global final_nodes
    my_new_source = Source()
    my_new_source.source_node = my_source
    dot_dict["Node_Start"] = [my_source]
    GSTSEP("Node_Start", my_new_source)
    final_nodes = final_nodes.union(my_new_source.output_nodes)


with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    executor.map(GSTSEP_helper, sources)
    
output_final_dot_graph(final_nodes, 'output.dot')


# for x in sources:
#     print(x)
#     my_new_source = Source()
#     my_new_source.source_node = x
#     dot_dict["Node_Start"] = [x]
#     # dot_dict_back["Node_Start"] = [x]
#     if sys.argv[1] == 'taint':
#         show_taint("Node_Start", my_new_source)
#         with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
#             executor.map(show_taint, sources), my_new_source
#     elif sys.argv[1] == 'sts' or sys.argv[1] == 'fusion':
#         GSTSEP("Node_Start", my_new_source)
#     elif sys.argv[1] == 'backslice':
#         backwards_slice("Node_Start", my_new_source)
#         output_final_dot_graph(my_new_source.leaf_nodes, 'leaves.dot')
#     if sys.argv[1] == 'fusion':
#         flows.append(my_new_source.output_nodes)
    
#     final_nodes = final_nodes.union(my_new_source.output_nodes)
#     output_final_dot_graph(final_nodes, 'output.dot')
# if sys.argv[1] == 'fusion':
#     find_missing_fusion(flows + [['Node_super_duper_fake', 'Node_extra_super_fake', 'Node0x7f62940e02b0']])