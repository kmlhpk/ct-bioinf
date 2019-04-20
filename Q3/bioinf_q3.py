import numpy as np

f = open('matrix1.txt', 'r')
mat = [[x for x in line.split(" ")] for line in f]
f.close()

spec = [x for x in mat[0][1:len(mat)]]
spec[len(spec)-1] = spec[len(spec)-1][:-1]
#print(spec)

dist = [[None for x in range(1,len(mat))] for x in range(1,len(mat))]
for i in range (1,len(mat)):
    for j in range (1,len(mat)):
        dist[i-1][j-1] = int(mat[i][j])
dist = np.array(dist)
#print(dist)


minR = 0
minC = 1
mini = dist[minR][minC]

for row in range(0,len(dist)):
    for col in range(row+1,len(dist)):
        print(row,col)
        if dist[row][col] < mini:
            mini = dist[row][col]
            minR = row
            minC = col
        
print(minR," ",minC,":",dist[minR][minC])


# Add new row and col
# merge labels, add them to new row and col
# calculate new distances down new species col
# delete two merged species' rows and cols
# move everything along two rows and cols


# ADD NEW ROW+COL
dist = np.insert(dist,len(dist),0,axis=1)
dist = np.append(dist,[[0 for x in range(0, len(dist)+1)]],axis=0)
print(dist)

# MERGE LABELS
spec.append(spec[minR]+spec[minC])
print(spec)

# CALC NEW DISTANCES










'''
keep = min(minR,minC)
merge = max(minR,minC)
mat[0][keep] += mat[0][merge]
mat[keep][0] += mat[merge][0]

print(mat[0])
print(mat[keep])
'''

'''
for i in range (1,len(mat)):
    for j in range (1,len(mat)):
        mat[i][j] = int(mat[i][j])

mat[0][len(mat[0])-1] = mat[0][len(mat[0])-1][:-1]
'''