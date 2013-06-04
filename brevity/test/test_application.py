#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import sys
import unittest

import webtest
from google.appengine.ext import testbed

import application as app
import model


sys.path.insert(0, '.')  # add parent folder to path list


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

