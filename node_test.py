# A python test to test the functionality of the node class
# this will use the problems found in HW 19 and 20

from TSPNODE import TSPNODE
import pytest
import numpy as nm


def test_initial_matrix():

    initial_Matrix = [[nm.inf, 7, 3, 12],
                      [3, nm.inf, 6, 14],
                      [5, 8, nm.inf, 6],
                      [9, 3, 5, nm.inf]]


    starting_node = TSPNODE(initial_Matrix, 0, 1, None)

    assert starting_node.cost == 15
    print(starting_node.cost_matrix)
    assert starting_node.getPath() == [1]

