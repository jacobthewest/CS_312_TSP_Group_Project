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


    starting_node = TSPNODE(initial_Matrix, 0, 1, None, 1)

    assert starting_node.cost == 15
    print(starting_node.cost_matrix)
    assert starting_node.getPath() == [1]


def test_child_matrix():

    initial_Matrix = [[nm.inf, 7, 3, 12],
                      [3, nm.inf, 6, 14],
                      [5, 8, nm.inf, 6],
                      [9, 3, 5, nm.inf]]

    starting_node = TSPNODE(initial_Matrix, 0, 1, None, 1)

    node12_cost = starting_node.cost + starting_node.cost_matrix[0][1]
    node12_depth = starting_node.depth + 1
    node12 = TSPNODE(starting_node.getChildMatrix(0, 1), node12_cost, 2, starting_node, node12_depth)

    print(node12.cost_matrix)
    assert node12.cost == 24
    assert node12.depth == 2
    assert node12.parent == starting_node
    assert node12.getPath() == [1,2]

    node13_cost = starting_node.cost + starting_node.cost_matrix[0][2]
    node13_depth = starting_node.depth + 1
    node13 = TSPNODE(starting_node.getChildMatrix(0, 2), node13_cost, 3, starting_node, node13_depth)

    print(node13.cost_matrix)
    assert node13.cost == 15
    assert node13.depth == 2
    assert node13.parent == starting_node
    assert node13.getPath() == [1, 3]

    node34_cost = node13.cost + node13.cost_matrix[2][3]
    node34_depth = node13.depth + 1
    node34 = TSPNODE(node13.getChildMatrix(2, 3), node34_cost, 4, node13, node34_depth)

    print(node34.cost_matrix)
    assert node34.cost == 15
    assert node34.depth == 3
    assert node34.parent == node13
    assert node34.getPath() == [1, 3, 4]

    node32_cost = node13.cost + node13.cost_matrix[2][1]
    node32_depth = node13.depth + 1
    node32 = TSPNODE(node13.getChildMatrix(2, 1), node32_cost, 2, node13, node32_depth)

    print(node32.cost_matrix)
    assert node32.cost == 18
    assert node32.depth == 3
    assert node32.parent == node13
    assert node32.getPath() == [1, 3, 2]





