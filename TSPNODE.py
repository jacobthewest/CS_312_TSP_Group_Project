# Adam Welker    CS 312   04/2021
#
# A Class that is used to make a branch and bound node
#
# DATA: a cost matrix, cost, a related city, a parent
#
# METHODS: getChildMatrix(p,n), getPath(), solveMatrix

import TSPClasses
import numpy as np

class TSPNODE:

    cost = 0
    cost_matrix = []
    city = None
    parent = None

    # All data must be defined in the constructor
    def __init__(self, matrix, cost, city, parent):

        self.cost_matrix = matrix
        self.cost = cost
        self.city = city
        self.parent = parent

        # reduce the matrix
        self.reduceMatrix()

    # a function that reduces the matrix given to the node and adds any
    # reduction costs to the node's cost var
    def reduceMatrix(self):

        # go through each row and find the min
        for i in range(0,len(self.cost_matrix)):

            #find the min
            minimum  = min(self.cost_matrix[i])

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



