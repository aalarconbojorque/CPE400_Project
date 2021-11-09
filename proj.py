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
    G.add_node(1, failure="5%")
    G.add_node(2, failure="9%")
    G.add_node(3, failure="10%")
    G.add_node(4, failure="11%")
    G.add_node(5, failure="100%")
    G.add_edge(1, 2, failure="10%")
    G.add_edge(1, 3, failure="100%")
    G.add_edge(2, 3, failure="19%")
    G.add_edge(3, 4, failure="21%")
    G.add_edge(1, 5, failure="33%")
    G.add_edge(5, 4, failure="43%")
    
    #Setup graph
    pos = nx.circular_layout(G)
    subax1 = plt.subplot(121)
    nx.draw(G,pos, font_weight='bold', node_size=2000)
    edge_labels = nx.get_edge_attributes(G,'failure')
    node_labels = nx.get_node_attributes(G,'failure')
    for key, value in node_labels.items():
        node_labels[key] = "[" + str(key) + "," + value + "]"
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='black', font_weight='bold')
    nx.draw_networkx_labels(G,pos,labels=node_labels,font_color='black',  font_size=10, font_weight='bold')
    ax = plt.gca()
    ax.margins(0.2)
    
    #Plot shortest path and graph
    path = nx.shortest_path(G, source=1, target=4)
    path_edges = zip(path,path[1:])
    path_edges = set(path_edges)
    nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r', node_size=2000)
    nx.draw_networkx_edges(G,pos, edgelist=path_edges,edge_color='r',width=5)
    plt.show()
    
    # Remove 100% edges
    edgelist = list(G.edges.data("failure"))
    for u, v, failure in edgelist:
      if failure == "100%":
        print(u, v , ":", failure)
        G.remove_edge(u, v)
      pass

    # Remove 100% nodes
    nodelist = list(G.nodes.data("failure"))
    for u, failure in nodelist:
      if failure == "100%":
        print(u, ":", failure)
        G.remove_node(u)
      pass
   
    #Setup graph
    pos = nx.circular_layout(G)
    subax1 = plt.subplot(121)
    nx.draw(G,pos, font_weight='bold', node_size=2000)
    edge_labels = nx.get_edge_attributes(G,'failure')
    node_labels = nx.get_node_attributes(G,'failure')
    for key, value in node_labels.items():
        node_labels[key] = "[" + str(key) + "," + value + "]"
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels,font_color='black', font_weight='bold')
    nx.draw_networkx_labels(G,pos,labels=node_labels,font_color='black',  font_size=10, font_weight='bold')
    ax = plt.gca()
    ax.margins(0.2)
    
    #Plot shortest path and graph
    path = nx.shortest_path(G, source=1, target=4)
    path_edges = zip(path,path[1:])
    path_edges = set(path_edges)
    nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r', node_size=2000)
    nx.draw_networkx_edges(G,pos, edgelist=path_edges,edge_color='r',width=5)
    plt.show()
   



    

    

# ----------------------------------------------------------------------------
# FUNCTION NAME:     CompMagSqr()
# PURPOSE:           Computes the magnitude squared
# -----------------------------------------------------------------------------

    
if __name__ == "__main__":
    main()
