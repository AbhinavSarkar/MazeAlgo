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

myList = LinkedList()
myList.add((24,24),24)
myList.add((12,32),23)
myList.add((11,32),22)
myList.print_list()

    
