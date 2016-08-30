import numpy as np
import cv2
import time
start_time = time.time()
def makeTile(wallCode):
    temp = wallCode
    tilePattern = np.ones((20,20), np.uint8)*255
    if temp/8==1:
       for i in range(0,2):
           for j in range(20):
               tilePattern[j,i] = 0;
       temp = temp - 8
    if temp/4 == 1:
       for i in range(20):
           for j in range(18,20):
               tilePattern[j,i] = 0;
       temp = temp - 4
    if temp/2 == 1:
       for i in range(18,20):
           for j in range(20):
               tilePattern[j,i] = 0;
       temp = temp - 2
    if temp/1 == 1:
       for i in range(2):
           for j in range(20):
               tilePattern[i,j] = 0;
    return tilePattern

def buildMazeImage(maze,length,breadth):
    fullPattern = np.ones((length*20,breadth*20), np.uint8)*255
    for i in range(length):
        for j in range(breadth):
            tile = makeTile(maze[i,j])
            for k in range(20):
                for l in range(20):
                    fullPattern[i*20+k,j*20+l]= tile[k,l]
    return fullPattern

def generateRandom(low,high,skip1,skip2):
    a = np.random.random_integers(low,high)
    while a == skip1 or a == skip2:
        a = np.random.random_integers(low,high)
    return a

def findAdjacent(mazeVisit,i,j,length, breadth):
    if i == 0:
        if j == 0:
            if mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 0:
                return 0
            elif mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 1:
                return 3
            elif mazeVisit[i,j+1] == 1 and mazeVisit[i+1,j] == 0:
                return 2
            else:
                return np.random.random_integers(2,3)
        elif j == length - 1:
            if mazeVisit[i,j-1] == 0 and mazeVisit[i+1,j] == 0:
                return 0
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i+1,j] == 1:
                return 3
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i+1,j] == 0:
                return 4
            else :
                return np.random.random_integers(3,4)
        else :
            if mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 0:
                return 0
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 1:
                return 3
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i+1,j] == 0:
                return 2
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i+1,j] == 1:
                return np.random.random_integers(2,3)
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 0:
                return 4
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i+1,j] == 1:
                return np.random.random_integers(3,4)
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 1 and mazeVisit[i+1,j] == 0:
                return generateRandom(2,4,3,3)     
            else :
                return np.random.random_integers(2,4)
    elif i == breadth - 1:
        if j == 0:
            if mazeVisit[i-1,j] == 0 and mazeVisit[i,j+1] == 0:
                return 0
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i,j+1] == 1:
                return 2
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i,j+1] == 0:
                return 1
            else:
                return np.random.random_integers(1,2)
        elif j == length - 1:
            if mazeVisit[i-1,j] == 0 and mazeVisit[i,j-1] == 0:
                return 0
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i,j-1] == 1:
                return 4
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i,j-1] == 0:
                return 1
            else :
                a = np.random.random_integers(1,4)
                while a == 3 or a == 2:
                    a = np.random.random_integers(1,4)
                return a
        else :
            if mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i-1,j] == 0:
                return 0
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i-1,j] == 1:
                return 1
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i-1,j] == 0:
                return 2
            elif mazeVisit[i,j-1] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i-1,j] == 1:
                return np.random.random_integers(1,2)
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i-1,j] == 0:
                return 4 
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i-1,j] == 1:
                a = np.random.random_integers(1,4)
                while a == 2 or a == 3:
                    a = np.random.random_integers(1,4)
                return a
            elif mazeVisit[i,j-1] == 1 and mazeVisit[i,j+1] == 1 and mazeVisit[i-1,j] == 0:
                a = np.random.random_integers(2,4)
                while a == 3:
                    a = np.random.random_integers(2,4)
                return a
            else :
                a = np.random.random_integers(1,4)
                while a == 3:
                    a = np.random.random_integers(1,4)
                return a
    else :
        if j == 0:
            if mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0:
                return 0
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1:
                return 2
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0:
                return 3
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 1:
                return np.random.random_integers(2,3)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0:
                return 1
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1:
                return np.random.random_integers(1,2)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0:
                a = np.random.random_integers(1,3)
                while a == 2:
                    a = np.random.random_integers(1,3)
                return a
            else :
                return np.random.random_integers(1,3)
        elif j == length - 1:
            if mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j-1] == 0:
                return 0
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j-1] == 1:
                return 4
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j-1] == 0:
                return 3
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j-1] == 1:
                return np.random.random_integers(3,4)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j-1] == 0:
                return 1
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j-1] == 1:
                return generateRandom(1,4,2,3)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j-1] == 0:
                return generateRandom(1,3,2,2)
            else :
                return generateRandom(1,4,2,2)
        else:
            if mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 0:
                return 0
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 1:
                return 4
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 0:
                return 2
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 1:
                return generateRandom(2,4,3,3)
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 0:
                return 3
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 1:
                return np.random.random_integers(3,4)
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 0:
                return np.random.random_integers(2,3)
            elif mazeVisit[i-1,j] == 0 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 1:
                return np.random.random_integers(2,4)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 0:
                return 1
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 1:
                return generateRandom(1,4,2,3)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 0:
                return np.random.random_integers(1,2)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 0 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 1:
                return generateRandom(1,4,3,3)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 0:
                return generateRandom(1,3,2,2)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 0 and mazeVisit[i,j-1] == 1:
                return generateRandom(1,4,2,2)
            elif mazeVisit[i-1,j] == 1 and mazeVisit[i+1,j] == 1 and mazeVisit[i,j+1] == 1 and mazeVisit[i,j-1] == 0:
                return np.random.random_integers(1,3)
            else :
                return np.random.random_integers(1,4)

length = 10
breadth = 10
maze = np.ones((breadth, length),np.uint8)*15
maze_visit = np.ones((breadth, length),np.uint8)
start_i = np.random.random_integers(0,breadth - 1)
start_j = np.random.random_integers(0,length - 1)
stack = []

pos_i = start_i
pos_j = start_j
stack.append((pos_i, pos_j))
maze_visit[pos_i, pos_j] = 0

while len(stack) != 0:
    temp = findAdjacent(maze_visit,pos_i,pos_j,length, breadth)
    if temp == 1:
        maze[pos_i,pos_j] += -1
        pos_i += -1
        maze[pos_i,pos_j] += -4
        stack.append((pos_i,pos_j))
        maze_visit[pos_i,pos_j] = 0
    elif temp == 2:
        maze[pos_i,pos_j] += -2
        pos_j += 1
        maze[pos_i,pos_j] += -8
        stack.append((pos_i,pos_j))
        maze_visit[pos_i,pos_j] = 0
    elif temp == 3:
        maze[pos_i,pos_j] += -4
        pos_i += 1
        maze[pos_i,pos_j] += -1
        stack.append((pos_i,pos_j))
        maze_visit[pos_i,pos_j] = 0
    elif temp == 4:
        maze[pos_i,pos_j] += -8
        pos_j += -1
        maze[pos_i,pos_j] += -2
        stack.append((pos_i,pos_j))
        maze_visit[pos_i,pos_j] = 0
    else:
        prev = stack.pop()
        pos_i = prev[0]
        pos_j = prev[1]

print maze
print maze_visit
print stack

fullPattern = buildMazeImage(maze,breadth,length)
cv2.imshow('canvas', fullPattern)
cv2.imwrite('C:\Users\ERTS\Documents\images\maze10by10\maze05.jpg', fullPattern)

print("--- %s seconds ---" % (time.time() - start_time))
cv2.waitKey(0)
cv2.destroyAllWindows()

