#!/usr/bin/python
import time
import sys
import numpy as np


# YOUR FUNCTIONS GO HERE -------------------------------------

def initScore(a,b):
    # Sequence 1 goes on top of matrix, 2 goes on the left
    # a and b should be integers len(seq 1) and len(seq 2)
    matrix = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    for i in range(0,a+1):
        matrix[0][i] = -2*i
    for i in range(0,b+1):
        matrix[i][0] = -2*i
    return matrix
    
def initTrack(a,b):
    # 0 = end
    # 1 = left
    # 2 = up
    # 3 = diag
    # Sequence 1 goes on top of matrix, 2 goes on the left
    # a and b should be integers len(seq 1) and len(seq 2)
    matrix = [[None for x in range(0,a+1)] for x in range(0,b+1)]
    matrix[0][0] = "e"
    for i in range(1,a+1):
        matrix[0][i] = "l"
    for i in range(1,b+1):
        matrix[i][0] = "u"
    return matrix

def populate(smat,tmat,seq1,seq2,i,j):
    # i = column index, ie which element within a subarray
    # j = row index, ie which subarray in main array
    # i relates to seq1, j relates to seq2
    upScore = smat[j-1][i] - 2
    leftScore = smat[j][i-1] - 2
    diagScore = 0
    if seq1[i-1] == "A" and seq2[j-1] == "A":
        diagScore = smat[j-1][i-1] + 4
    elif seq1[i-1] == "C" and seq2[j-1] == "C":
        diagScore = smat[j-1][i-1] + 3
    elif seq1[i-1] == "G" and seq2[j-1] == "G":
        diagScore = smat[j-1][i-1] + 2
    elif seq1[i-1] == "T" and seq2[j-1] == "T":
        diagScore = smat[j-1][i-1] + 1
    else:
        diagScore = smat[j-1][i-1] - 3
    if diagScore == max(diagScore,upScore,leftScore):
        smat[j][i] = diagScore
        tmat[j][i] = "d"
    elif upScore == max(diagScore,upScore,leftScore):
        smat[j][i] = upScore
        tmat[j][i] = "u"
    else:
        smat[j][i] = leftScore
        tmat[j][i] = "l"

def backtrack(tmat,seq1,seq2):
    pos = [len(seq2),len(seq1)]
    best_alignment = ["",""]
    while pos != [0,0]:
        
        #print()
        #print("Current position: ",pos)
        #print("Letter at position: ",tmat[pos[0]][pos[1]])
        
        if tmat[pos[0]][pos[1]] == "d":
            best_alignment[0] += seq1[len(seq1)-1]
            seq1 = seq1[0:len(seq1)-1]
            best_alignment[1] += seq2[len(seq2)-1]
            seq2 = seq2[0:len(seq2)-1]
            pos[0] -= 1
            pos[1] -= 1
            #print(best_alignment)
            
        elif tmat[pos[0]][pos[1]] == "u":
            best_alignment[1] += seq2[len(seq2)-1]
            seq2 = seq2[0:len(seq2)-1]
            best_alignment[0] += "-"
            pos[0] -= 1
            #print(best_alignment)
            
        elif tmat[pos[0]][pos[1]] == "l":
            best_alignment[0] += seq1[len(seq1)-1]
            seq1 = seq1[0:len(seq1)-1]
            best_alignment[1] += "-"
            pos[1] -= 1
            #print(best_alignment)
            
    best_alignment[0] =  best_alignment[0][::-1]
    best_alignment[1] =  best_alignment[1][::-1]
    #print(best_alignment)
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
'''
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
'''
start = time.time()


#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# Intialise the scoring matrix and backtracking matrix and call the function to populate them
# Use the backtracking matrix to find the optimal alignment 
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 

seq1 = "GAATTCAATACTCCACTTTCCATTCTGTTCAAAGGTCACGTATAGTCCTGGGAATACTCAGGGTTCTCACTTCATGGCTATGCAGGTATTTGTTCCCACACTACTTAAATACATTAAATATCATTTACAGTAACATAAAAATCAAATGCTTAAGAATAAATCTAATGAAAGAGGTGCCAGAGGTCTGTATCAATATGAACAAGGCATTAAAATTAAAGGCGCCTAAATAAATGAAGAGAGATGCTATGTTCATTGCTCGAAAGGACTCAACACAGTTAAGGATGTCAGCTCTCCTCAGAGTGATCTAGAGATTCAATGTCATCCCAATAAAATACAGCAGGACATTTGTGAGAACTAGAAAGCTAGTTTAAATTACATAAAGTGGAAAAGACCTAGAATAGTCAAGACAAACTCGGAAAGAAATGAATAAAGTTGGAACACTTATAATACCAGATAGCAAGATTTACTATAAGTTCCCATTATTGGCCAGGTGTGGACGCTCATGCCTGTAATGCCAGCAGTTTAGGAAGCTGAGGTGGGTGGATCACTTGAGCCCAAGAGTTCAAGTCCAGCCTGAGCAACATGGCAAAACCACATCTCGACAACAACACATTGGCTGTGTGCTGGCAGGTATCTGTAATCTCAGCTACCCGTGAGGCTGGGGTGGGAGGACTGTCGGACCCCAGGAGGTTGCGGCTGCAGATCTTGCCCTTGCACTCCAGTCTGGGGGACAGTGAGACCCTGTCTCAAAAAAATGTTCCCATTTGTGAACCCCTCAAATTTGAGACAGGTCTCAGTTAATTTAGAAAGCTTATTTTGCCCAGGTTGAGAATGCACGTCCAACACAACCTCAGGGGGTCCTGACATGTGCCCAACCTCATGAGGTCTGACCAAGGCAGCCAGAGCACAGTCTGGTTTTATACATTTTAGGGAGATACGAGACATCAACATATGTCAGATGAACACTGGTTTTGTCTGGAAAGGCGGTAGAACTCGAAGC"
seq2 = "GAATTCAATACTCCTCTTTCCATTATGTTCTAAGGTCACTCTAGTCCTGGGATACCGGTTCTCACTTCTACTATGCAGGTTTTTGTTCCAACACACTTAAACAAAAATATCATTTATGTAACATAAAAATCAATGCGTAAGATAAATTAATGCAAGCTGTCGAGGTTGTTTCAAAGACAAGGCCTTAAAATTAAAGCGCCTATAAAAGAGTGCTATGTCATTCCTCGACAGGACTAACATAGTTAAGGAGTAACTCTCCTCAGAGTGACTAGAGATCCATGTCATCCCAAAAAATACAGCAGCACTCTATAACTAGTAAGTTAGGTTAATTACTAAACTGAAAAACCGAGAATAGTAACAACTCGCAAAAAAGATAAGTTGGAACACTATAATACCAGATAGCAAGATTTAAAATAGTTCCCATGTTGGCAGGTGTGGACGCCTGCCTGTAAGTTAGCAGTTAGGAAGCTGTGTTGTGATCACTTGAGCCCAAGTGTTCAAGGCCACCTTAGCACATGGCAAAACACTTCTCGACAACAACACATTCTGTGCGGCGTATAGTAATCTCATCGACCGTGAGGCGGGGTGGGAGGAGTGTCGGACACCAGGAGGTTGCGGCTCAGTTTTGCCCTTGCACCCAGTCTGTGGGAAGTGGACCTGTCCAAAAAAATGTTCCCATTTTGAACCCCTCAAATTTGACAGGTCTCGTTAATGTGAATGCTATTGCAGTTGAGAATCCACGTCCACACAATTCGGGGTCCTGCCATGGACAACCTCATGGGGTCTGACAAGGCAGAGAGCACAGACTCGTTTTATACCTTGGGGATCGAGACTCACAATGTCAGATGAAGACTGGTTTTGTCTGGAAAGGAGGTAGACTCCAGTGAGGGGCTTCCAGTCACAGGTAGATACAGACAAATGGCTGCATCTTTAAGTTCTGATTAGACCCTAGAGGAGGAATGGAATGTATTTATCTCATGACAGAGGGTGACTCGAAAGA"

len1 = len(seq1)
len2 = len(seq2)

scoreMat = initScore(len1,len2)
trackMat = initTrack(len1,len2)
scoreMat=np.array(scoreMat)
trackMat=np.array(trackMat)


for i in range(1,len1+1):
    for j in range(1,len2+1):
        populate(scoreMat,trackMat,seq1,seq2,i,j)
#print(trackMat)
        
best_alignment = backtrack(trackMat,seq1,seq2)
best_score = scoreMat[len(scoreMat)-1][len(scoreMat[len(scoreMat)-1])-1]

#-------------------------------------------------------------


# DO NOT EDIT (unless you want to turn off displaying alignments for large sequences)------------------
# This calculates the time taken and will print out useful information 

stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)
'''
'''
#-------------------------------------------------------------