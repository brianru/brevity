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

    def put_test_data_in_ndb(self):
        return [item.put()
                for item
                in self.factory.random_instance_of_each()]

    def is_valid_response(self, response):
        """Verify input response status is OK and content type is html."""
        return (response.status_int == 200 and
                response.content_type == 'text/html')

    def response_contains(self, response, target_object):
        """Verify inputted response contains inputted object."""
        for var in target_object._values:
            if str(target_object._values[var]) not in response.normal_body:
                return False
        return True

    def activate_datastore_testbed(self):
        active_testbed = testbed.Testbed()
        active_testbed.activate()
        active_testbed.init_datastore_v3_stub()
        active_testbed.init_memcache_stub()
        return active_testbed

    def tearDown(self):
        if hasattr(self, 'testbed'):
            self.testbed.deactivate()


class LoadMainPageTestCase(AbstractWebtestBaseClass):
    def runTest(self):
        response = self.testapp.get('/')
        self.is_valid_response(response)


class DisplayObjectOnWebTestCase(AbstractWebtestBaseClass):
    """Test /view/(.*)."""
    def setUp(self):
        super(DisplayObjectOnWebTestCase, self).setUp()
        self.testbed = self.activate_datastore_testbed()
        self.factory = model.SampleObjectFactory()
        self.test_data_keys = self.put_test_data_in_ndb()

    def runTest(self):
        for key in self.test_data_keys:
            response = self.testapp.get('/view/' + key.urlsafe())
            self.assertTrue(self.is_valid_response(response))
            self.assertTrue(self.response_contains(response, key.get()))


class ModifyDataFromWebTestCase(AbstractWebtestBaseClass):
    """Populate modify and submit HTML form, succesfully communicating with NDB at each end.
    Test /edit/(.*)
    
    """
    def setUp(self):
        super(ModifyDataFromWebTestCase, self).setUp()
        self.testbed = self.activate_datastore_testbed()
        self.factory = model.SampleObjectFactory()
        self.gen_data = model.RandomDataGenerator()
        self.test_data_keys = self.put_test_data_in_ndb()

    def runTest(self):
        for key in self.test_data_keys:
            get_response = self.testapp.get('/edit/' + key.urlsafe())
            self.assertTrue(self.is_valid_response(get_response))
            #self.assertTrue(self.response_contains(get_response, str(key.get())))
            form = get_response.form
            self.assertEquals(form.action, '/edit/' + key.urlsafe())
            test_object = key.get()
            self.assertEquals(test_object.text, form['content'].value)
            self.assertIn(str(test_object.variables), form['variables'].value)
            #self.assertEquals(test_object.linked_node, form['linked_node'].value)
            #form['content'].value = self.gen_data.randomly_nodify(key.get())
            post_response = form.submit()
            self.assertTrue(self.is_valid_response(post_response))
            self.assertTrue(self.response_contains(post_response, str(key.get())))
            self.assertNotEquals(get_response.normal_body, post_response.normal_body)
            self.assertTrue(self.response_contains(post_response, str(key.get())))


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

