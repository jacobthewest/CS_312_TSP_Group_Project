import pytest
from PriorityHeap import PriorityHeap

class node:

    node_id = None

    def __init__(self, id):

        self.node_id = id


def test_heap():
    array = PriorityHeap(6)

    node1 = node(0)
    node2 = node(1)
    node3 = node(2)
    node4 = node(3)
    node5 = node(4)
    node6 = node(5)

    array.insert(node1, -100)
    array.insert(node2, 1)
    array.insert(node3, -2)
    array.insert(node4, 3)
    array.insert(node5, -1)
    array.insert(node6, -500)


    array.decrease_Key(node1, -6)
    array.decrease_Key(node2,-5)
    array.decrease_Key(node3, -4)
    array.decrease_Key(node4, 5)
    array.decrease_Key(node5, 6)
    array.decrease_Key(node6, 800)

    assert array.delete_min() == node1
    assert array.delete_min() == node2
    assert array.delete_min() == node3
    assert array.delete_min() == node4
    assert array.delete_min() == node5
    assert array.delete_min() == node6

    assert array.size() == 0

    print("donezo")


