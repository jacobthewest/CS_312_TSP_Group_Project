#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
from TSPNODE import TSPNODE
from Priority_Array import PriorityArray
import heapq
import itertools
from random import random



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
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
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

	def greedy(self, time_allowance=60.0):

		results = {}

		cities = self._scenario.getCities()

		route = []

		solution_found = False

		start_time = time.time()

		# BEGIN COMPUTATION HERE
		################################################################################################################

		route = []

		index = 0

		queue = PriorityArray()

		route.append(cities[index])

		for i in range(1, len(cities)):

			queue.insert(cities[i], cities[index].costTo(cities[i]))

		while queue.size() != 0 and time.time()-start_time < time_allowance:

			nextCity = queue.delete_min()

			route.append(nextCity)

			if queue.size() == 0:

				solution_found = True
				break


			for i in range(0, len(cities)):

				if queue.contains(cities[i]):

					queue.decrease_Key(cities[i], nextCity.costTo(cities[i]))


		# END COMPUTATION HERE
		################################################################################################################
		end_time = time.time()

		#make the route a loop

		greedySolution = TSPSolution(route)

		results['cost'] = greedySolution.cost if greedySolution.cost != np.inf and solution_found else np.inf
		results['time'] = end_time - start_time
		results['count'] = 1 if greedySolution.cost != np.inf and solution_found else 0
		results['soln'] = greedySolution
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
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

		#intialize the variables needed for computation
		results = {}

		cities = self._scenario.getCities()
		foundTour = False
		num_solutions = 0
		num_pruned = 0
		num_perm = 0
		largest_size = 0
		bssf = None



		starting_matrix = []

		for i in range(0, len(cities)):

			starting_matrix.append([None] * len(cities))

			for j in range(0, len(cities)):
				starting_matrix[i][j] = cities[i].costTo(cities[j])

		queue = []

		start_time = time.time()

		#BEGIN COMPUTATION HERE
		################################################################################################################

		# make the starting node from city[0]

		starting_Node = TSPNODE(starting_matrix, 0, cities[0], None, 1)

		heapq.heappush(queue, (starting_Node.depth, starting_Node)) # put the staring node into a heapqueue

		# find the upper bound by using a greedy path

		# if the greedy cannot find a solution, then return the results
		results = self.greedy(time_allowance)

		bssf = results['soln']
		if bssf.cost != np.inf:

			foundTour = True

		# while the queue is not empty and time hasn't run out
		while len(queue) != 0 and time.time() - start_time < time_allowance:

			# record the queue size
			if len(queue) > largest_size:

				largest_size = len(queue)


			#take the top node and increase the number of permutations that were increased
			topNode = heapq.heappop(queue)[1]

			#check to make sure that this wasn't a state left after a better solution was found
			if topNode.cost > bssf.cost:

				num_pruned += 1
				continue

			# if the node's depth is equal to the len(cities), then we've found a solution
			if topNode.depth == len(cities):

				foundTour = True
				num_solutions += 1

				# number of solutions found ++heapq.heappush(starting_Node.cost, starting_Node)

				if topNode.cost <= bssf.cost:

					bssf = TSPSolution(topNode.getPath())
					# make it the best solution and change the upper bound to it's length

				continue

			curr_index = topNode.city._index
			for j in range(0, len(cities)):

				# if the node goes to a previously visited city or bad path -- len == inf
				# move to next
				if topNode.cost_matrix[curr_index][j] != np.inf:

					newCost = topNode.cost + topNode.cost_matrix[curr_index][j]
					newNode = TSPNODE(topNode.getChildMatrix(curr_index, j), newCost, cities[j], topNode, topNode.depth + 1)
					num_perm += 1


				# elif the node is valid, but the length is greater than the upper bound
					# pruned ++
					# move on to next
					if newNode.cost >= bssf.cost:

						num_pruned += 1

					else: # else make node and put it in the queue

						heapq.heappush(queue, (newNode.cost/ newNode.depth, newNode))


		################################################################################################################
		# END COMPUTATION HERE AND CALCULATE TIME PASSEs

		end_time = time.time()

		num_pruned += len(queue)

		# Do any final book keeping

		# return the dictionary with all values
		results['cost'] = bssf.cost
		results['time'] = end_time - start_time
		results['count'] = num_solutions
		results['soln'] = bssf
		results['max'] = largest_size
		results['total'] = num_perm
		results['pruned'] = num_pruned
		return results




	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy(self, time_allowance=60.0):
		pass
		



