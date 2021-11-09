# -----------------------------------------------------------------------------
# FILE NAME:         proj.py
# USAGE:             python3 proj3.py
# NOTES:             Requires Python3                    
# Authors:           Andy Alarcon and Griffin Wagenknecht
# -----------------------------------------------------------------------------

import networkx as nx
import matplotlib.pyplot as plt

def main():
    
    print("Hello World!")
    G = nx.Graph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_node(5)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(1, 5)
    G.add_edge(5, 4)
    subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()
    print("Shortest path before removing Node 5 from 1 -> 4")
    print(nx.shortest_path(G, source=1, target=4))
    G.remove_node(5)
    print("Shortest path after removing Node 5 from 1 -> 4")
    print(nx.shortest_path(G, source=1, target=4))
   



    

    

# ----------------------------------------------------------------------------
# FUNCTION NAME:     CompMagSqr()
# PURPOSE:           Computes the magnitude squared
# -----------------------------------------------------------------------------

    
if __name__ == "__main__":
    main()