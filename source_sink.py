import re 
import sys

if sys.argv[1] != 'taint' and sys.argv[1] != 'sts' and sys.argv[1] != 'fusion':
    print('please use a correct-command line argument, try\npython3 source_sink.py sts\nor\npython3 source_sink.py taint\n')
    exit(42069)
sources = set(["Node0x7f62940fa5c0"])
#sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60"])

# sources = set(["Node0x7f62940fa5c0", "Node0x7f6294096c10", "Node0x7f6294275a60", "Node0x7f62937f65e0", "Node0x7f629345e2f0", "Node0x7f6293bf4160", "Node0x7f62940c07f0"])
sinks = set(["Node0x7f62940e02b0"])

destination_regex = re.compile("^.*? -> (.*)\[style.*$")
definition_regex = re.compile("^\s*(.*) \[shape.*$")
source_regex = re.compile("^\s*(.*?)(?::.*)? -> .*\[style.*$")

f = open("./SVF/svfg_final.dot")
graph = f.read().splitlines()
f.seek(0)

GSTSEP_counter = 0

class Source:
    def __init__(self):
        self.visited_nodes = []
        self.output_nodes = []
        self.source_node = 'fake_source_node_id' 
        self.sink_node = 'fake_sink_node_id'

# def sym_list_diff(li1, li2):
#     sym_set = set(li1).symmetric_difference(set(li2))
    
#     return (list()


def GSTSEP(cur_node, my_source):
    global GSTSEP_counter
    # if GSTSEP_counter > 505:
    #     return False
    if cur_node in my_source.visited_nodes:
        if cur_node not in my_source.output_nodes:
            return False
        else:
            return True
            
    else:
        my_source.visited_nodes += [cur_node]
    if is_sink(cur_node):
        my_source.sink_node = cur_node
        GSTSEP_counter += 1
        my_source.output_nodes += [cur_node]
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
            GSTSEP_counter += 1
            my_source.output_nodes += [cur_node]
            return True
        else:
            if cur_node == "Node_Start":
                print("Path from source to sink not found")
            return False

        #if cur_node == "Node_Start":
         #   print("Path from source to sink not found")
          #  return False
        #my_source.output_nodes.remove(cur_node)
        #return False

# def get_path(node_from, node_to):
    

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
    output_final_dot_graph(tagged_nodes_list)
        
                
                
    # print('performing fusion analysis')
    # good = True
    # for path in my_flows:
    #     found = False
    #     for x in path:
    #         if not found:
    #             if x not in sinks:
    #                 for path_2 in my_flows:
    #                     if path != path_2:
    #                         if x in path_2:
    #                             found = True
    #     if not found:
    #         good = False
    #         print('!WARNING! fusion not detected for flow starting with node: ' + str(path[0]))
    #     else:
    #         print('fusion detected for path starting with node: ' + str(path[0]))
    # if not good:
    #     print('drone is not fully fused!')



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
flows = []
for x in sources:
    print(x)
    my_new_source = Source()
    my_new_source.source_node = x
    dot_dict["Node_Start"] = [x]
    if sys.argv[1] == 'taint':
        show_taint("Node_Start", my_new_source)
    elif sys.argv[1] == 'sts' or sys.argv[1] == 'fusion':
        GSTSEP("Node_Start", my_new_source)
    if sys.argv[1] == 'fusion':
        flows.append(my_new_source.output_nodes)
    final_nodes = final_nodes.union(my_new_source.output_nodes)
    output_final_dot_graph(final_nodes)
if sys.argv[1] == 'fusion':
    find_missing_fusion(flows + [['Node_super_duper_fake', 'Node_extra_super_fake', 'Node0x7f62940e02b0']])