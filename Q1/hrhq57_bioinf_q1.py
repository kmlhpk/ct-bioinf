#!/usr/bin/python
# This program was successfully tested using both Python 2.7.16 64-bit and 3.7.3 64-bit...
# ...however it runs a lot faster in 2.7 than 3.7!

import time
import sys

# YOUR FUNCTIONS GO HERE -------------------------------------
# 1. Populate the scoring matrix and the backtracking matrix

def initialise(a,b):
    # a should be len(seq1), b should be len(seq2)
    # Initialises a fresh scoring matrix of size a+1*b+1
    matrix_score = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    # Fills first row and column with appropriate scores
    for i in range(0,a+1):
        matrix_score[0][i] = -2*i
    for i in range(0,b+1):
        matrix_score[i][0] = -2*i
    
    # Initialises a fresh backtracking matrix of size a+1*b+1 
    matrix_track = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    # Fills first row and column with appropriate directions
    # 0 = end, 1 = left, 2 = up, 3 = diag
    matrix_track[0][0] = 0
    for i in range(1,a+1):
        matrix_track[0][i] = 1
    for i in range(1,b+1):
        matrix_track[i][0] = 2
    
    matrices=[matrix_score,matrix_track]
    return matrices

def populate(smat,tmat,seq1,seq2):
    # seq1 along "top" of matrix, seq2 along "left"
    # i = column index, ie. which element within a subarray
    # j = row index, ie. which subarray in main array
    # i relates to seq1, j relates to seq2
    # Populates scoring and backtracking matrices
    for i in range(1,len(seq1)+1):
        for j in range(1,len(seq2)+1):
            # Calculates potential scores for each direction
            upScore = smat[j-1][i] - 2
            leftScore = smat[j][i-1] - 2
            diagScore = smat[j-1][i-1]
            
            # Determines potential score when cell is diagonal
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
                
            # Picks maximum score, and populates matrices accordingly
            if diagScore >= upScore >= leftScore or diagScore >= leftScore >= upScore:
                smat[j][i] = diagScore
                tmat[j][i] = 3
            elif upScore >= leftScore >= diagScore or upScore >= diagScore >= leftScore:
                smat[j][i] = upScore
                tmat[j][i] = 2
            else:
                smat[j][i] = leftScore
                tmat[j][i] = 1
            
def backtrack(tmat,seq1,seq2):
    # Generates optimal alignment
    # Starts at bottom-right of backtracking matrix, works its way up and left according to directions
    row = len(seq2)
    col = len(seq1)
    best_alignment = ["",""]
    # Stops when it gets to top-left cell
    while tmat[row][col] != 0:
        # If direction is diagonal...
        if tmat[row][col] == 3:
            # Takes corresponding letters of seq1 and seq2, adds to alignment, deletes from end of seqs
            best_alignment[0] += seq1[len(seq1)-1]
            seq1 = seq1[0:len(seq1)-1]
            best_alignment[1] += seq2[len(seq2)-1]
            seq2 = seq2[0:len(seq2)-1]
            row -= 1
            col -= 1
        # If direction is up...
        elif tmat[row][col] == 2:
            # Takes corresponding letter of seq2, adds to alignment, deletes from end of seq2
            best_alignment[1] += seq2[len(seq2)-1]
            seq2 = seq2[0:len(seq2)-1]
            # Adds gap to other side of alignment
            best_alignment[0] += "-"
            row -= 1
        # If direction is left...
        elif tmat[row][col] == 1:
            # Takes corresponding letter of seq2, adds to alignment, deletes from end of seq2
            best_alignment[0] += seq1[len(seq1)-1]
            seq1 = seq1[0:len(seq1)-1]
            # Adds gap to other side of alignment
            best_alignment[1] += "-"
            col -= 1

    # Flips the alignment strings, as they're appended to in the "wrong" order
    best_alignment[0] = best_alignment[0][::-1]
    best_alignment[1] = best_alignment[1][::-1]
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

# Sets matrices
mats = initialise(len(seq1),len(seq2))
scoreMat = mats[0]
trackMat = mats[1]

# Populates matrices
populate(scoreMat,trackMat,seq1,seq2)

# Pulls best score from "final" cell of scoring matrix
best_score = scoreMat[len(scoreMat)-1][len(scoreMat[len(scoreMat)-1])-1]

# Gets best alignment
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

