# create a new network of n people

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

'''
Contains functions for creating networks and (potentially) matchmaking algorithms. 
'''

#TODO: Watts-Strogatz 
def regularise_network(G,k):
    
    #TODO: remove this function

    ''' 
        Remove extra neighbours of the given network until it becomes a regular network with the given number of neighbors.
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
def draw(G, pos=None, with_labels=True):
    if pos:
        nx.draw(G, pos, with_labels=with_labels, node_size=100, node_color='skyblue')
    else:
        nx.draw(G, with_labels=with_labels, node_size=20, node_shape='8')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def pairs_this_round(am, active_nodes, executed_pairs):

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
            if (r,c) not in executed_pairs:
                if am[r][c] and (active_nodes[r] or active_nodes[c]):
                    if r not in participants and c not in participants:
                        pairs.append((r, c))
                        participants.add(r)
                        participants.add(c)
                        executed_pairs.append((r, c))
                

    return pairs, participants


def activate(active_nodes, participants):

    '''
    Updates the nodes activation array INPLACE which takes boolean values depending on 
    if the diffusion process has reached the given node.
    
    inputs:
        active_nodes: ndarray, the nodes activation array,
        participants: set, the set of participants which were active this round
    '''
    new_active_nodes = active_nodes
    for part in participants:
        new_active_nodes[part] = 1
    
    print(new_active_nodes)
    return new_active_nodes


def to_ring(n):

    # Calculate polar coordinates for nodes for a ring layout
    theta = np.linspace(0, 2*np.pi, n, endpoint=False)
    pos = {i: (np.cos(theta[i]), np.sin(theta[i])) for i in range(n)}

    return pos


def watts_strogatz(N=12,k=4,p=0.4):

    # Generate the graph
    G = nx.watts_strogatz_graph(N, k, p)

    pos = to_ring(N)

    # Draw the graph using the polar coordinates
    draw(G, pos) 


if __name__ == '__main__':

    # RANDOM NETWORK
    N_NEIGHBORS = 4
    N_NODES = 20

    # PLANTED PARTITION NETWORK (remove)
    N_NODES_PER_COMMUNITY = 4
    N_COMMUNITY = int(N_NODES/N_NODES_PER_COMMUNITY)

    # WATTS-STROGATZ NETWORK
    P_REWIRE = 0.2

    # GAME
    N_ROUNDS = 5

    random_G = nx.random_regular_graph(N_NEIGHBORS, N_NODES)
    pos = to_ring(N_NODES)
    draw(random_G, pos)

    watts_strogatz(N_NODES, N_NEIGHBORS, P_REWIRE)
    

    # clustered_G = nx.planted_partition_graph(N_COMMUNITY,
    #                             N_NODES_PER_COMMUNITY,
    #                             0.8, 
    #                             0.05, 
    #                             directed=False)
    # regularise_network(clustered_G, N_NEIGHBORS)

    ###################################### ACTIVATION TEST ##########################################################

    active_nodes = np.zeros(N_NODES_PER_COMMUNITY * N_COMMUNITY)
    active_nodes[0] = 1
    executed_pairs = []

    am_random = nx.adjacency_matrix(random_G).toarray()
    for _ in range(N_ROUNDS):
        pairs, participants = pairs_this_round(am_random, active_nodes, executed_pairs)
        print(pairs)
        active_nodes = activate(active_nodes, participants)
        print(active_nodes)


    

        
