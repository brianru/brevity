#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import inspect
import sys
import unittest

from google.appengine.ext import ndb, db, testbed

import model


sys.path.insert(0, '.')  # add parent folder to path list


def activateDatastoreTestbed():
    activeTestbed = testbed.Testbed()
    activeTestbed.activate()
    activeTestbed.init_datastore_v3_stub()
    activeTestbed.init_memcache_stub()
    return activeTestbed


class CompleteAndConsistentDataModelTestCase(unittest.TestCase):
    """Verify data model ensures data is well-formed (i.e. consistent and complete).
    1) Assign sample object contents to local variables.
    2) Instantiate component instance with sample object contents.
    3) Assert contents of component instance equals sample object contents.
    4) Validate obja == objb iff obja.contents == objb.contents
    5) Test content type restrictions raise expected exceptions.
    """
    def setUp(self):
        self.testbed = activateDatastoreTestbed()
        self.objectFactory = model.SampleObjectFactory()

    def runTest(self):
        self.testSocket()
        self.testNode()
        self.testDocument()
        self.testAmendment()
        self.testAgreement()

    def testSocket(self):
        # 1
        test_text = 'I am a ${fruit}.'
        test_variables = {'fruit': 'banana'}
        # 2
        test_socket = model.Socket(text=test_text, variables=test_variables)
        # 3
        self.assertEquals(test_socket.text, test_text)
        self.assertEquals(test_socket.variables, test_variables)
        self.assertEquals(test_socket.linked_node, None)
        #4
        self.assertEquals(test_socket, model.Socket(text=test_text,
                                                 variables=test_variables))
        self.assertNotEquals(test_socket, model.Socket(text='',
                                                    variables=test_variables))
        self.assertNotEquals(test_socket, model.Socket(text=test_text,
                                                    variables=None))
        self.assertNotEquals(test_socket, model.Socket(text=test_text,
                                                    variables=test_variables,
                                                    linked_node=model.Node()))
        # 5
        self.assertRaises(db.BadValueError, lambda: model.Socket(text=0))
        self.assertRaises(db.BadValueError, lambda: model.Socket(variables=0))
        self.assertRaises(db.BadValueError, lambda: model.Socket(linked_node=0))
        ####### TEST LINKED NODES #######

    def testNode(self):
        nodeVariableKeys = []
        testNode = self.objectFactory.randomNode()
        for socket in testNode.sockets:
            nodeVariableKeys.extend(socket.get().variables.keys())
        self.assertEquals(sorted(nodeVariableKeys), sorted(list(set(nodeVariableKeys))))
        nodeSockets = sorted([x for x in testNode.sockets])
        self.assertEquals(nodeSockets, sorted(list(set(nodeSockets))))
        self.assertRaises(db.BadValueError, lambda: model.Node(sockets=0))
        self.assertRaises(db.BadValueError,
                          lambda: model.Node(sockets=[self.objectFactory.randomNode().put()]))
    
    def testDocument(self):
        documentVariableKeys = []
        sampleDocument = self.objectFactory.randomDocument()
        for node in sampleDocument.nodes:
            for socket in node.get().sockets:
                documentVariableKeys.extend(socket.get().variables.keys())
        self.assertEquals(sorted(documentVariableKeys),
                          sorted(list(set(documentVariableKeys))))
        documentNodes = sorted([x for x in sampleDocument.nodes])
        self.assertEquals(documentNodes, sorted(list(set(documentNodes))))
        self.assertRaises(db.BadValueError, lambda: model.Document(nodes=0))
        self.assertRaises(db.BadValueError, lambda: model.Document(nodes=self.objectFactory.randomSocket().put()))
        self.assertRaises(db.BadValueError, lambda: model.Document(variables=0))

    def testAmendment(self):
        self.assertEquals(0, 1)
    
    def testAgreement(self):
        self.assertEquals(0, 1)

    def tearDown(self):
        self.testbed.deactivate()


class RandomDataGeneratorTestCase(unittest.TestCase):
    """Verify helper methods create valid test data.
    Other methods are factory methods.
    Factory methods should be moved to a SampleData factory class in production code.
    
    """
    def setUp(self):
        self.dataGenerator = model.RandomDataGenerator()
        self.SAMPLE_SIZE = 3
    
    def runTest(self):
        self.assertEquals(len(self.dataGenerator.randomLinesOfText(self.SAMPLE_SIZE)),
                          self.SAMPLE_SIZE)
        testVariableKeys = self.dataGenerator.randomVariableKeys(self.SAMPLE_SIZE)
        self.assertEquals(len(testVariableKeys), self.SAMPLE_SIZE)
        self.assertEquals(len(self.dataGenerator.randomDictionary(self.SAMPLE_SIZE)),
                          self.SAMPLE_SIZE)


class SampleObjectFactoryTestCase(unittest.TestCase):
    """Ensure this class does not overlap with ConsistentAndCompleteDataModelTestCase.

    """
    def setUp(self):
        self.testbed = activateDatastoreTestbed()
        self.objectFactory = model.SampleObjectFactory()
        self.dataGenerator = model.RandomDataGenerator()
        self.testDataSet = self.objectFactory.randomInstanceOfEach()

    @unittest.expectedFailure
    def runTest(self):
        for testItem in self.testDataSet:
            testItemWithModifications = self.objectFactory.objectVariationsOf(testItem)
            testItemWithModifications.append(testItem)
            # TODO verify contents of testItemWithModifications.append(testItem) are unique
            self.assertEquals(len(testItemWithModifications), len(testItem._values)+1)
        listOfModelClasses = []
        for item in dir(model):
            itemClass = eval('model.' + item)
            if inspect.isclass(itemClass) and issubclass(itemClass, ndb.Model):
                listOfModelClasses.append(itemClass)
        listOfClassesFromObjectFactory = [dataInstance.__class__\
                                          for dataInstance\
                                          in self.objectFactory.randomInstanceOfEach()]
        self.assertEquals(sorted(listOfModelClasses), sorted(listOfClassesFromObjectFactory))

    def tearDown(self):
        self.testbed.deactivate()


class CRUDInNDBTestCase(unittest.TestCase):
    """Create test data.
    Instantiate test object with test data.
    Save test objects to database, maintaining keys.
    For each key, access objects and compare objects' values to test data.
    Add attribute. Confirm.
    Delete attribute. Confirm.

    """
    def setUp(self):
        self.testbed = activateDatastoreTestbed()
        self.objectFactory = model.SampleObjectFactory()

    def runTest(self):
        testData = self.objectFactory.randomInstanceOfEach()
        testDataKeys = [testItem.put() for testItem in testData]
        # Create // assert keys are returned
        self.assertEquals(len(testData), len(testDataKeys))
        for testItem in testDataKeys:
            self.assertIsInstance(testItem, ndb.Key)
        # Read // assert keys.get() equals test data items
        self.assertEquals(testData,
                          [testItem.get() for testItem in testDataKeys])
        # Update // update one property and .put(), assert keys match
        for testItem in testData:
            self.objectFactory.randomlyModify(testItem)
            self.assertIsInstance(testItem.put(), ndb.Key)
        # Delete // delete and assert keys.get() fails
        for testItem in testDataKeys:
            testItem.delete()
            self.assertIsNone(testItem.get())

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == "__main__":
    unittest.main()
