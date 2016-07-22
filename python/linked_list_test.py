from linked_list import LinkedList
import unittest


class TestLinkedList(unittest.TestCase):
    def setUp(self):
        self.l_list = LinkedList()

    def test_insert_single_item_to_list(self):
        print self.l_list.length
        self.l_list.insert(10)
        #self.assertEquals(self.list.length, 0)