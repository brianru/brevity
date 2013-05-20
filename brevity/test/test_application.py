import sys
sys.path.insert(0, '.')  # add parent folder to path list

import unittest
import application as br
import webtest
import webapp2

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed

### TEST WALKING SKELETON ###
class DisplayObjectOnWebTestCase(unittest.TestCase):
    """Store an object in NDB.
    Pass the object key through the url. https://developers.google.com/appengine/docs/python/ndb/keyclass#Key_urlsafe
    (/key=___)
    Access and display object using key from url.

    """
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        class Employee(ndb.Model):
            text = ndb.StringProperty()
        self.test_employee = Employee(text='I am a banana!')
        self.key = self.test_employee.put()
        self.testapp = webtest.TestApp(br.application)

    def runTest(self):
        test_object_url = '/view/' + self.key.urlsafe()
        response = self.testapp.get(test_object_url)
        self.assertEqual(self.key, ndb.Key(urlsafe=self.key.urlsafe()))  # parse response
        self.assertEqual(response.status_int, 200)
        self.assertIn(self.test_employee.text, response.normal_body)
        self.assertEqual(response.content_type, 'text/plain')

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
        test_text = 'I am a banana!'
        class Employee(ndb.Model):
            text = ndb.StringProperty()
        test_employee = Employee(text=test_text)
        test_key = test_employee.put()
        self.assertEquals(test_text, test_key.get().text)
        test_employee.text = 'My spoon is too big!'
        test_employee.put()
        self.assertEquals('My spoon is too big!', test_key.get().text)
        test_employee.price = len(test_employee.text)
        test_employee.put()
        self.assertEquals(len('My spoon is too big!'), test_key.get().price)

    def tearDown(self):
        self.testbed.deactivate()

### GENERAL UNIT TESTS ###
class StoreDataModelInNDBTestCase(unittest.TestCase):
    pass

class DisplayDataModelOnWebTestCase(unittest.TestCase):
    pass

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

