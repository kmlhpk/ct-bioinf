f = open('matrix1.txt', 'r')
mat = [[x for x in line.split(" ")] for line in f]
f.close()

for i in range (1,len(mat)):
    for j in range (1,len(mat)):
        mat[i][j] = int(mat[i][j])

mat[0][len(mat[0])-1] = mat[0][len(mat[0])-1][:-1]

print(mat)

mini = mat[1][2]
minR = 1         #make this more pythonic
minC = 2

for row in range(1,len(mat)):
    for col in range(row+1,len(mat)):
        if mat[row][col] < mini:
            mini = mat[row][col]
            minR = row
            minC = col
        
print(minR," ",minC,":",mat[minR][minC])

# merge labels
# calculate new distances along new species row
# calculate new distances along new species col
# collapse bottom row and right col - move rest of matrix up and to the left
# delete last row and col (should be empty)

# MERGE LABELS
winner = min(minR,minC)
loser = max(minR,minC)
mat[0][winner] += mat[0][loser]
mat[winner][0] += mat[loser][0]

print(mat[0])
print(mat[winner])


# NEW ROW
i = len(mat[minR])-1
#while mat[minR][i] != 0:
    





'''
spec = [x for x in mat[0][1:len(mat)]]
spec[len(spec)-1] = spec[len(spec)-1][:-1]
print(spec)

dist = [[None for x in range(1,len(mat))] for x in range(1,len(mat))]
for i in range (1,len(mat)):
    for j in range (1,len(mat)):
        dist[i-1][j-1] = int(mat[i][j])
print(dist)
'''