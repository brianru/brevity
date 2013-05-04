import sys
sys.path.insert(0, '.')  # add parent folder to path list

import unittest
import application as br

from google.appengine.api import memcache
from google.appengine.ext import ndb
from google.appengine.ext import testbed


class DisplaySampleDataFromNDBOnWebTestCase(unittest.TestCase):
    """Populate database with sample data.
    Generate html request containing sample data.
    Verify html document contains all sample data.
    http://webapp-improved.appspot.com/guide/testing.html

    """


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
        retrieved_employee = test_key.get()
        self.assertEquals(test_text, retrieved_employee.text)

    def tearDown(self):
        self.testbed.deactivate()


class DisplayDataOnlineTestCase(unittest.TestCase):
    pass

class DisplayComponentsOnPageTestCase(unittest.TestCase):
    pass

if __name__ == "__main__":
    unittest.main()
