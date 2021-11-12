# -----------------------------------------------------------------------------
# FILE NAME:         proj.py
# USAGE:             python3 proj3.py
# NOTES:             Requires Python3
#                    Requires networkx
#                    Requires pip (if networkx is not installed)
# Authors:           Andy Alarcon and Griffin Wagenknecht
# -----------------------------------------------------------------------------

import networkx as nx
import matplotlib.pyplot as plt
import sys
import random


def main():

    G = nx.Graph()

    # Check that both input files exist
    nodesFile = CheckFile("routers.txt")
    edgesFile = CheckFile("links.txt")

    # If they do then input data and build the first graph
    if nodesFile and edgesFile:
        ObtainNodeData(G)

    else:
        sys.exit()

    print("-------------------------------------------------------------")
    print("Dynamic routing mechanism design in a faulty network simulation")

    # Main menu loop
    while(True):
        print("-------------------------------------------------------------")
        print("Menu Options : ")
        print(
            "[1] - Select a source and destination router to simulate routing in a faulty network")
        print("[2] - Exit")
        option = ''
        try:
            option = int(input('Enter your selection : '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            DisplayGraph(G, "", 1, False, "", False, "", "")
            runSimulation(G)
        elif option == 2:
            print('Thank you !')
            exit()
        else:
            print('Invalid option. Please enter a number.')


# ----------------------------------------------------------------------------
# FUNCTION NAME:     runSimulation(G)
# PURPOSE:           Runs the shortest path simulation
# -----------------------------------------------------------------------------


def runSimulation(G):

    # Obtains valid sourceNode and destNode
    returnedNodes = ObtainNodesMenu(G)
    sourceNode = returnedNodes[0]
    destNode = returnedNodes[1]

    InitalPathExist = nx.has_path(G, sourceNode, destNode)

    # We keep looping the entered path does not work
    while not InitalPathExist:

        # Check if a path exists between the two nodes
        InitalPathExist = nx.has_path(G, sourceNode, destNode)

        # If we cannot find a path, we need to let the user enter new nodes
        if not InitalPathExist:
            print(
                "\nUnfortunately, a route cannot be established between the two routers. Please try another route.")
            returnedNodes = ObtainNodesMenu(G)
            sourceNode = returnedNodes[0]
            destNode = returnedNodes[1]

        # If we find a path break
        else:
            pass

    # Begin network simulation
    print("-------------------------------------------------------------")
    print("A path from router", sourceNode, "->", destNode,
          "will be simulated on using the provided network.")
    initalPath = nx.shortest_path(
        G, source=sourceNode, target=destNode, weight="failure")
    print("Without any network failures, the shortest route is",
          initalPath, ".")

    initalPath_edges = zip(initalPath, initalPath[1:])
    initalPath_edges = set(initalPath_edges)

    # Update graph with shortest path
    DisplayGraph(G, "", 1, True, initalPath_edges, False, "", "")

    print("\nRunning failure simulation ...")
    # RemovalList[0] - edges that failed
    # RemovalList[1] - nodes that failed
    RemovalLists = simulateNetworkFailues(G)

    # Create a copy of the network to remove edges and routes
    H = G.copy()
    H.remove_edges_from(RemovalLists[0])
    H.remove_nodes_from(RemovalLists[1])

    # If all the network fails we need to retry
    if H.number_of_edges() == 0:
        print("\nUnfortunately because of the failures, no links are available to create a route. Please try another simulation.")
    else:

        pathStillExists = False
        sourceCheck = H.has_node(sourceNode)
        destCheck = H.has_node(destNode)

        # Display the network graph after the failures
        DisplayGraph(G, H, 1, False, "", True,
                     RemovalLists[1], RemovalLists[0])

        # Check if our source and desination nodes are still good
        if(not sourceCheck or not destCheck):

            print("\nUnfortunately, either the source or desination router no longer exists. Please try another route.")

            # Since they are not we need new nodes
            returnedNodes = ObtainNodesMenu(H)
            sourceNode = returnedNodes[0]
            destNode = returnedNodes[1]

            # We keep looping if our path does not work
            while not pathStillExists:

                # Check if a path exists between the two nodes
                pathStillExists = nx.has_path(H, sourceNode, destNode)

                # If we cannot find a path, we need to let the user enter new nodes
                if not pathStillExists:
                    print(
                        "\nUnfortunately, a route cannot be established between the two routers. Please try another route.")
                    returnedNodes = ObtainNodesMenu(H)
                    sourceNode = returnedNodes[0]
                    destNode = returnedNodes[1]

                # If we find a path, calculate the shortest route and update graph
                else:
                    spath = nx.shortest_path(
                        H, source=sourceNode, target=destNode, weight="failure")
                    spath_edges = zip(spath, spath[1:])
                    spath_edges = set(spath_edges)
                    print("\nWith the current network failures, the shortest route between", sourceNode, "and", destNode, "is",
                          spath, ".")
                    DisplayGraph(G, H, 1, True, spath_edges, True,
                                 RemovalLists[1], RemovalLists[0])
        else:

            # We keep looping if our path does not work
            while not pathStillExists:

                # Check if a path exists between the two nodes
                pathStillExists = nx.has_path(H, sourceNode, destNode)

                # If we cannot find a path, we need to let the user enter new nodes
                if not pathStillExists:
                    print(
                        "\nUnfortunately, a route cannot be established between the two routers. Please try another route.")
                    returnedNodes = ObtainNodesMenu(H)
                    sourceNode = returnedNodes[0]
                    destNode = returnedNodes[1]

                # If we find a path, calculate the shortest route and update graph
                else:
                    spath = nx.shortest_path(
                        H, source=sourceNode, target=destNode, weight="failure")
                    spath_edges = zip(spath, spath[1:])
                    spath_edges = set(spath_edges)
                    print("\nWith the current network failures, the shortest route between", sourceNode, "and", destNode, "is",
                          spath, ".")
                    DisplayGraph(G, H, 1, True, spath_edges, True,
                                 RemovalLists[1], RemovalLists[0])


# ----------------------------------------------------------------------------
# FUNCTION NAME:     simulateNetworkFailues(G)
# PURPOSE:           Modifes the input network based on the failure probablity
# -----------------------------------------------------------------------------


def simulateNetworkFailues(G):

    print("\nThe following links between routers have failed due to their chance of failure:")

    # Randomly fail edges based on percentage of failure
    edgelist = list(G.edges.data("failure"))
    # This list will be used later on to remove edges from the graph
    edgelistRemoval = list(G.edges.data("failure"))
    for index, edge in enumerate(edgelist):

        perc = float(edge[2])
        val = float(random.randint(0, 100))

        # Randomly compute a failure chance
        if val <= perc:
            per = str(edge[2]) + "%"
            print("-", edge[0], "->", edge[1], ":", per, "failure")
        else:
            edgelistRemoval.remove(edge)

    print("\nThe following routers have failed due to their chance of failure:")
    # Randomly fail nodes based on percentage of failure
    nodelist = list(G.nodes.data("failure"))
    # This list will be used later on to remove nodes from the graph
    nodelistRemoval = []
    for index, node in enumerate(nodelist):

        perc = float(node[1])
        val = float(random.randint(0, 100))

        # Randomly compute a failure chance
        if val <= perc:
            per = str(node[1]) + "%"
            print("-", node[0], ":", per, "failure")
            nodelistRemoval.append(node[0])
        else:
            pass

    return edgelistRemoval, nodelistRemoval

# ----------------------------------------------------------------------------
# FUNCTION NAME:     ObtainNodesMenu(G, sourceNode, destNode)
# PURPOSE:           Runs menu to obtain the source and dest nodes
# -----------------------------------------------------------------------------


def ObtainNodesMenu(G):

    print("-------------------------------------------------------------")

    # Loop to check if the source node exists
    loop1 = True
    while(loop1):
        sourceNode = ''
        try:
            sourceNode = int(
                input('Please enter your source router number : '))
        except:
            print('Wrong input. Please enter a number ...')
        else:
            check = checkIfNodeExists(G, sourceNode)
            if check:
                loop1 = False
            else:
                loop1 = True

    # Loop to check if the desination node exists
    loop2 = True
    while(loop2):
        destNode = ''
        try:
            destNode = int(
                input('Please enter your destination router number : '))
        except:
            print('Wrong input. Please enter a number ...')
        else:
            check2 = checkIfNodeExists(G, destNode)
            if check2 and (sourceNode != destNode):
                loop2 = False
            else:
                loop2 = True

    return sourceNode, destNode

# ----------------------------------------------------------------------------
# FUNCTION NAME:     checkIfNodeExists(G, node)
# PURPOSE:           Checks if the passed node exists in the graph
# -----------------------------------------------------------------------------


def checkIfNodeExists(G, node):

    if G.has_node(node):
        return True
    else:
        print("Router", node, "could not be found in the network. Please try again.")
        return False


# ----------------------------------------------------------------------------
# FUNCTION NAME:     DisplayGraph()
# PURPOSE:           Displays a window graph that varies depending on input
# -----------------------------------------------------------------------------
def DisplayGraph(P, H, fig, shortestPath, spath, deadNodes, dnodes, dedges):

    G = P.copy()

    if shortestPath and deadNodes:

       # G original graph
        # H graph with only the good nodes
        # dnodes nodes that we removed
        # Want to leave only the bad nodes

        color_map = []
        i = 0

        # Make all nodes green
        for node in G:
            color_map.append('green')

        # Make the nodes that failed red
        for index, item in enumerate(dnodes):
            color_map[dnodes[index]-1] = 'red'

        # Remove the edges of all the failed nodes
        for index, item in enumerate(dnodes):
            edgesRemoved = list(G.edges(dnodes[index]))
            G.remove_edges_from(edgesRemoved)

        # Remove edges that failed
        G.remove_edges_from(dedges)

        # Setup graph
        plt.clf()
        pos = nx.circular_layout(G)
        nx.draw(G, pos, node_color=color_map,
                font_weight='bold', node_size=2000)
        edge_labels = nx.get_edge_attributes(G, 'failure')
        for key, value in edge_labels.items():
            edge_labels[key] = str(value) + "%"
        node_labels = nx.get_node_attributes(G, 'failure')
        for key, value in node_labels.items():
            node_labels[key] = str(key) + "\n" + str(value) + "%"
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='black', font_weight='bold')
        nx.draw_networkx_labels(G, pos, labels=node_labels,
                                font_color='black',  font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos, edgelist=spath, edge_color='g', width=3)
        ax = plt.gca()
        ax.margins(0.2)
        plt.figure(fig)
        plt.show(block=False)

    elif not shortestPath and deadNodes:

        # G original graph
        # H graph with only the good nodes
        # dnodes nodes that we removed
        # Want to leave only the bad nodes

        color_map = []
        i = 0

        # Make all nodes green
        for node in G:
            color_map.append('green')

        # Make the nodes that failed red
        for index, item in enumerate(dnodes):
            color_map[dnodes[index]-1] = 'red'

        # Remove the edges of all the failed nodes
        for index, item in enumerate(dnodes):
            edgesRemoved = list(G.edges(dnodes[index]))
            G.remove_edges_from(edgesRemoved)

        # Remove edges that failed
        G.remove_edges_from(dedges)

        # Setup graph
        plt.clf()
        pos = nx.circular_layout(G)
        nx.draw(G, pos, node_color=color_map,
                font_weight='bold', node_size=2000)
        edge_labels = nx.get_edge_attributes(G, 'failure')
        for key, value in edge_labels.items():
            edge_labels[key] = str(value) + "%"
        node_labels = nx.get_node_attributes(G, 'failure')
        for key, value in node_labels.items():
            node_labels[key] = str(key) + "\n" + str(value) + "%"
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='black', font_weight='bold')
        nx.draw_networkx_labels(G, pos, labels=node_labels,
                                font_color='black',  font_size=10, font_weight='bold')

        ax = plt.gca()
        ax.margins(0.2)
        plt.figure(fig)
        plt.show(block=False)

    elif not shortestPath and not deadNodes:

        # Setup graph
        plt.clf()
        pos = nx.circular_layout(G)
        nx.draw(G, pos, font_weight='bold', node_size=2000)
        edge_labels = nx.get_edge_attributes(G, 'failure')
        for key, value in edge_labels.items():
            edge_labels[key] = str(value) + "%"
        node_labels = nx.get_node_attributes(G, 'failure')
        for key, value in node_labels.items():
            node_labels[key] = str(key) + "\n" + str(value) + "%"
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='black', font_weight='bold')
        nx.draw_networkx_labels(G, pos, labels=node_labels,
                                font_color='black',  font_size=10, font_weight='bold')
        ax = plt.gca()
        ax.margins(0.2)
        plt.figure(fig)
        plt.show(block=False)

    elif shortestPath and not deadNodes:

        # Setup graph
        plt.clf()
        pos = nx.circular_layout(G)
        nx.draw(G, pos, font_weight='bold', node_size=2000)
        edge_labels = nx.get_edge_attributes(G, 'failure')
        for key, value in edge_labels.items():
            edge_labels[key] = str(value) + "%"
        node_labels = nx.get_node_attributes(G, 'failure')
        for key, value in node_labels.items():
            node_labels[key] = str(key) + "\n" + str(value) + "%"
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='black', font_weight='bold')
        nx.draw_networkx_labels(G, pos, labels=node_labels,
                                font_color='black',  font_size=10, font_weight='bold')
        nx.draw_networkx_edges(G, pos, edgelist=spath, edge_color='g', width=3)
        ax = plt.gca()
        ax.margins(0.2)
        plt.figure(fig)
        plt.show(block=False)


# ----------------------------------------------------------------------------
# FUNCTION NAME:     ObtainNodeData(G)
# PURPOSE:           Open the input files and populate graph with nodes, edges
# -----------------------------------------------------------------------------


def ObtainNodeData(G):

    # Read the nodes file and create nodes
    nFile = open('routers.txt', 'r')
    for line in nFile:
        line = line.replace('%', '')
        line = line.rstrip("\n")
        line = line.split('|')
        G.add_node(int(line[0]), failure=int(line[1]))

    # Read the edges file and create nodes
    nFile = open('links.txt', 'r')
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
