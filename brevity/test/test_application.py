import sys
sys.path.insert(0, '.')  # add parent folder to path list

import logging
import unittest
import application as br
import webtest
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed
from google.appengine.ext import db

### TEST WALKING SKELETON ###
class MainPageTestCase(unittest.TestCase):
    def setUp(self):
        self.testapp = webtest.TestApp(br.application)

    def runTest(self):
        response = self.testapp.get('/')
        self.assertEqual(response.status_int, 200)
        self.assertEqual(response.content_type, 'text/html')

class DisplayObjectOnWebTestCase(unittest.TestCase):
    """Tests /view/(.*)
    1) setUp testbed and testapp
    2) generate___ForWeb() create sample object and place in ndb
    3) call web and make assertions on response
    Store an object in NDB.
    Access and display object using key from url.

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testapp = webtest.TestApp(br.application)

    def runTest(self):
        self.displaySampleClassOnWeb()
        self.displayDataModelOnWeb()

    def displaySampleClassOnWeb(self):
        class Employee(ndb.Model):
            text = ndb.StringProperty()
        self.test_employee = Employee(text='I am a banana!')
        self.key = self.test_employee.put()

        test_object_url = '/view/' + self.key.urlsafe()
        response = self.testapp.get(test_object_url)
        self.assertEqual(self.key, ndb.Key(urlsafe=self.key.urlsafe()))  # parse response
        self.assertEqual(response.status_int, 200)
        self.assertIn(self.test_employee.text, response.normal_body)
        self.assertEqual(response.content_type, 'text/html')

    def displayDataModelOnWeb(self):
        self.displaySocketOnWeb()
        self.displayNodeOnWeb()
        self.displayDocumentOnWeb()
        self.displayAmendmentOnWeb()
        self.displayAgreementOnWeb()
    
    def displaySocketOnWeb(self):
        self.test_socket = br.Socket(text='I am a ${fruit}!', variables={'fruit': 'banana'})
        self.test_socket_key = self.test_socket.put()
        
        response = self.testapp.get('/view/' + self.test_socket_key.urlsafe())
        self.assertEqual(response.status_int, 200)
        self.assertIn(self.test_socket.text, response.normal_body)
        self.assertIn(str(self.test_socket.variables), response.normal_body)
        self.assertEqual(response.content_type, 'text/html')

    def displayNodeOnWeb(self):
        self.assertEquals(0, 1)

    def displayDocumentOnWeb(self):
        self.assertEquals(0, 1)

    def displayAmendmentOnWeb(self):
        self.assertEquals(0, 1)

    def displayAgreementOnWeb(self):
        self.assertEquals(0, 1)

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
        test_socket = br.Socket(text='I am a ${fruit}!', variables={'fruit': 'banana'})
        test_socket_key = test_socket.put()
        self.assertEquals(test_socket_key.get(), test_socket)
        test_socket.variables = {'fruit': 'apple'}
        test_socket.put()
        self.assertEquals(test_socket_key.get(), test_socket)

    def testWithNode(self):
        self.assertEquals(0, 1)

    def testWithDocument(self):
        self.assertEquals(0, 1)

    def testWithAmendment(self):
        self.assertEquals(0, 1)

    def testWithAgreement(self):
        self.assertEquals(0, 1)

    def tearDown(self):
        self.testbed.deactivate()

class ConsistentCompleteDataModelTestCase(unittest.TestCase):
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
        test_socket = br.Socket(text=test_text, variables=test_variables)
        # 3
        self.assertEquals(test_socket.text, test_text)
        self.assertEquals(test_socket.variables, test_variables)
        self.assertEquals(test_socket.linked_node, None)
        #4
        self.assertEquals(test_socket, br.Socket(text=test_text,
                                                 variables=test_variables))
        self.assertNotEquals(test_socket, br.Socket(text='',
                                                    variables=test_variables))
        self.assertNotEquals(test_socket, br.Socket(text=test_text,
                                                    variables=None))
        self.assertNotEquals(test_socket, br.Socket(text=test_text,
                                                    variables=test_variables,
                                                    linked_node=br.Node()))
        # 5
        self.assertRaises(db.BadValueError, lambda: br.Socket(text=test_text,
                                                      variables=test_variables,
                                                      linked_node=0))

    def testNode(self):
        self.assertEquals(0, 1)

    def testDocument(self):
        self.assertEquals(0, 1)

    def testAmendment(self):
        self.assertEquals(0, 1)

    def testAgreement(self):
        self.assertEquals(0, 1)

class ModifyDataModelFromWebTestCase(unittest.TestCase):
    pass

class CreateDataFromWebTestCase(unittest.TestCase):
    pass

class ExportDataFromWebTestCase(unittest.TestCase):
    pass

class ImportDataToWebTestCase(unittest.TestCase):
    pass


if __name__ == "__main__":
    unittest.main()

