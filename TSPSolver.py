#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
    from PyQt5.QtCore import QLineF, QPointF
# elif PYQT_VER == 'PYQT4':
# 	from PyQt4.QtCore import QLineF, QPointF
else:
    raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))


import time
import numpy as np
from TSPClasses import *
from CityWrapper import *
import heapq
import itertools
INFINITY = math.inf


class TSPSolver:
    def __init__( self, gui_view ):
        self._scenario = None

    def setupWithScenario( self, scenario ):
        self._scenario = scenario


    ''' <summary>
        This is the entry point for the default solver
        which just finds a valid random tour.  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of solution, 
        time spent to find solution, number of permutations tried during search, the 
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    def defaultRandomTour( self, time_allowance=60.0 ):
        results = {}
        cities = self._scenario.getCities()
        ncities = len(cities)
        foundTour = False
        count = 0
        bssf = None
        start_time = time.time()
        while not foundTour and time.time()-start_time < time_allowance:
            # create a random permutation
            perm = np.random.permutation( ncities )
            route = []
            # Now build the route using the random permutation
            for i in range( ncities ):
                route.append( cities[ perm[i] ] )
            bssf = TSPSolution(route)
            count += 1
            if bssf.cost < np.inf:
                # Found a valid route
                foundTour = True
        end_time = time.time()
        results['cost'] = bssf.cost if foundTour else math.inf
        results['time'] = end_time - start_time
        results['count'] = count # Number of solutions discovered.
        results['soln'] = bssf # Object containing the route.
        results['max'] = None # Max size of the queue.
        results['total'] = None # Total states generated.
        results['pruned'] = None # Number of states pruned.
        return results


    ''' <summary>
        This is the entry point for the greedy solver, which you must implement for 
        the group project (but it is probably a good idea to just do it for the branch-and
        bound project as a way to get your feet wet).  Note this could be used to find your
        initial BSSF.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found, the best
        solution found, and three null values for fields not used for this 
        algorithm</returns> 
    '''

    # Time complexity: O(n^2) because we compare every city to every other city when
    #                  we are trying to find the min cost.
    # Space complexity: O(n). Because of a map of size n called visitedCities,
    #                   a heapQueue that is of size n (worst case),
    #                   and a route list of size n.
    def greedy(self, time_allowance=60.0):

        results = {}
        self._cities = self._scenario.getCities()
        visitedCities = {}

        self._startTime = time.time()
        self._time_allowance = time_allowance
        route = []
        route.append(self._cities[0])  # Add starting city to the route
        visitedCities[self._cities[0]._name] = True  # Prevent us from visiting our starting city

        runningCost = 0

        # For every city, get the minimal cost to another city and add it to our route
        i = 0
        counter = 0
        # This is O(n^2) because of an n size loop inside of an n size loop
        while (counter < len(self._cities)):
            currCity = self._cities[i]
            heapFromCurrCity = []

            # Find costs from current city to every other city
            for j in range(len(self._cities)):
                tempCity = self._cities[j]
                try:
                    isVisited = visitedCities[tempCity._name]  # Will not throw exception if city has
                    # been visited. Therefore, skip it.
                except:
                    cost = currCity.costTo(tempCity)
                    wrappedCity = CityWrapper(cost, tempCity, j)
                    heapq.heappush(heapFromCurrCity, wrappedCity)

            # Obtain the closest city, make it impossible to visit in the future, and add it to the route.
            if len(heapFromCurrCity) == 0:
                # currCity is the last city. We are done.
                break
            wrappedCity = heapq.heappop(heapFromCurrCity)
            closestCityToCurrentCity = wrappedCity._city
            cost = wrappedCity._cost

            i = wrappedCity._indexInCities
            visitedCities[closestCityToCurrentCity._name] = True  # Prevent us from visiting the closest city
            # in future calculations
            route.append(closestCityToCurrentCity)
            runningCost += cost
            counter += 1

        endTime = time.time()
        bssf = TSPSolution(route)
        bssf.cost = INFINITY
        if len(visitedCities.keys()) == len(self._cities):
            bssf.cost = runningCost

        timePassed = endTime - self._startTime

        results['time'] = timePassed
        results['cost'] = bssf.cost
        results['count'] = 0  # Number of solutions discovered. Will always be 1 for the greedy solution
        results['soln'] = bssf  # Object containing the route.
        results['max'] = 0  # Max size of the queue. Will always be 0 for the greedy solution
        results['total'] = 0  # Total states generated. Will always be 0 for the greedy solution
        results['pruned'] = 0  # Number of states pruned. Will always be 0 for the greedy solution

        return results


    ''' <summary>
        This is the entry point for the branch-and-bound algorithm that you will implement
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number solutions found during search (does
        not include the initial BSSF), the best solution found, and three more ints: 
        max queue size, total number of states created, and number of pruned states.</returns> 
    '''

    def branchAndBound( self, time_allowance=60.0 ):
        pass



    ''' <summary>
        This is the entry point for the algorithm you'll write for your group project.
        </summary>
        <returns>results dictionary for GUI that contains three ints: cost of best solution, 
        time spent to find best solution, total number of solutions found during search, the 
        best solution found.  You may use the other three field however you like.
        algorithm</returns> 
    '''
    # method that executes the 2 opt solve
    # PSEUDOCODE
    # repeat until no improvement is made or time runs out {
    #    start_again:
    #    best_distance = calculateTotalDistance(existing_route)
    #    for (i = 1; i < number of nodes eligible to be swapped; i++) {
    #       for (k = i + 1; k <= number of nodes eligible to be swapped; k++) {
    #           new_route = 2optSwap(existing_route, i, k)
    #           new_distance = calculateTotalDistance(new_route)
    #           if (new_distance < best_distance) {
    #               existing_route = new_route
    #               best_distance = new_distance
    #               goto start_again
    #           }
    #       }
    #   }
    # }
    # Time Complexity: O(n^4) because we have two nested for loops that iterate just under n times.
    #                  Inside of the double nested for loop, we call twoOptSwap() which is an O(n)
    #                  operation function. Surrounding all of this is a while loop that runs for as many
    #                  times as we find an improved solution (worst case is O(n)). Therefore, the total
    #                  time complexity is O(n^4).
    # Space Complexity: O(n^2) because we have a list called self._results['soln'].route object that
    #                   holds a unique routes that we generate from the twoOptSwap() function.
    #                   The worst case scenario is such that we generate n unique solutions for n cities,
    #                   thus, bringing the resulting worst case space complexity up to O(n^2).
    def fancy(self, time_allowance=60.0):
        self._generatedRoutes = {} # A map used to track unique routes our algorithm generates
        self._generatedRoutes[str(self._results['soln'].route)] = True # Add the first unique route
                                                                       # (found from the greedy solution)
                                                                       # to self._generatedRoutes
        self.initResults(time_allowance) # sets self_results to be equal to the greedy results
        self._startTime = time.time() # Initializing a global variable we will reference in a time checker function

        improvementMade = True

        # This while loop increases our time complexity to O(n^4) because it wraps an O(n^3) time complexity
        # operation. This while loop will iterate for as many times as we find a cheaper route (worst case is
        # n cheaper routes)
        while improvementMade and not self.isTimeUp():
            improvementMade = False
            existing_route = self._results['soln'].route
            best_distance = self._results['soln'].cost
            numNodesEligibleToBeSwapped = len(existing_route) - 1 # All nodes are eligible, except for the pivot node.
                                                                  # Therefore, elibible nodes = all cities - 1
            # This for loop makes the time complexity be O(n^3) because it performs O(n^2) operations
            # just under n times.
            for i in range(1, numNodesEligibleToBeSwapped):
                # This for loop makes the time complexity to be O(n^2)
                for k in range(1, numNodesEligibleToBeSwapped + 1):
                    # O(n) function call.
                    new_route, new_distance, isUniqueRoute = self.twoOptSwap(existing_route, i, k)
                    if new_distance < best_distance:
                        self._results['total'].route = new_route # Because we have generated a unique new state
                        self._results['soln'].route = new_route
                        self._results['soln'].cost = new_distance
                        improvementMade = True
                        k = INFINITY # Just to force us to leave repeat the loop
                        i = INFINITY # Just to force us to leave repeat the loop
                    elif isUniqueRoute:
                        self._results['pruned'] += 1 # A route is 'pruned' only if it is unique
                        self._results['total'].route = new_route  # Because we have generated a unique new state

        self._results['cost'] = self._results['soln'].cost
        return self._results

    # Time Complexity: O(1) because the City.costTo(OtherCity) function is O(1).
    # Space Complexity: O(1) because we are storing only an integer :)
    def updateRunningCost(self, new_route, runningCost):
        childCityIndex = len(new_route) - 1
        parentCityIndex = len(new_route) - 2
        runningCost += new_route[parentCityIndex].costTo(new_route[childCityIndex])
        return runningCost

    # Checks self._generatedRoutes to see if our new_route is actually a route that we have
    # created before, and have happened to re-create. This function is useful for updating
    # our total states created and total states pruned counts.
    #
    # Time Complexity: O(1) because we are performing only an get and an insertion into a map
    # Space Complexity: O(n) because in the end we will have a map of size n cities
    def checkIsUniqueRoute(self, new_route):
        isUniqueRoute = False

        try:
            existsInGeneratedRoutes = self._generatedRoutes[str(new_route)]
        except:
            # It threw an error because the key does not exist in self._generatedRoutes
            # therefore, it is a unique route
            # Add the unique route to self._generatedRoutes and then return True
            self._generatedRoutes[str(new_route)] = True
            isUniqueRoute = True

        return isUniqueRoute


    # Builds a swapped route, calculates its cost, and checks to see if this newly
    # created swapped route is unique or if it has been created before.
    #
    # Time Complexity: O(n) because we are adding every item from route to new_route, only
    #                  in a newly arranged manner.
    # Space Complexity: O(n) becauase we are building a new list (new_route) of size n cities
    def twoOptSwap(self, route, i, k):
        new_route = []
        runningCost = 0

        # Take route[0] to route[i - 1] and add them in order to new_route
        for index in range(i):
            new_route.append(route[index])
            if len(new_route) > 1: # Don't add the cost for the first city
                runningCost = self.updateRunningCost(new_route, runningCost)


        # Take route[i] to route[k] and add them in reverse order to new_route
        temp_index = k
        while temp_index >= i:
            new_route.append(route[temp_index])
            runningCost = self.updateRunningCost(new_route, runningCost)
            temp_index -= 1

        # Take route[k+1] to end and add them in order to new_route
        for index in range(k + 1, len(route)):
            new_route.append(route[index])
            runningCost = self.updateRunningCost(new_route, runningCost)

        # Makes sure we are returning a unique route because sometimes this
        # two opt function flips the new_route to something that we've already
        # generated
        isUniqueRoute = self.checkIsUniqueRoute(new_route)

        return new_route, runningCost, isUniqueRoute

    # Returns true if we have ran out of time
    #
    # Time Complexity: O(1) because we are performing constant time operations
    #                  with the time library
    # Space Complexity: O(1) because we are only updating global variables
    def isTimeUp(self):
        currTime = time.time()
        tempTimePassed = currTime - self._startTime
        totalTimePassed = tempTimePassed + self._results['time']
        if totalTimePassed >= self._time_allowance:
            return True # Time is up
        return False # Time is not up

    # Builds an initial BSSF from the greedy algorithm
    #
    # Time Complexity: Same as the greedy algorithm
    # Space Complexity: Same as the greedy algorithm
    def initResults(self, time_allowance):
        self._results = self.greedy(time_allowance)