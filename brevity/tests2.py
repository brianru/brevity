import os
import pdb
import unittest
import xml.etree.ElementTree as etree
import application as br


##### UNIT TESTS #####

class BadInputTestCase(unittest.TestCase):
    """Ensure application crashesnand burns immediately when fed bad inputs."""
    def setUp(self):
        self.s1 = br.Socket('I want A{item1}', {'item1': 'cheese'})
        self.s2 = br.Socket('I want A{condiment} with my A{item2}.',
                            {'condiment': 'cheese', 'item2': 'nachos'})
        self.n1 = br.Node([self.s2])


class SocketBadInputTestCase(BadInputTestCase):
    """1) Instantiate socket with incompatible node
    2) Link incompatible node to existing socket

    """
    def runTest(self):
        self.assertRaises(ValueError,
                          lambda: br.Socket('I want A{item1}',
                                            {'item1': 'cheese'},
                                            self.n1))
        self.asertRaises(ValueError, self.s1.link_node(self.n1))


class NodeBadInputTestCase(BadInputTestCase):
    """1) Instantiate empty node

    """
    def runTest(self):
        self.assertRaises(TypeError, lambda: br.Node())


class DocumentBadInputTestCase(BadInputTestCase):
    """1) Instantiate document with incompatible node
    2) Instantiate empty document

    """
    def runTest(self):
        self.assertRaises(ValueError,
                          lambda: br.Document([self.n1],
                                      {'place1': 'Dos Toros'}))
        self.assertRaises(ValueError, lambda: br.Document())


class DocumentConstructionTestCase(unittest.TestCase):
    """For each component, test update_xx method to ensure it correctly updates attributes.

    """


class DataTraversalTestCase(unittest.TestCase):
    """Create list of components. Traverse from head, popping the item from the list at each step. Assert list is empty at end of loop.

    """


class VisitorPatternTestCase(unittest.TestCase):
    """Verify every component type has an accept() method that calls the correct visit_component() method.

    """


class BuilderPatternTestCase(unittest.TestCase):
    pass


##### END-TO-END TESTS #####

class ReadXMLTestCase(unittest.TestCase):
    """Verify zero data loss."""


class WriteXMLTestCase(unittest.TestCase):
    """Verify zero data loss."""


class RoundTripXMLTestCase(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
