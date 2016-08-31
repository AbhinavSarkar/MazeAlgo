import numpy as np
import cv2

def viewCell(image, row, column):
    temp1 = row*20
    temp2 = temp1 + 20
    temp3 = column*20
    temp4 = temp3 + 20
    cell = image[temp1 : temp2, temp3 : temp4]
    return cell

def colourCell(image, row, column):
    cell = viewCell( image, row, column)
    for i in range(0,20):
        for j in range(0,20):
            if cell[i,j] >= 127:
                cell[i,j] = 200
    for i in range(row*20,(row*20)+20):
        for j in range(column*20, (column*20)+20):
            image[i,j] = cell[i - row*20, j - column*20]
    return image

def checkCellWalls(image, row, column):
    cell = viewCell(image, row, column)
    wallCode = 0
    if cell[0,10] <= 120:
        wallCode += 1
    if cell[10,19] <= 120:
        wallCode += 2
    if cell[19,10] <= 120:
        wallCode += 4
    if cell[10,0] <= 120:
        wallCode += 8
    return wallCode

def constructMazeArray(maze, image, length, breadth):
    for i in range(breadth/20):
        for j in range(length/20):
            maze[i,j] = checkCellWalls(image, i, j)
    return maze

def movePossibility(maze, i , j):
    tempStack = []
    tempStack.append(0)
    temp = maze[i,j]
    if temp/8 == 0:
        tempStack.append(4)
    else:
        temp = temp - 8
    if temp/4 == 0:
        tempStack.append(3)
    else:
        temp = temp - 4
    if temp/2 == 0:
        tempStack.append(2)
    else:
    	temp = temp - 2
    if temp/1 == 0:
        tempStack.append(1)
    return tempStack

def labelAdjacent(maze, mazeVisit, mazeVisit2, i, j, step_counter):
    paths = movePossibility(maze, i, j)
    while len(paths) != 1:
        temp = paths.pop()
        if temp == 1:
            if mazeVisit[i-1,j] != 0:
                mazeVisit2[i-1,j] = step_counter+1
                mazeVisit[i-1,j] = 0
        elif temp == 2:
            if mazeVisit[i,j+1] != 0:
                mazeVisit2[i,j+1] = step_counter+1
                mazeVisit[i,j+1] = 0
        elif temp == 3:
            if mazeVisit[i+1,j] != 0:
                mazeVisit2[i+1,j] = step_counter+1
                mazeVisit[i+1,j] = 0
        else:
            if mazeVisit[i,j-1] != 0:
                mazeVisit2[i,j-1] = step_counter+1
                mazeVisit[i, j-1] = 0
    return 0
            
def scanAdjacent(mazeVisit2, i, j, step_number):
    stack = []
    if i == 0:
        if j == 0:
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
        elif j == 9:
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
        else:
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
    elif i == 9:
        if j == 0:
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
        elif j == 9:
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
        else:
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
    else:
        if j == 0:
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
        elif j == 9:
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
        else:
            if mazeVisit2[i-1,j] == step_number-1:
                stack.append(1)
            if mazeVisit2[i,j+1] == step_number-1:
                stack.append(2)
            if mazeVisit2[i+1,j] == step_number-1:
                stack.append(3)
            if mazeVisit2[i,j-1] == step_number-1:
                stack.append(4)
    return stack

class tree(object):
    def __init__(self, pos, step_number, north = None, east = None, south = None, west = None):
        self.pos = pos
        self.step_number = step_number
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def __getPos__(self):
        return self.pos

    def __getStepNumber__(self):
        return self.step_number
        
        
        
                
    

fullImage = cv2.imread('C:\Users\ERTS\Documents\images\maze01.jpg')
gray_image = cv2.cvtColor(fullImage, cv2.COLOR_BGR2GRAY)
ret,binaryImage = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
breadth = len(binaryImage)
length = len(binaryImage[0])

maze = np.zeros((breadth/20, length/20),np.uint8)
mazeVisit = np.ones((breadth/20, length/20),np.uint8)
mazeVisit2 = np.ones((breadth/20, length/20),np.uint8)*(-1)
maze = constructMazeArray(maze, binaryImage, length, breadth)

start_i = 0
start_j = 0
stop_i = 20
stop_j = 20
pos_i = start_i
pos_j = start_j

print maze
print mazeVisit
print mazeVisit2

mazeVisit[pos_i, pos_j] = 0
step_counter = 0
mazeVisit2[pos_i, pos_j] = step_counter

#labelAdjacent(maze, mazeVisit, mazeVisit2, pos_i, pos_j, step_counter)
while mazeVisit[stop_i - 1, stop_j - 1] != 0:
    for i in range(stop_i):
        for j in range(stop_j):
            if mazeVisit2[i, j] == step_counter:
                labelAdjacent(maze, mazeVisit, mazeVisit2, i, j, step_counter)
    step_counter += 1
    ##raw_input("Press enter")
    ##print mazeVisit2

##tempMazeVisit2 = mazeVisit2
##Tree = tree((stop_i-1, stop_j-1),step_counter)
##pos_i = stop_i - 1
##pos_j = stop_j - 1
##while step_counter != 0:
##    tempstack = scanAdjacent(tempMazeVisit2, pos_i, pos_j, step_counter)
##    while len(tempstack) != 0:
##        temp = tempstack.pop()


print maze
print mazeVisit
print mazeVisit2
print step_counter




            
        




