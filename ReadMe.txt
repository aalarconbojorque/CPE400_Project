Source Code Requirements
------------------------
1) Python3
2) Matplolib Python Plotting Module
3) Networkx Python Graph Module
4) Pip3 if any of the modules are not already installed

Instructions to install source code requirements if not already installed
--------------------------------------------------------
1) Install pip3 (package installer for Python):
sudo apt-get install python3-pip (Ubuntu)
2) Install Matplolib module :
pip3 install matplotlib
3) Install Networkx Python Graph Module:
pip3 install networkx

Source code notes
--------------------------------------------------------
1) routers.txt must be in the same directory as proj.py - contains routers information
Ex : 1|5% = Adds router 1 with a 5% chance of failure
Ex : 2|7% = Adds router 2 with a 7% chance of failure
2) links.txt must be in the same directory as proj.py - contains links information
Ex : 1|2|5% = Adds link from router 1 to 2 with a 5% chance of failure
Ex : 3|2|7% = Adds link from router 3 to 2 with a 7% chance of failure
3) During execution of the program a graph plot window will open and should remain open to visualize
the simulation as changes occur. If it is closed, executing a new simulation will reopen it.

Instructions to run source code
--------------------------------------------------------
1) python3 proj.py