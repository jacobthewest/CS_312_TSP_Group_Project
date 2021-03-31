# Adam Welker 02/2021   CS 312
#
# A class that makes a priority queue using a heap
# The Heap nodes will hold a node  and a matched queue number

import numpy as nm


class PriorityHeap:

    # The heap array -- here, nodes are sorted by index where
    # i_parent * 2 + 2 = i_right_child. The left child is adjacent to the
    # right child
    __heap = []
    __size = 0
    __map = []

    # An intializing function. Must put in max size in order to preallocate space

    def __init__(self, length):

        self.__heap = [[None, nm.inf]] * length
        self.__map = [None] * length

    # Gets the parent index of a node given it's array index
    def __getParent(self, node_index):

        return (node_index - 1) // 2

    # Gets the rightChild of a node given it's index
    def __getRightChild(self, node_index):

        return (2 * node_index) + 2

    def __getLeftChild(self, node_index):

        return (2 * node_index) + 1

    # A helper function to insert()
    # given a node index, moves it up or down the tree using a series of swaps

    def __MoveUp(self, node_index):

        # While the parent priority is greater than the child
        while node_index > 0 and self.__heap[self.__getParent(node_index)][1] > self.__heap[node_index][1]:
            #swap each other's positions on the node map

            child_node_number = self.__heap[node_index][0]._index
            parent_node_number = self.__heap[self.__getParent(node_index)][0]._index

            self.__map[child_node_number] = self.__getParent(node_index)
            self.__map[parent_node_number] = node_index

            #now swap the two

            temp = self.__heap[self.__getParent(node_index)]
            self.__heap[self.__getParent(node_index)] = self.__heap[node_index]
            self.__heap[node_index] = temp

            node_index = self.__getParent(node_index)

    def __MoveDown(self, node_index):

        left_index = self.__getLeftChild(node_index)
        right_index = self.__getRightChild(node_index)

        #TODO: Fix this conditional statement to make sure no index errors happen

        # if the right doesn't exist
        if right_index >= self.__size:
            if left_index < self.__size and self.__heap[node_index][1] > self.__heap[left_index][1]:
                #swap the map positions

                parent_node_num = self.__heap[node_index][0]._index
                child_node_num = self.__heap[left_index][0]._index

                self.__map[parent_node_num] = left_index
                self.__map[child_node_num] = node_index

                #swap the nodes
                temp  = self.__heap[left_index]
                self.__heap[left_index] = self.__heap[node_index]
                self.__heap[node_index] = temp

                self.__MoveDown(left_index)

        # if the left child doesn't exist
        elif left_index >= self.__size:

            if right_index < self.__size and self.__heap[node_index][1] > self.__heap[left_index][1]:
                #swap the map positions

                parent_node_num = self.__heap[node_index][0]._index
                child_node_num = self.__heap[right_index][0]._index

                self.__map[parent_node_num] = right_index
                self.__map[child_node_num] = node_index

                #swap the nodes
                temp = self.__heap[right_index]
                self.__heap[right_index] = self.__heap[node_index]
                self.__heap[node_index] = temp

                self.__MoveDown(right_index)

        elif self.__heap[right_index][1] > self.__heap[left_index][1]:

            parent_node_num = self.__heap[node_index][0]._index
            child_node_num = self.__heap[left_index][0]._index

            self.__map[parent_node_num] = left_index
            self.__map[child_node_num] = node_index

            # swap the nodes
            temp = self.__heap[left_index]
            self.__heap[left_index] = self.__heap[node_index]
            self.__heap[node_index] = temp

            self.__MoveDown(left_index)

        else:

            parent_node_num = self.__heap[node_index][0]._index
            child_node_num = self.__heap[right_index][0]._index

            self.__map[parent_node_num] = right_index
            self.__map[child_node_num] = node_index

            # swap the nodes
            temp = self.__heap[right_index]
            self.__heap[right_index] = self.__heap[node_index]
            self.__heap[node_index] = temp

            self.__MoveDown(right_index)


    # returns the number of elements in the swqueues
    def size(self):

        return self.__size

    # A function that inserts a number into the queue
    # INPUTS - value: the value to be inserted
    #        - priority: the priority value of the number
    def insert(self, node, priority):

        # create a data entry
        data = [node, priority]

        #update the size
        self.__size += 1

        #put the node in the heap
        self.__heap[self.__size - 1] = data

        #make a mapping

        self.__map[node._index] = self.__size - 1

        #move the node up
        self.__MoveUp(self.__size - 1)


    # Returns and also deletes the top item on the queue
    # OUTPUT: the item of lowest priority number. In the case of Dijkstra's algorithm, a node
    def delete_min(self):

        #if there's nothing then return zero
        if self.__size == 0:

            return

        # find the top value
        min = self.__heap[0][0]

        #swap the end leaf with the root and delete the root
        self.__map[self.__heap[0][0]._index] = None
        self.__heap[0] = self.__heap[self.__size - 1]


        self.__heap[self.__size - 1] = [None, nm.inf]
        self.__size -= 1

        # shift the root down and return the old root
        self.__MoveDown(0)
        return min

    # changes the priority number of a value in the queue
    # in this case self.insert() acts as a helper function
    # INPUTS - value: the value to be reprioritized
    #       -  priority: the new priority number of the value
    def decrease_Key(self, node, priority):


        #find the value on the map
        index = self.__map[node._index]

        if index == None:

            return

        # change the value
        oldPriority = self.__heap[index][1]
        self.__heap[index][1] = priority

        #move up or down the list accordingly
        if(priority < oldPriority):

            self.__MoveUp(index)

        else:

            self.__MoveDown(index)

    
    # finds if a node is in the queue
    def contains(self, node):

        return not(self.__map[node._index] == None)

    def getTopPriority(self):

        return self.__heap[0][1]

