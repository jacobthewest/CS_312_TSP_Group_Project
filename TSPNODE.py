# Adam Welker    CS 312   04/2021
#
# A Class that is used to make a branch and bound node
#
# DATA: a cost matrix, cost, a related city, a parent
#
# METHODS: getChildMatrix(p,n), getPath()

import TSPClasses

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

        # assert data types
        assert type(city) == TSPClasses.City
        assert type(parent) == TSPNODE


    # Recursively gets the current path using the parents
    def getPath(self):

        if self.parent == None:

            return [self.city]

        else:

            return self.parent.getPath() + [self.city]



