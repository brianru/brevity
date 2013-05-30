import sys
import unittest

import webtest
from google.appengine.ext import ndb, testbed, db

import application as app
import model

sys.path.insert(0, '.')  # add parent folder to path list



class RandomDataGeneratorTestCase(unittest.TestCase):
    """Verify helper methods create valid test data.
    Other methods are factory methods.
    Factory methods should be moved to a SampleData factory class in production code.
    
    """
    def setUp(self):
        self.dataGenerator = model.RandomDataGenerator()
        self.SAMPLE_SIZE = 3
    
    def runTest(self):
        """1) Random text -> dictionary values from text
        2) Random text -> dictionary keys and values from text

        """
        self.assertEquals(len(self.dataGenerator.randomText(self.SAMPLE_SIZE).splitlines()),
                          self.SAMPLE_SIZE)
        testVariableKeys = self.dataGenerator.randomVariableKeys(self.SAMPLE_SIZE)
        self.assertEquals(len(testVariableKeys), self.SAMPLE_SIZE)
        self.assertEquals(len(self.dataGenerator.randomDictionary(self.SAMPLE_SIZE)),
                          self.SAMPLE_SIZE)


class SampleObjectFactoryTestCase(unittest.TestCase):
    """Ensure this class does not overlap with ConsistentAndCompleteDataModelTestCase.

    """
    def setUp(self):
        self.objectFactory = model.SampleObjectFactory()
        self.dataGenerator = model.RandomDataGenerator()
        self.test_socket = model.Socket(text=self.dataGenerator.randomText(3),
                                     variables=self.dataGenerator.randomDictionary(3))

    def runTest(self):
        self.testSocketFactory()
        self.testNodeFactory()
        self.testDocumentFactory()
        self.testAmendmentFactory()
        self.testAgreementFactory()

    def testSocketFactory(self):
        sample_with_variations = self.objectFactory.objectVariationsOf(self.test_socket).append(self.test_socket)
        print('\nsample with variations: \n %s' % (sample_with_variations))
        self.assertEquals(sample_with_variations, list(set(sample_with_variations)))

    @unittest.skip("Stub")
    def testNodeFactory(self):
        pass

    @unittest.skip("Stub")
    def testDocumentFactory(self):
        pass

    @unittest.skip("Stub")
    def testAmendmentFactory(self):
        pass

    @unittest.skip("Stub")
    def testAgreementFactory(self):
        pass

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

class ReadAndWriteFromNDBTestCase(unittest.TestCase):
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

    def runTest(self):
        self.testWithSampleClass()
        self.testWithDataModel()

    def testWithSampleClass(self):
        test_text = 'I am a banana!'
        class Employee(ndb.Model):
            text = ndb.StringProperty()
        test_employee = Employee(text=test_text)
        test_key = test_employee.put()
        self.assertEquals(test_text, test_key.get().text)
        test_employee.text = 'My spoon is too big!'
        test_employee.put()
        self.assertEquals('My spoon is too big!', test_key.get().text)
        test_employee.text_length = len(test_employee.text)
        test_employee.put()
        self.assertEquals(len('My spoon is too big!'), test_key.get().text_length)

    def testWithDataModel(self):
        self.testWithSocket()
        self.testWithNode()
        self.testWithDocument()
        self.testWithAmendment()
        self.testWithAgreement()

    def testWithSocket(self):
        test_socket = model.Socket(text='I am a ${fruit}!', variables={'fruit': 'banana'})
        test_socket_key = test_socket.put()
        self.assertEquals(test_socket_key.get(), test_socket)
        test_socket.variables = {'fruit': 'apple'}
        test_socket.put()
        self.assertEquals(test_socket_key.get(), test_socket)

    @unittest.skip("Test")
    def testWithNode(self):
        pass

    @unittest.skip("Test")
    def testWithDocument(self):
        pass

    @unittest.skip("Stub")
    def testWithAmendment(self):
        pass

    @unittest.skip("Stub")
    def testWithAgreement(self):
        pass

    def tearDown(self):
        self.testbed.deactivate()

class CompleteAndConsistentDataModelTestCase(unittest.TestCase):
    """Verify data model ensures data is well-formed (i.e. consistent and complete).
    1) Assign sample object contents to local variables.
    2) Instantiate component instance with sample object contents.
    3) Assert contents of component instance equals sample object contents.
    4) Validate obja == objb iff obja.contents == objb.contents
    5) Test content type restrictions raise expected exceptions.
    """
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

    @unittest.skip("Stub")
    def testNode(self):
        pass

    @unittest.skip("Stub")
    def testDocument(self):
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

