# Adam Welker 02/2021   CS 312
#
# A class that makes a priority queue using an array
# The Array will hold an int and a matched queue number

import numpy as nm


class PriorityArray:

    __queue = []


    # A function that inserts a number into the queue
    # INPUTS - value: the value to be inserted
    #        - priority: the priority value of the number
    def insert(self, value, priority):

        item = [value, priority]

        self.__queue.append(item)

        return

    # changes the priority number of a value in the queue
    # INPUTS - value: the value to be reprioritized
    #       -  priority: the new priority number of the value
    def decrease_Key(self, value, priority):

        # check if we can find the value in the list
        for i in range(0, len(self.__queue)):

            # if we find it change its priority value
            if value == self.__queue[i][0]:

                self.__queue[i][1] = priority


    # Returns and also deletes the top item on the queue
    # OUTPUT: the item of lowest priority number. In the case of Dijkstra's algorithm, a node
    def delete_min(self):

        min = nm.inf
        min_index = -1

        # go over the entire list
        for i in range(0, len(self.__queue)):

            # if we find a value with a lower priority value than min, make it the min
            if self.__queue[i][1] < min:

                min = self.__queue[i][1]
                min_index = i

        val = self.__queue[min_index]

        del self.__queue[min_index]

        return val[0]

    # returns the number of elements in the queues
    def size(self):

        return len(self.__queue)


    # TODO: Change this from just a dummy function to something that runs in constant time
    # finds if a node is in the queue
    def contains(self, node):

        return True
