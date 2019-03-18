import networkx as nx

#Load datasets or graph
G = nx.read_pajek("test.net")

#Dataset-node dict


#Init graph
print('test')
G = nx.Graph()

#'Add nodes
#TODO: Assign weights according to the dataset popularity 
G.add_nodes_from([1, 2, 3])
G.number_of_nodes()


#'Add edges
#1. +1 when share a same proper noun in the title or description, e.g. WHO
#2. +1 when share a same noun with a tf-idf lower than a threshold
#3. +1 when share a same tag, e.g. healthcare
G.add_edge(1, 2, weight=1)
G.number_of_edges()
G.edges.data()
G.edges[3, 4]['weight'] += 1

#Export graph
nx.write_pajek(G, "test.net")