import networkx as nx
import matplotlib.pyplot as plt


def has_same_father(graph, a, b):
    # for i in G.neighbors(a):
    for i in graph.predecessors(a):
        if graph.has_edge(i, a) and graph.has_edge(i, b):
            return True
    return False


def sort_node(graph, node_list):
    return [item[0] for item in sorted(graph.degree(node_list), key=lambda x: x[1], reverse=True)]


def bfs(graph, bfs_tree, start_node):
    visited = [False for i in range(len(graph.nodes.data()))]
    queue = []
    queue.append(start_node)
    visited [start_node] = True
    bfs_tree.add_node(start_node)
    while queue:
        start_node = queue.pop(0)
        visited[start_node] = True
        node_list = sort_node(graph, graph.neighbors(start_node))  # sort node based on degree
        # for i in graph.neighbors(start_node):
        for i in node_list:

            if not bfs_tree.has_node(i):
                bfs_tree.add_node(i)
                queue.append(i)
                bfs_tree.add_edge(start_node, i)
            elif has_same_father(bfs_tree, i, start_node) and not visited[i]:

                if not bfs_tree.has_node(i + len(graph.nodes())):
                    bfs_tree.add_node(i + len(graph.nodes()))
                bfs_tree.add_edge(start_node, i + len(graph.nodes()))

                if not bfs_tree.has_node(start_node + len(graph.nodes())):
                    bfs_tree.add_node(start_node + len(graph.nodes()))
                bfs_tree.add_edge(i, start_node + len(graph.nodes()))
            # else:
            #     A.add_edge(s, i)
            # elif  set(A.predecessors(s))&set(A.predecessors(i)) :
            #     A.add_edge(s, i)
            #     # A.add_edge(i, s)
            elif not i in bfs_tree.predecessors(start_node) and \
                    not set(bfs_tree.predecessors(start_node)) & set(bfs_tree.predecessors(i)):
                bfs_tree.add_edge(start_node, i)
                # A.add_edge(i, s)


def encrypting(graph, rootNode):
    nodeStr= "("+str(len(list(graph.predecessors(rootNode))))+":"
    # sorting_nodes(graph, rootNode)
    # neighbors_list= sorted_neighbors(graph, rootNode)
    neighbors_list= sort_node(graph, graph.neighbors(rootNode))
    for i in neighbors_list:
        nodeStr+= encrypting(graph, i)
    if not any(neighbors_list):
        nodeStr+= "0"
    nodeStr+= ")"
    return nodeStr

'''def sorted_neighbors(graph, rootNode):
    neighbors_list= list(graph.neighbors(rootNode))
    for i in range(len(neighbors_list)):
        for j in range(len(neighbors_list)-i-1):
            if(graph.out_degree(list(graph.neighbors(rootNode))[j] ) > graph.out_degree(list(graph.neighbors(rootNode)) [j+1] )):
                neighbors_list [j] , neighbors_list [j+1] = neighbors_list [j+1] , neighbors_list [j] 
            elif (graph.out_degree(list(graph.neighbors(rootNode)) [j] ) == graph.out_degree(list(graph.neighbors(rootNode)) [j+1] )):
                if(graph.in_degree(list(graph.neighbors(rootNode)) [j] ) > graph.in_degree(list(graph.neighbors(rootNode)) [j+1] )):
                    neighbors_list [j] , neighbors_list [j + 1]  = neighbors_list [j + 1] , neighbors_list [j] 

    return neighbors_list
'''
'''
def number_of_parents(graph, j, rootNode):
    # return len(list(graph.predecessors(list(graph.neighbors(rootNode)) [j] )))
    return graph.in_degree(list(graph.neighbors(rootNode)) [j] )'''
'''
def number_of_child(graph, j, rootNode):
    return graph.out_degree(list(graph.neighbors(rootNode)) [j] )
'''
def delete_last_character(nodeStr):
    nodeStr = nodeStr [:-1] 
    return nodeStr


def read_one_graph(file_name, graph_number):
    return nx.read_graph6(file_name + '.g6') [graph_number] 


def save_graph_fig(G, graph_name):
    plt.clf()
    nx.draw(G, with_labels= True)
    plt.savefig(graph_name+".png")


def save_two_graphs_fig(A, G, file_name, i):
    plt.clf()
    nx.draw(G, node_color= 'red', with_labels= True)
    nx.draw(A, node_color= 'blue', with_labels= True)
    plt.savefig(file_name+str(i))


def execute_graphs_file(file_name):#read graph file and create file of  graph string
    file = open('bfs_tree_of_' + file_name + '.txt', "w+")
    for graph in nx.read_graph6(file_name + ".g6"):
        graph_str = find_graph_string(graph)
        file.write(graph_str + '\n')#write graph string in file
    file.close()
    return 'bfs_tree_of_'+ file_name + '.txt'


def find_graph_string(graph):
    graph_str = ""
    node_list = sort_node(graph, graph.nodes)  # sort node based on degree
    # j= 0 ##for save graph fig
    for i in node_list:  # find node string for all nodes and connect them
        A = nx.DiGraph()
        bfs(graph, A, i)
        graph_str += encrypting(A, i)
    '''  save graph fig
         j= j+1
         save_two_graph_fig(A, G, file_name, i)'''
    return graph_str


def print_isomorphic_graphs(file_name):

    file=open("isomorphic_"+file_name+".txt","w+")
    graph6_array=get_graph6_array(file_name)
    encrypting_file_name=execute_graphs_file(file_name)
    isomorphic_graph_array=find_isomorphic_tuple(get_parenthesis_array(encrypting_file_name),get_numbers_array(encrypting_file_name))
    get_numbers_file(encrypting_file_name)#create file of numbers as log
    get_parenthesis_file(encrypting_file_name)#create file of parenthesis as log
    for i in isomorphic_graph_array:
        print("("+graph6_array[i[0]]+" "+graph6_array[i[1]]+")")
        file.write("("+graph6_array[i[0]]+" "+graph6_array[i[1]]+")")
    file.close()
    ##
def get_graph6_array(file_name):
    graph6_array=[]
    file=open(file_name + ".g6","r")
    for line in file:
        graph6_array.append(line)
    file.close()
    return graph6_array

def get_parenthesis_file(file_name):
    file = open('parenthesis_' + file_name, "w+")
    file2 = open(file_name, "r")
    for line in file2:
        file.write(separate_parenthesis(line)+'\n')
    file.close()
    return 'parenthesis_' + file_name+"txt"


def get_parenthesis_array(file_name):
    parenthesis_array=[]
    file2 = open(file_name, "r")
    for line in file2:
        parenthesis_array.append(separate_parenthesis(line)+'\n')
    return parenthesis_array


def get_numbers_file(file_name):
    file = open('numbers_' + file_name, "w+")
    file2 = open(file_name, "r")
    for line in file2:
        file.write(separate_numbers(line) + '\n')
    file.close()
    return 'numbers_' + file_name+"txt"


def get_numbers_array(file_name):
    file2 = open(file_name, "r")
    numbers_array=[]
    for line in file2:
        numbers_array.append(separate_numbers(line) + '\n')
    return numbers_array

def separate_numbers(graph_string):
    numbers_string= ""
    for s in graph_string:
        if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] :
            numbers_string= numbers_string+s
    return numbers_string


def find_isomorphic_tuple(parenthesis_array, number_array):
    isomorphic_array=[]
    for i in range(len(parenthesis_array)):
        node_dic=count_same_element_of_array(separate_parenthesis_node(parenthesis_array[i]))
        for j in range(i+1,len(parenthesis_array)):
            if len(parenthesis_array[i])==len(parenthesis_array[j] )and \
                    parenthesis_is_same(node_dic, count_same_element_of_array(separate_parenthesis_node(parenthesis_array[j]))) \
                    and number_array[i]==number_array[j]:
                    isomorphic_array.append((i,j))
    return isomorphic_array


def separate_parenthesis_node(line):
    stack = []
    array=[]
    i=0
    node_str=""
    for s in line:
        if not any(stack) and node_str!="":
            array.append(node_str)
            node_str=""
        if s == '(':
            node_str+= s
            stack.append(s)
        elif s == ')':
            node_str+= s
            stack.pop()
    return array



def count_same_element_of_array(array):
    dictionary={}
    for i in range(len(array)):
        dictionary.update({array[i]:array.count(array[i])})
    return dictionary

def parenthesis_is_same(dict1, dict2):
    list_key1=list(dict1.keys())
    temp=0

    for i in list_key1:
        if i  not in dict2 or dict1[i]!=dict1[i]:
            return False

    return True






def separate_parenthesis(graph_string):
    parenthesis_string= ""
    for s in graph_string:
        if s== '(' or s== ')':
            parenthesis_string= parenthesis_string + s
    return parenthesis_string
# graph_number= 4
# string_graph_file_name= execute_graphs_file(file_name)
# get_parenthesis_file(string_graph_file_name)
# get_numbers_file(string_graph_file_name)
# G= read_one_graph(file_name, graph_number)
# # A =  nx.DiGraph()
# # bfs(G, A, 0)
# # # save_graph_fig(G, "g5c4")
# # # save_graph_fig(A, "Ag5c4")
# # print(encrypting(A, 0))
#
# coding_file_name=execute_graphs_file(file_name)

# file_name= "graph8c"
# print_isomorphic_graphs(file_name)
for i in range(3,12):
    print_isomorphic_graphs("graph"+str(i)+"c")
