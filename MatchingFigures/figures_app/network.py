# generate the network structure without networkx

''' 
Doc:
Generates network structure without using the Networkx package. 
Represented in adjacency matrix format. Might implement a graphical representation.
'''

import numpy as np

def count_neighbours(G, node):
    '''
    Inputs:
        G: The adjacency matrix representation of a graph,
        node: the node whose neighbors are to be counted.
        
    return: int, the number of neighbors to the given node.'''

    neighour_count = 0

    return neighour_count

def generate_regular_graph(n_nodes, n_neighbours, is_di=False):
    '''
    Inputs:
        n_nodes: number of nodes,
        n_neighbours: number of neighbours to each node,
        is_di: whether the graph is directional, if directional only the top half of the 
        adjacency matrix will be populated.
    '''

    G = np.zeros((n_nodes, n_nodes), dtype=np.int64)

    for i in range(n_nodes):
        for j in range(n_nodes):
            if is_di and j <= i:
                continue
            G[i, j] = np.random.randint(0,2,dtype=np.int64)
            
    return G


if __name__ == '__main__':
    G = generate_regular_graph(4, 3, False)
    print(G)





# BACKUP

# # Draw the graph
# nx.draw(G, with_labels=True)
# plt.show()

# # position is stored as node attribute data for random_geometric_graph
# regularise_network(G,k)
# pos = nx.get_node_attributes(G, "pos")


# # find node near center (0.5,0.5)
# dmin = 1
# ncenter = 0
# for n in pos:
#     x, y = pos[n]
#     d = (x - 0.5) ** 2 + (y - 0.5) ** 2
#     if d < dmin:
#         ncenter = n
#         dmin = d

# # color by path length from node near center
# p = dict(nx.single_source_shortest_path_length(G, ncenter))

# plt.figure(figsize=(8, 8))
# nx.draw_networkx_edges(G, pos, alpha=0.4)
# nx.draw_networkx_nodes(
#     G,
#     pos,
#     nodelist=list(p.keys()),
#     node_size=20,
#     node_color=list(p.values()),
#     cmap=plt.cm.Reds_r,
# )

# plt.xlim(-0.05, 1.05)
# plt.ylim(-0.05, 1.05)
# plt.axis("off")
# plt.show()
