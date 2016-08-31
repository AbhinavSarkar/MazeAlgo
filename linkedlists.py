import numpy as np
import cv2

class Node(object):
    def __init__(self, pos, step, next_node = None):
        self.pos = pos
        self.step = step
        self.next_node = next_node
    def get_pos(self):
        return self.pos
    def get_step(self):
        return self.step
    def get_next(self):
        return self.next_node
    def set_pos(self, pos):
        self.pos = pos
    def set_step(self, step):
        self.step = step
    def set_next(self, next_node):
        self.next_node = next_node

class LinkedList(object):
    def __init__(self, r = None):
        self.root = r
        self.size = 0
    def get_size(self):
        return self.size
    def add(self, pos, step):
        new_node = Node(pos, step, self.root)
        self.root = new_node
        self.size += 1
    def remove(self, d):
        this_node = self.root
        prev_node = None
        while this_node:
            if this_node.get_step() == d:
                if prev_node:
                    prev_node.set_next(this_node.get_next())
                else:
                    self.root = this_node
                self.size -= 1
                return  True
            else:
                prev_node = this_node
                this_node = this_node.get_next()
        return False
    def find_step(self, d):
        this_node = self.root
        while this_node:
            if this_node.get_step() == d:
                return d
            else:
                this_node = this_node.get_next()
        return None
    def print_list(self):
        this_node = self.root
        while this_node:
            print this_node.get_pos()
            print this_node.get_step()
            this_node = this_node.get_next()

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

mazeVisit[pos_i, pos_j] = 0
step_counter = 0
mazeVisit2[pos_i, pos_j] = step_counter

while mazeVisit[stop_i - 1, stop_j - 1] != 0:
    for i in range(stop_i):
        for j in range(stop_j):
            if mazeVisit2[i, j] == step_counter:
                labelAdjacent(maze, mazeVisit, mazeVisit2, i, j, step_counter)
    step_counter += 1

pos_i = stop_i - 1
pos_j = stop_j - 1
step = mazeVisit2[pos_i, pos_j]
tempMazeVisit2 = mazeVisit2
myList = LinkedList()
myList.add((pos_i,pos_j),step)
while pos_i != start_i and pos_j != start_j:
    tempStack = scanAdjacent(tempMazeVisit2, pos_i, pos_j, step)
    if len(tempStack) == 1:
        temp = tempStack.pop()
        if temp == 1:
            pos_i -= 1
        elif temp == 2:
            pos_j += 1
        elif temp == 3:
            pos_i += 1
        elif temp == 4:
            pos_j -= 1
        else:
            x= 3
        step = step - 1
        myList.add((pos_i, pos_j),step)
    else:
        while len(tempStack) != 0:
            temp = tempStack.pop()
            if temp == 1:
                
            elif temp == 2:
                
            elif temp == 3:
                
            elif temp == 4:
                
            else:
                x= 3
        

myList = LinkedList()
myList.add((24,24),24)
myList.add((12,32),23)
myList.add((11,32),22)
myList.print_list()

    
