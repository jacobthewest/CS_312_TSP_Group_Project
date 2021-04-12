# Adam Welker    CS 312   04/2021
#
# A Class that is used to make a branch and bound node
#
# DATA: a cost matrix, cost, a related city, a parent
#
# METHODS: getChildMatrix(p,n), getPath(), solveMatrix

import TSPClasses
import numpy as np
from copy import deepcopy

class TSPNODE:

    cost = 0
    cost_matrix = []
    depth = 0
    city = None
    parent = None

    # All data must be defined in the constructor
    def __init__(self, matrix, cost, city, parent, depth):

        self.cost_matrix = matrix
        self.cost = cost
        self.city = city
        self.parent = parent
        self.depth = depth

        # reduce the matrix
        self.reduceMatrix()

    def __lt__(self, other):

        return self.depth < other.depth

    # a function that reduces the matrix given to the node and adds any
    # reduction costs to the node's cost var
    def reduceMatrix(self):

        # go through each row and find the min
        for i in range(0, len(self.cost_matrix)):

            #find the min
            minimum = np.inf
            for j in range(0, len(self.cost_matrix[i])):

                if self.cost_matrix[i][j] < minimum:

                    minimum = self.cost_matrix[i][j]

            # if the min is not 0 or inf
            if minimum != 0 and minimum != np.inf:

                # add the min to the cost total
                self.cost += minimum

                # subtract the min from every row

                for j in range(0, len(self.cost_matrix[i])):

                    self.cost_matrix[i][j] = self.cost_matrix[i][j] - minimum

        # now do the same for each column

        for j in range(0, len(self.cost_matrix[0])):

            # find the min
            minimum = np.inf

            for i in range(0, len(self.cost_matrix)):

                if self.cost_matrix[i][j] < minimum:

                    minimum = self.cost_matrix[i][j]

            # if the min is not 0 or inf
            if minimum != 0 and minimum != np.inf:

                # add the min to the cost total
                self.cost += minimum

                # subtract the min from every row

                for i in range(0, len(self.cost_matrix)):
                    self.cost_matrix[i][j] = self.cost_matrix[i][j] - minimum




    # Recursively gets the current path using the parents
    def getPath(self):

        if self.parent == None:

            return [self.city]

        else:

            return self.parent.getPath() + [self.city]


    # makes the cost reduction matrix for a child matrix going from fromNode, to toNode
    def getChildMatrix(self, fromNode, toNode):

        childMatrix = deepcopy(self.cost_matrix)

        for j in range(0, len(childMatrix[0])):

            childMatrix[fromNode][j] = np.inf

        for i in range(0, len(childMatrix)):

            childMatrix[i][toNode] = np.inf

        childMatrix[toNode][fromNode] = np.inf
        childMatrix[fromNode][toNode] = np.inf

        return childMatrix


