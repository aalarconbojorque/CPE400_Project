# -----------------------------------------------------------------------------
# FILE NAME:         proj.py
# USAGE:             python3 proj3.py
# NOTES:             Requires Python3
# Authors:           Andy Alarcon and Griffin Wagenknecht
# -----------------------------------------------------------------------------

import networkx as nx
import matplotlib.pyplot as plt
import sys


def main():

    G = nx.Graph()

    # Check that both input files exist
    nodesFile = CheckFile("nodes.txt")
    edgesFile = CheckFile("edges.txt")

    # If they do then input data and build the first graph
    if nodesFile and edgesFile:
        ObtainNodeData(G)

    else:
        sys.exit()

    print("-------------------------------------------------------------")
    print("Dynamic routing mechanism design in a faulty network Simulation")
    
    #Main menu loop
    while(True):
        print("-------------------------------------------------------------")
        print("Menu Options : ")
        print("[1] - Select a source and destination route to experiment")
        print("[2] - View the input network")
        print("[3] - Exit")
        option = ''
        try:
            option = int(input('Enter your selection : '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            print("Option 1")
        elif option == 2:
             DisplayGraph(G)
        elif option == 3:
            print('Thank you !')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')
    
    

    


# ----------------------------------------------------------------------------
# FUNCTION NAME:     DisplayGraph(G)
# PURPOSE:           Displays a window graph 
# -----------------------------------------------------------------------------


def DisplayGraph(G):
    
    # Setup graph
    pos = nx.circular_layout(G)
    subax1 = plt.subplot(121)
    nx.draw(G, pos, font_weight='bold', node_size=2000)
    edge_labels = nx.get_edge_attributes(G, 'failure')
    node_labels = nx.get_node_attributes(G, 'failure')
    for key, value in node_labels.items():
        node_labels[key] = "[" + str(key) + "," + str(value) + "]"
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='black', font_weight='bold')
    nx.draw_networkx_labels(G, pos, labels=node_labels,
                            font_color='black',  font_size=10, font_weight='bold')
    ax = plt.gca()
    ax.margins(0.2)
    plt.show()

# ----------------------------------------------------------------------------
# FUNCTION NAME:     ObtainNodeData(G)
# PURPOSE:           Open the input files and populate graph with nodes, edges
# -----------------------------------------------------------------------------
def ObtainNodeData(G):

    # Read the nodes file and create nodes
    nFile = open('nodes.txt', 'r')
    for line in nFile:
        line = line.replace('%', '')
        line = line.rstrip("\n")
        line = line.split('|')
        G.add_node(int(line[0]), failure=int(line[1]))

    # Read the edges file and create nodes
    nFile = open('edges.txt', 'r')
    for line in nFile:
        line = line.replace('%', '')
        line = line.rstrip("\n")
        line = line.split('|')
        G.add_edge(int(line[0]), int(line[1]), failure=int(line[2]))

# ----------------------------------------------------------------------------
# FUNCTION NAME:     CheckFile(fname)
# PURPOSE:           Check if we can open the files
# -----------------------------------------------------------------------------


def CheckFile(fname):
    try:
        f = open(fname, "r")
        return 1
    except IOError:
        print("Error: " + fname + " file was not found")
        return 0


if __name__ == "__main__":
    main()
