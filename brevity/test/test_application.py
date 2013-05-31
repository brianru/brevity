import sys
import unittest

import webtest
from google.appengine.ext import ndb, testbed, db

import application as app
import model

sys.path.insert(0, '.')  # add parent folder to path list

# TODO: move to test/test_model.py
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


# TODO: move to test/test_model.py
class SampleObjectFactoryTestCase(unittest.TestCase):
    """Ensure this class does not overlap with ConsistentAndCompleteDataModelTestCase.

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.objectFactory = model.SampleObjectFactory()
        self.dataGenerator = model.RandomDataGenerator()
        self.testDataSet = self.objectFactory.randomInstanceOfEach()

    def runTest(self):
        for testItem in self.testDataSet:
            self.assertEquals(\
                    self.objectFactory.objectVariationsOf(testItem).append(testItem),
                    list(set(self.objectFactory.objectVariationsOf(testItem).append(testItem))))
        self.assertEquals([dataType\
                           for dataType\
                           in dir(model)\
                           if issubclass(dataType, ndb.Model)],
                          [dataInstance.__class__\
                           for dataInstance\
                           in  self.objectFactory.randomInstanceOfEach()])

class LoadMainPageTestCase(unittest.TestCase):
    def setUp(self):
        self.testapp = webtest.TestApp(app.application)

    def runTest(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'text/html')

class DisplayObjectOnWebTestCase(unittest.TestCase):
    """Tests /view/(.*)

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testapp = webtest.TestApp(app.application)
        self.objectFactory = model.SampleObjectFactory()
        self.test_data_keys = self.putTestDataInNDB()

    def putTestDataInNDB(self):
        return [x.put() for x in self.objectFactory.randomInstanceOfEach()]

    def runTest(self):
        for key in self.test_data_keys:
            response = self.testapp.get('/view/' + key.urlsafe())
            self.assertTrue(self.isValidHTTPResponse(response))
            self.assertTrue(self.HTTPResponseContains(response, str(key.get())))

    def isValidHTTPResponse(self, response):
        """Verify that input response status is OK and content type is html."""
        return response.status_int == 200 and response.content_type == 'text/html'

    def HTTPResponseContains(self, response, target_object):
        """Verify that inputted response contains inputted object."""
        return str(target_object) in response.normal_body

    def tearDown(self):
        self.testbed.deactivate()

# TODO: move to test/test_model.py
class CRUDInNDBTestCase(unittest.TestCase):
    """Create test data.
    Instantiate test object with test data.
    Save test objects to database, maintaining keys.
    For each key, access objects and compare objects' values to test data.
    Add attribute. Confirm.
    Delete attribute. Confirm.

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.objectFactory = model.SampleObjectFactory()

    def runTest(self):
        #TODO Separate tasks with helper methods.
        # Create // assert keys are returned
        # Read // assert keys.get() equals test data items
        # Update // update one property and .put(), assert keys match
        # Delete // delete and assert keys.get() fails
        for test_item in self.objectFactory.randomInstanceOfEach():
            self.assertEquals(test_item.put().get(), test_item)

    def tearDown(self):
        self.testbed.deactivate()

# TODO: move to test/test_model.py
class CompleteAndConsistentDataModelTestCase(unittest.TestCase):
    """Verify data model ensures data is well-formed (i.e. consistent and complete).
    1) Assign sample object contents to local variables.
    2) Instantiate component instance with sample object contents.
    3) Assert contents of component instance equals sample object contents.
    4) Validate obja == objb iff obja.contents == objb.contents
    5) Test content type restrictions raise expected exceptions.
    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
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

    def testNode(self):
        nodeVariables= []
        testNode = self.objectFactory.randomNode()
        for socket in testNode._values['sockets']:
            nodeVariables.extend(socket.get().variables)
        self.assertEquals(nodeVariables, list(set(nodeVariables)))
        # should disallow duplicate variable keys

        nodeSockets = [x for x in testNode.sockets]
        self.assertEquals(nodeSockets, list(set(nodeSockets)))
        # should disallow duplicate sockets (requires deep search)

        self.assertRaises(bd.BadValueError, lambda: model.Node(socket=0))
        # ensure nodes can only contain sockets (and not other nodes)

    def testDocument(self):
        # ensure nodes do not overlap (have identical variables)
        # disallow duplicate nodes
        # ensure document only contains nodes in nodes attribute
        pass

    @unittest.skip("Stub")
    def testAmendment(self):
        pass
    
    @unittest.skip("Stub")
    def testAgreement(self):
        pass

@unittest.skip("Stub")
class ModifyDataFromWebTestCase(unittest.TestCase):
    pass

@unittest.skip("Stub")
class CreateDataFromWebTestCase(unittest.TestCase):
    pass

@unittest.skip("Stub")
class ExportDataFromWebToXMLTestCase(unittest.TestCase):
    pass

@unittest.skip("Stub")
class ImportDataFromXMLToWebTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

