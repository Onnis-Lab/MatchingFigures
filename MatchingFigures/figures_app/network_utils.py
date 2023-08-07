# create a new network of n people

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def regularise_network(G,k):

    ''' 
        Remove extra neighbours of the given network until it becomes a regular network with the given number of neighbors.
        !!! WARNING: ONLY REMOVE EXTRA EDGES RANDOMLY!!!!
        Inputs:
        G: graph, 
            the graph to be regularised with MORE edges than desired;
        k: int,
            the number of neighbours for each node.
        
    '''
    for node in G.nodes:
        while len(list(G.neighbors(node))) > k:
            # Randomly select a neighbor to disconnect
            neighbor = np.random.choice(list(G.neighbors(node)))
            G.remove_edge(node, neighbor)

        # non_neighbors = list(nx.non_neighbors(G, node))
        # while len(list(G.neighbors(node))) < k:
        #     # Randomly select a non-neighbor node to connect
            
        #     if non_neighbors:  # If there are non-neighbors available
        #         new_neighbor = np.random.choice(non_neighbors)
        #         if get_distance(G, node, new_neighbor) < max_dist:
        #             G.add_edge(node, new_neighbor)
        #         non_neighbors.remove(new_neighbor)
        #     else:
        #         break


# Draw the graph
def draw(G):
    nx.draw(G, with_labels=False, node_size=20, node_shape='8')
    plt.show()

def pairs_this_round(am, active_nodes):

    '''
    Picks out all possible pairs if at least one of the nodes are active.
    
    Inputs:
        am: 2d-ndarray, 
            the adjacency matrix of the graph in np.array format, must be squared;
        active_nodes: 1D ndarray, 
            the array of of if the active nodes, 
        '''

    
    pairs = []
    participants = set() # is already paired up this round
    
    for r in range(len(am)):
        for c in range(len(am[0])):
            if am[r][c] and (active_nodes[r] or active_nodes[c]):
                if r not in participants and c not in participants:
                    pairs.append((r, c))
                    participants.add(r)
                    participants.add(c)
                

    return pairs, participants


def activate_nodes(active_nodes, participants):

    '''
    Updates the nodes activation array INPLACE which takes boolean values depending on 
    if the diffusion process has reached the given node.
    
    inputs:
        active_nodes: ndarray, the nodes activation array,
        participants: set, the set of participants which were active this round
    '''

    for part in participants:
        activate_nodes[part] = 1



if __name__ == '__main__':

    # RANDOM NETWORK
    n_neighbors = 4
    n_nodes = 12
    random_G = nx.random_regular_graph(n_neighbors, n_nodes)
    
    n_nodes_per_community = 4
    n_community = 3
    G = nx.planted_partition_graph(n_community,
                                n_nodes_per_community,
                                0.8, 
                                0.05, 
                                directed=False)
    regularise_network(G, n_neighbors)

    # make all activce for now 
    active_nodes = np.ones(n_nodes_per_community * n_community)

    draw(random_G)
    draw(G)
    
    pos = nx.get_node_attributes(G, "pos")
    
    pairs = pairs_this_round(G)
    print(pairs)
