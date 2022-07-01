import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
# %matplotlib inline
import copy
import math
import heapq

'''
The below script is based on a 55 * 57 maze. 
Todo 55 by 61 maze

This class
	2. Implement DFS algorithm to and A* with eucladian distance to find the shortest path in a maze

'''



width, height = 61, 55
X, Y = 14, 2

ori_img = mpimg.imread('maze.png')
img = ori_img[:,:,0]

class Cell:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.succ = ''
        self.action = ''  # which action the parent takes to get this cell
cells = [[Cell(i,j) for j in range(width)] for i in range(height)]




for i in range(height):
    succ = []
    for j in range(width):
        s = ''
        c1 = i * 16 + 8

        c2 =  j * 16 + 8

        if img[c1-8, c2] == 1: s += 'U'
        if img[c1+8, c2] == 1: s += 'D'
        if img[c1, c2-8] == 1: s += 'L'
        if img[c1, c2+8] == 1: s += 'R'
        cells[i][j].succ = s
        succ.append(s)
# 2    
#30 is range(height)/2, 54 is range height 

cells[0][30].succ = cells[0][30].succ.replace('U', '')
cells[54][30].succ = cells[54][30].succ.replace('D', '')

     

# bfs
visited = set()
s1 = {(0,30)}
s2 = set()
while (54,30) not in visited:
    for a in s1:
        visited.add(a)
        i, j = a[0], a[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in (s1 | s2 | visited): 
            s2.add((i-1,j))
            cells[i-1][j].action = 'U'
        if 'D' in succ and (i+1,j) not in (s1 | s2 | visited): 
            s2.add((i+1,j))
            cells[i+1][j].action = 'D'
        if 'L' in succ and (i,j-1) not in (s1 | s2 | visited): 
            s2.add((i,j-1))
            cells[i][j-1].action = 'L'
        if 'R' in succ and (i,j+1) not in (s1 | s2 | visited): 
            s2.add((i,j+1))
            cells[i][j+1].action = 'R'     
    s1 = s2
    s2 = set()


#print solution

print("visited rows")

for i in range(height):
    print()
    for x in range(width):
        totry = (i, x)
        if(totry in visited):
            if(x != (width - 1)):
                print("1,", end = '')
            else:
                print("1", end = '')
        else:
            if(x != (width - 1)):
                print("0,", end = '')
            else:
                print("0", end = '')



cur = (54,30)
s = ''
seq = []

while cur != (0,30):
    seq.append(cur)
    i, j = cur[0], cur[1]
    t = cells[i][j].action
    s += t
    if t == 'U': cur = (i+1, j)
    if t == 'D': cur = (i-1, j)
    if t == 'L': cur = (i, j+1)
    if t == 'R': cur = (i, j-1)
action = s[::-1]
seq = seq[::-1]





# 3 


## Part2
man = {(i,j): abs(i-54) + abs(j-30) for j in range(width) for i in range(height)}
euc = {(i,j): math.sqrt((i-54)**2 + (j-30)**2 ) for j in range(width) for i in range(height)}

# manhattan   use man
g = {(i,j): float('inf') for j in range(width) for i in range(height)}
g[(0,30)] = 0

queue = [(0,30)]
visited = set()

while queue and (54,30) not in visited:
    queue.sort(key=lambda x: g[x] + man[x])
    point = queue.pop(0)

    if point not in visited:
        visited.add(point)
        i, j = point[0], point[1]
        succ = cells[i][j].succ
        if 'U' in succ and (i-1,j) not in visited:
            if (i-1,j) not in queue: queue += [(i-1,j)]
            g[(i-1,j)] = min(g[(i-1,j)], g[(i,j)]+1)

        if 'D' in succ and (i+1,j) not in visited:
            if (i+1,j) not in queue: queue += [(i+1,j)]
            g[(i+1,j)] = min(g[(i+1,j)], g[(i,j)]+1)

        if 'L' in succ and (i,j-1) not in visited:
            if (i,j-1) not in queue: queue += [(i,j-1)]
            g[(i,j-1)] = min(g[(i,j-1)], g[(i,j)]+1)

        if 'R' in succ and (i,j+1) not in visited:
            if (i,j+1) not in queue: queue += [(i,j+1)]
            g[(i,j+1)] = min(g[(i,j+1)], g[(i,j)]+1)     


print("manhatten distance")

for i in range(height):
    print()
    for x in range(width):
        if(x != (width - 1)):
            print(man[i,x],",",end = '', sep='')    
        else:
            print(man[i,x],end = '', sep='')  
        

print('\n')



print("euclidian distance")
for i in range(height):
    print()
    for x in range(width):
        totry = (i, x)
        if(totry in visited):
            if(x != (width - 1)):
                print("1,", end = '')
            else:
                print("1", end = '')
        else:
            if(x != (width - 1)):
                print("0,", end = '')
            else:
                print("0", end = '')

#print tree
M = np.zeros([height*2+1, width*3+1]) # space

for h in range(height*2+1):
    for w in range(width*3 + 1):
        if(h%2==0) and (w%3==0):
            M[h,w] = 1
        
        if (h%2==0) and (w%3 !=0):
            i = int(h/2)
            j = int(np.floor(w/3))
            if np.sum(img[16*i + 0:16*i + 2, 16*j + 2:16*j + 16]) == 0:
                    M[h,w] = 2

        if (h%2 != 0) and (w%3 == 0):
            i = int(np.floor(h/2))
            j = int(w/3)
            if np.sum(img[16*i + 2:16*i+16, 16*j + 0:16*j + 2]) == 0:
                    M[h,w]=3
f = open("withoutSolution.txt",'a')
f.write('##1: \n')



#todo this
for h in range(height*2 + 1):
    for w in range(width*3 +1):
        if M[h,w]==0:
            f.write(' ')
        if M[h,w]==1:
            f.write('+')
        if M[h,w]==2:
            f.write('-')
        if M[h,w]==3:
            f.write('|')
    f.write('\n')
f.close()

for k in range(len(action)):
    
    i,j  = seq[k]
    a= action[k]
    M[2*i+1, 3*j+1:3*j+3]=4
    if a== 'U':
        M[2*i+0, 3*j+1:3*j+3] = 4
    if a=='D':
        M[2*i+2, 3*j+1: 3*j+3] = 4
    if a == 'L':
        M[2*i+1, 3*j+0] = 4
    if a == 'R':
        M[2*i+1, 3*j+3]=4

try: 
    i,j = seq[k + 1]
except:
    print("")


M[2*i+1, 3*j+1: 3*j+3] = 4

M[ 0,3*int((width-1)/2)+1:3*int((width-1)/2)+3]=4
M[-1,3*int((width-1)/2)+1:3*int((width-1)/2)+3]=4

f = open("treeWithSolution.txt",'a')
f.write('##4: \n')

for h in range(height*2+1):
    for w in range(width*3+1):
        if M[h,w]==0:
            f.write(' ')
        if M[h,w]==1:
            f.write('+')
        if M[h,w]==2:
            f.write('-')
        if M[h,w]==3:
            f.write('|')
        if M[h,w]==4:
            f.write('@')
    f.write('\n')
f.close()