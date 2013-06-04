#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys
import unittest

import webtest
from google.appengine.ext import testbed

import application as app
import model


sys.path.insert(0, '.')  # add parent folder to path list


class WebtestTestCaseTemplate(unittest.TestCase):
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

class LoadMainPageTestCase(WebtestTestCaseTemplate):
    def runTest(self):
        response = self.testapp.get('/')
        self.isValidHTTPResponse(response)


class DisplayObjectOnWebTestCase(WebtestTestCaseTemplate):
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
            self.assertTrue(self.HTTPResponseContains(response,
                                                      str(key.get())))


class ModifyDataFromWebTestCase(WebtestTestCaseTemplate):
    """Populate modify and submit HTML form, succesfully communicating with NDB at each end.
    Test /edit/(.*)
    
    """
    def setUp(self):
        super(ModifyDataFromWebTestCase, self).setUp()
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.objectFactory = model.SampleObjectFactory()
        self.dataGenerator = model.RandomDataGenerator()
        self.test_data_keys = self.putTestDataInNDB()

    def runTest(self):
        for key in self.test_data_keys:
            getResponse = self.testapp.get('/edit/' + key.urlsafe())
            self.assertTrue(self.isValidHTTPResponse(getResponse))
            self.assertTrue(self.HTTPResponseContains(getResponse, str(key.get())))
            form = getResponse.form
            self.assertEquals(form.action(), '/edit/' + key.urlsafe()) 
            form['textarea'].value = model.randomlyModify(key.get())
            postResponse = form.submit()
            self.assertTrue(self.isValidHTTPResponse(postResponse))
            self.assertTrue(self.HTTPResponseContains(postResponse, str(key.get())))
            self.assertNotEquals(getResponse.normal_body, postResponse.normal_body)
            self.assertTrue(self.HTTPResponseContains(postRespose, str(key.get())))


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

