# This program written and tested using Python 3.7.3 64-bit

import numpy as np
import time
import networkx as nx
import matplotlib.pyplot as plt

def WPGMA(txt):
    # Starts timer
    start = time.time()
    
    # Transfers text input into workable matrix
    f = open(txt, 'r')
    mat = [[x for x in line.split(" ")] for line in f]
    f.close()
    
    # Pulls species labels into array (only 1D needed as mat is symmetrical)
    spec = [x for x in mat[0][1:len(mat)]]
    spec[len(spec)-1] = spec[len(spec)-1][:-1]
    
    # Pulls species distances into matrix
    dist = [[None for x in range(1,len(mat))] for x in range(1,len(mat))]
    for i in range (1,len(mat)):
        for j in range (1,len(mat)):
            dist[i-1][j-1] = float(mat[i][j])
    dist = np.array(dist)
    
    # Initalises graph for plotting, and x-position marker for nodes
    G=nx.Graph()
    nextPos = 0
    
    # Repeats until it merges all species into one
    while len(spec) > 1:
        # Finds smallest species distance; if > 1 have same distance, uses the last one it finds
        minR = 0
        minC = 1
        mini = dist[minR][minC]
        end=len(dist)
        # Entire algorithm only uses the top-right triangle of the symmetrical matrix, only touching...
        # ...the bottom-left when it comes time to fix & display it
        for row in range(0,end):
            for col in range(row+1,end):
                if dist[row][col] <= mini:
                    mini = dist[row][col]
                    minR = row
                    minC = col

        # Adds new col to distances matrix
        dist = np.insert(dist,len(dist),0,axis=1)
        # Adds new row to distances matrix (while not directly useful, it maintains symmetry)
        dist = np.append(dist,[[0 for x in range(0, len(dist)+1)]],axis=0)
        
        # Calculates new species' species distances
        end = len(dist)
        smaller = min(minR,minC)
        bigger = max(minR,minC)
        for row in range(0,end-1):
            # Checks whether species currently being considered is before, between or after the two...
            # ...species being merged, as this has an effect on how to find relevant distances in matrix
            if row == minR or row == minC:
                continue
            # Implements WPGMA formula
            elif row < smaller:
                dist[row][end-1] = 0.5*(dist[row][minR] + dist[row][minC])
            elif smaller < row < bigger:
                dist[row][end-1] = 0.5*(dist[minR][row] + dist[row][minC])
            else:
                dist[row][end-1] = 0.5*(dist[minR][row] + dist[minC][row])
        
        # Deletes columns and rows corersponding to pre-merge species
        dist = np.delete(dist,(minR,minC),axis=0)
        dist = np.delete(dist,(minR,minC),axis=1)
        
        # Merges species labels
        newLab = spec[minR]+spec[minC]
        spec.append(newLab)
        
        # Plots next part of phylo tree
        # If neither to-merge species are in the graph already...
        if spec[minR] not in G.nodes() and spec[minC] not in G.nodes:
            # ...add both to bottom of graph and join with a node
            G.add_node(spec[minR],pos=(nextPos,0))
            nextPos += 1
            G.add_node(spec[minC],pos=(nextPos,0))
            nextPos += 1
            G.add_node(newLab,pos=(nextPos-1.5,len(newLab)/2))
            G.add_edge(spec[minR],newLab)
            G.add_edge(spec[minC],newLab)
        # If one of them is...
        elif spec[minR] in G.nodes() and spec[minC] not in G.nodes:
            # ...add the missing one to the bottom of the graph and join with a node
            G.add_node(spec[minC],pos=(nextPos,0))
            nextPos += 1
            G.add_node(newLab,pos=(nextPos-1.5,len(newLab)/2))
            G.add_edge(spec[minR],newLab)
            G.add_edge(spec[minC],newLab)
        # If one of them is...
        elif spec[minR] not in G.nodes() and spec[minC] in G.nodes:
            # ...add the missing one to the bottom of the graph and join with a node
            G.add_node(spec[minR],pos=(nextPos,0))
            nextPos += 1
            G.add_node(newLab,pos=(nextPos-1.5,len(newLab)/2))
            G.add_edge(spec[minR],newLab)
            G.add_edge(spec[minC],newLab)
        # If both of them are...
        else:
            # ...join them with a node
            G.add_node(newLab,pos=(nextPos-2.5,len(newLab)/2.5))
            G.add_edge(spec[minR],newLab)
            G.add_edge(spec[minC],newLab)
        
        # Gets rid of pre-merge species
        old1 = spec[minR]
        old2 = spec[minC]
        spec.remove(old1)
        spec.remove(old2)
        
        # Makes display matrix with species on top and left
        # Starts by fixing symmetry of matrix
        end=len(dist)
        for row in range(0,end):
            for col in range(row+1,end):
                dist[col][row] = dist[row][col]
        # Inserts species labels and blank space marker
        distS = dist.astype(str)
        distS = np.insert(distS,0,spec,axis=0)
        spec.insert(0,"-")
        distS = np.insert(distS,0,spec,axis=1)
        spec.remove("-")
        print(distS)

    # Draws completed graph
    pos = nx.get_node_attributes(G,'pos')
    nx.draw_networkx(G,pos)
    
    # Saves graph to file
    graphName = "phylo_tree_"
    graphName = graphName + txt[::-1][4:][::-1] # this line gets rid of ".txt" from end of input
    graphName = graphName + ".png"
    plt.savefig(graphName)
    plt.clf()
    
    # Displays time taken to form matrix and graph
    stop = time.time()
    timeTaken = stop - start
    print("Time taken: ",timeTaken,"s")