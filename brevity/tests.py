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


class DataTraversalTestCase(unittest.TestCase):
    """Create list of components. Traverse from head, popping the item from the list at each step. Assert list is empty at end of loop.

    """
    def setUp(self):
        self.components = []
        self.s1 = br.Socket('This Sunday we are going to get a A{item1} with A{item2} for lunch.', {'item1': 'bialy', 'item2': 'cream cheese'})
        self.components.append(self.s1.oid)
        self.s2 = br.Socket('I think A{store1} has the best A{item1} in A{location1}.', {'store1': "Kossar's", 'location1': 'New York City'})
        self.components.append(self.s2.oid)
        self.n1 = br.Node([self.s1, self.s2])
        self.components.append(self.n1.oid)
        self.s5 = br.Socket('I think A{store1} has the best A{item1} in the entire A{location1}!', {'store1': "Kossar's", 'location1': 'New York City'})
        self.components.append(self.s5.oid)
        self.n4 = br.Node([self.s5])
        self.components.append(self.n4.oid)
        if not self.s2.link_node(self.n4):
            raise ValueError
        self.s3 = br.Socket('The A{item2} will be from A{store2}. They have great A{item3} A{item2}.', {'store2': "Russ and Daughter's", 'item3': 'goat'})
        self.components.append(self.s3.oid)
        self.n2 = br.Node([self.s3])
        self.components.append(self.n2.oid)
        self.s4 = br.Socket('We will also pick up some A{item4} for A{event1}.', {'item4': 'chopped liver', 'event1': 'Passover'})
        self.components.append(self.s4.oid)
        self.n3 = br.Node([self.s4])
        self.components.append(self.n3.oid)
        self.d1 = br.Document([self.n1, self.n2, self.n3])
        self.components.append(self.d1.oid)

    def runTest(self):
        t = br.TraversalVisitor()
        gen = t.get_generator(self.d1)
        for i in gen:
            self.components.remove(i.oid)
        else:
            self.assertFalse(self.components)


##### END-TO-END TESTS #####


class XMLTestCase(unittest.TestCase):
    def setUp(self):
        self.s1 = br.Socket('This Sunday we are going to get a A{item1} with A{item2} for lunch.', {'item1': 'bialy', 'item2': 'cream cheese'})
        self.s2 = br.Socket('I think A{store1} has the best A{item1} in A{location1}.', {'store1': "Kossar's", 'location1': 'New York City'})
        self.n1 = br.Node([self.s1, self.s2])
        self.s5 = br.Socket('I think A{store1} has the best A{item1} in the entire A{location1}!', {'store1': "Kossar's", 'location1': 'world'})
        self.n4 = br.Node([self.s5])
        self.s2.link_node(self.n4)
        self.s3 = br.Socket('The A{item2} will be from A{store2}. They have great A{item3} A{item2}.', {'store2': "Russ and Daughter's", 'item3': 'goat'})
        self.n2 = br.Node([self.s3])
        self.s4 = br.Socket('We will also pick up some A{item4} for A{event1}.', {'item4': 'chopped liver', 'event1': 'Passover'})
        self.n3 = br.Node([self.s4])
        self.d1 = br.Document([self.n1, self.n2, self.n3])


class ImportXMLTestCase(XMLTestCase):
    """Verify zero data loss."""
    def runTest(self):
        ctrl_obj = self.d1
        im = br.Importer()
        test_obj = im.import_from_xml('samples/reader_test.xml')
        self.assertEqual(test_obj, ctrl_obj)


class ExportXMLTestCase(XMLTestCase):
    """Verify zero data loss."""
    def runTest(self):
        ctrl_obj = 'samples/reader_text.xml'
        ex = br.ExporterDirector()
        import time
        test_obj = str(time.time()) + '.xml'
        ex.export_to_xml(self.d1, test_obj)
        with open(ctrl_obj, 'r') as x:
            with open(test_obj, 'r') as y:
                self.assertEqual(x.read(), y.read())


class RoundTripXMLTestCase(unittest.TestCase):
    """Try round-tripping every document in a test suite folder.
    Include XML -> TXT/MD/LaTeX -> XML
    and TXT/MD/LaTeX -> XML -> TXT/MD/LaTeX

    """

if __name__ == "__main__":
    unittest.main()
