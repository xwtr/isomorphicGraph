import networkx as nx
graph=nx.DiGraph()
graph.add_nodes_from([0, 3, 4, 9, 2, 1, 7])
graph.add_edges_from([(0, 3), (0, 4), (3, 9), (3, 2), (4, 1), (4, 7), (2, 4)])

sorted(graph.degree,reverse=True)

def encrypting(graph,rootNode):
    nodeStr="("+str(len(list(graph.predecessors(rootNode))))+":"
    for i in graph.neighbors(rootNode):
        nodeStr+=encrypting(graph,i)
    if not any(graph.neighbors(rootNode)):
        nodeStr+="0"
    nodeStr+=")"
    return nodeStr


def delete_last_character(nodeStr):
    nodeStr = nodeStr[:-1]
    return nodeStr


print(encrypting(graph, 0))
# print(encrypting(graph, 4))