import numpy as np
import time

def WPGMA(txt):
    start = time.time()
    # Transfers text input into workable matrix
    f = open(txt, 'r')
    mat = [[x for x in line.split(" ")] for line in f]
    f.close()
    
    # Pulls species labels into array (only 1D needed as mat is symmetrical)
    spec = [x for x in mat[0][1:len(mat)]]
    spec[len(spec)-1] = spec[len(spec)-1][:-1]
    
    #Pulls species distances into matrix
    dist = [[None for x in range(1,len(mat))] for x in range(1,len(mat))]
    for i in range (1,len(mat)):
        for j in range (1,len(mat)):
            dist[i-1][j-1] = float(mat[i][j])
    dist = np.array(dist)
    
    # Repeats until two species remaining, at which point merging becomes futile
    while len(spec) > 2: # change 2 to 1 to produce stupid pointless one-species matrix
        
        # Finds smallest species distance; if > 1 have same distance, uses the last one it finds
        minR = 0
        minC = 1
        mini = dist[minR][minC]
        
        end=len(dist)
        # Entire algorithm only uses the top-right triangle of the symmatrical matrix, only caring about...
        # ...the bottom-left when it comes time to display it
        for row in range(0,end):
            for col in range(row+1,end):
                if dist[row][col] <= mini: # maybe change this to < for speedup?#####################
                    mini = dist[row][col]
                    minR = row
                    minC = col

        # Adds new col to distances matrix
        dist = np.insert(dist,len(dist),0,axis=1)
        # Adds new row to distances matrix (while not useful, it maintains symmetry)
        dist = np.append(dist,[[0 for x in range(0, len(dist)+1)]],axis=0)
        
        # Calculates new species' species distances
        end = len(dist)
        smaller = min(minR,minC)
        bigger = max(minR,minC)
        for row in range(0,end-1):
            # Takes into account whether species currently being considered is before, between or after...
            # ...the two species currently being merged, as this has an effect on how to find distances
            if row == minR or row == minC:
                continue
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
        spec.append(spec[minR]+spec[minC])
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
    
    # Displays time taken to form matrix and graph
    stop = time.time()
    timeTaken = stop - start
    print("Time taken: ",timeTaken,"s")
    
    # Saves graph to file