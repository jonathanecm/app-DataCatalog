import networkx as nx

#Load datasets


#Dataset-node dict


#Init graph
print('test')
G = nx.Graph()

#'Add nodes
#TODO: Assign weights according to the dataset popularity 
G.add_nodes_from([2, 3])
G.nodes()


#'Add edges
#1. +1 when share a same proper noun in the title or description, e.g. WHO
#2. +1 when share a same tag, e.g. healthcare
G.add_edge(1, 2)

#Export graph