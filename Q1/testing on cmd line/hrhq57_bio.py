#!/usr/bin/python

# Please run this file on Python 2.7.16

import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------

def initialise(a,b):
    
    matrix_score = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    for i in range(0,a+1):
        matrix_score[0][i] = -2*i
    for i in range(0,b+1):
        matrix_score[i][0] = -2*i
        
    # 0 = end
    # 1 = left
    # 2 = up
    # 3 = diag
    matrix_track = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    matrix_track[0][0] = 0
    for i in range(1,a+1):
        matrix_track[0][i] = 1
    for i in range(1,b+1):
        matrix_track[i][0] = 2
    
    matrices=[matrix_score,matrix_track]
    return matrices


def populate(smat,tmat,seq1,seq2):
    # i = column index, ie which element within a subarray
    # j = row index, ie which subarray in main array
    # i relates to seq1, j relates to seq2
    
    for i in range(1,len(seq1)+1):
        for j in range(1,len(seq2)+1):
            
            upScore = smat[j-1][i] - 2
            leftScore = smat[j][i-1] - 2
            diagScore = smat[j-1][i-1]
            
            if seq1[i-1] != seq2[j-1]:
                diagScore -= 3
            elif seq1[i-1] == "A" and seq2[j-1] == "A":
                diagScore += 4
            elif seq1[i-1] == "C" and seq2[j-1] == "C":
                diagScore += 3
            elif seq1[i-1] == "G" and seq2[j-1] == "G":
                diagScore += 2
            else:
                diagScore += 1            
                
            maxi = max(diagScore,upScore,leftScore)
            if diagScore == maxi:
                smat[j][i] = diagScore
                tmat[j][i] = 3
            elif upScore == maxi:
                smat[j][i] = upScore
                tmat[j][i] = 2
            else:
                smat[j][i] = leftScore
                tmat[j][i] = 1


def backtrack(tmat,seq1,seq2):
    row = len(seq2)
    col = len(seq1)
    best_alignment = ["",""]
    while row != 0 and col != 0:
        
        if tmat[row][col] == 2 or tmat[row][col] == 3:
            best_alignment[1] += seq2[len(seq2)-1]
            seq2 = seq2[0:len(seq2)-1]
        if tmat[row][col] == 1 or tmat[row][col] == 3:
            best_alignment[0] += seq1[len(seq1)-1]
            seq1 = seq1[0:len(seq1)-1]
            
        if tmat[row][col] == 2:
            best_alignment[0] += "-"
        elif tmat[row][col] == 1:
            best_alignment[1] += "-"
            
        if tmat[row][col] == 2 or tmat[row][col] == 3:
            row -=1
        if tmat[row][col] == 1 or tmat[row][col] == 3:
            col -=1
        
        
    best_alignment[0] =  best_alignment[0][::-1]
    best_alignment[1] =  best_alignment[1][::-1]
    return best_alignment
            
# ------------------------------------------------------------

# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------

# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
print("starting...")
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------

# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Intialise the scoring matrix and backtracking matrix and call the function to populate them
# Use the backtracking matrix to find the optimal alignment 
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 

mats = initialise(len(seq1),len(seq2))
scoreMat = mats[0]
trackMat = mats[1]

populate(scoreMat,trackMat,seq1,seq2)

best_score = scoreMat[len(scoreMat)-1][len(scoreMat[len(scoreMat)-1])-1]

best_alignment = backtrack(trackMat,seq1,seq2)

#-------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)------------------
# This calculates the time taken and will print out useful information 

stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------