#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys
import unittest

import webtest
from google.appengine.ext import testbed

import application as app
import model


sys.path.insert(0, '.')  # add parent folder to path list


class AbstractWebtestBaseClass(unittest.TestCase):
    """Provide helper methods."""
    def setUp(self):
        self.testapp = webtest.TestApp(app.application)

    def putTestDataInNDB(self):
        return [item.put() for item in self.objectFactory.randomInstanceOfEach()]

    def isValidHTTPResponse(self, response):
        """Verify input response status is OK and content type is html."""
        return response.status_int == 200 and response.content_type == 'text/html'

    def HTTPResponseContains(self, response, target_object):
        """Verify inputted response contains inputted object."""
        return str(target_object) in response.normal_body
    
    def activateDatastoreTestbed(self):
        activeTestbed = testbed.Testbed()
        activeTestbed.activate()
        activeTestbed.init_datastore_v3_stub()
        activeTestbed.init_memcache_stub()
        return activeTestbed

    def tearDown(self):
        if hasattr(self, 'testbed'):
            self.testbed.deactivate()

class LoadMainPageTestCase(AbstractWebtestBaseClass):
    def runTest(self):
        response = self.testapp.get('/')
        self.isValidHTTPResponse(response)


class DisplayObjectOnWebTestCase(AbstractWebtestBaseClass):
    """Test /view/(.*)."""
    def setUp(self):
        super(DisplayObjectOnWebTestCase, self).setUp()
        self.testbed = self.activateDatastoreTestbed()
        self.objectFactory = model.SampleObjectFactory()
        self.test_data_keys = self.putTestDataInNDB()

    def runTest(self):
        for key in self.test_data_keys:
            response = self.testapp.get('/view/' + key.urlsafe())
            self.assertTrue(self.isValidHTTPResponse(response))
            self.assertTrue(self.HTTPResponseContains(response, str(key.get())))


class ModifyDataFromWebTestCase(AbstractWebtestBaseClass):
    """Populate modify and submit HTML form, succesfully communicating with NDB at each end.
    Test /edit/(.*)
    
    """
    def setUp(self):
        super(ModifyDataFromWebTestCase, self).setUp()
        self.testbed = self.activateDatastoreTestbed()
        self.objectFactory = model.SampleObjectFactory()
        self.dataGenerator = model.RandomDataGenerator()
        self.test_data_keys = self.putTestDataInNDB()

    def runTest(self):
        for key in self.test_data_keys:
            getResponse = self.testapp.get('/edit/' + key.urlsafe())
            self.assertTrue(self.isValidHTTPResponse(getResponse))
            #self.assertTrue(self.HTTPResponseContains(getResponse, str(key.get())))
            form = getResponse.form
            self.assertEquals(form.action, '/edit/' + key.urlsafe())
            test_object = key.get()
            self.assertEquals(test_object.text, form['content'].value)
            self.assertIn(str(test_object.variables), form['variables'].value)
            self.assertEquals(test_object.linked_node, form['linked_node'].value)
            print('\nform contents: %s' % form['content'].value)
            form['content'].value = self.dataGenerator.randomlyModify(key.get())
            postResponse = form.submit()
            print('\npostResponse.normal_body: %s' % postResponse.normal_body)
            self.assertTrue(self.isValidHTTPResponse(postResponse))
            self.assertTrue(self.HTTPResponseContains(postResponse, str(key.get())))
            self.assertNotEquals(getResponse.normal_body, postResponse.normal_body)
            self.assertTrue(self.HTTPResponseContains(postRespose, str(key.get())))


class CreateDataFromWebTestCase(unittest.TestCase):
    @unittest.skip("Stub")
    def runTest(self):
        self.assertEquals(0, 1)

class ExportDataFromWebToXMLTestCase(unittest.TestCase):
    @unittest.skip("Stub")
    def runTest(self):
        self.assertEquals(0, 1)

class ImportDataFromXMLToWebTestCase(unittest.TestCase):
    @unittest.skip("Stub")
    def runTest(self):
        self.assertEquals(0, 1)


if __name__ == "__main__":
    unittest.main()

