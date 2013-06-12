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
            if (isinstance(target_object._values[var], str) and
                    not self.response_contains_str(response, target_object._values[var])):
                return False
            elif (isinstance(target_object._values[var], dict) and
                    not self.response_contains_dict(response, target_object._values[var])):
                return False
            elif target_object._values[var] is None:
                pass
            #TODO what about linked_node, sockets, documents and such?
        return True

    def response_contains_str(self, response, string):
        return string.encode('ascii') in response

    def response_contains_dict(self, response, dictionary):
        for k in dictionary.keys():
            if k.encode('ascii') not in response:
                return False
        for v in dictionary.values():
            if v.encode('ascii') not in response:
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
    """Populate modify and submit HTML form,
    succesfully communicating with NDB at each end.
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
            self.assertTrue(self.response_contains(get_response, key.get()))
            form = get_response.form
            self.assertEquals(form.action, '/edit/' + key.urlsafe())
            test_object = key.get()
            self.assertTrue(self.response_contains(get_response, test_object))
            # FIXME code directly modifies the object, defeats the purpose.
            # only supposed to modify the contents of the for
            form.value = self.factory.randomly_modify(test_object)
            post_response = form.submit()
            self.assertTrue(False)  # FIXME changes not saving but tests PASS?!
            self.assertTrue(self.is_valid_response(post_response))
            self.assertTrue(self.response_contains(post_response, key.get()))
            self.assertNotEquals(get_response.normal_body,
                                 post_response.normal_body)


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

