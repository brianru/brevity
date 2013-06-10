#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
import inspect
import sys
import unittest

from google.appengine.ext import ndb, db, testbed

import model


sys.path.insert(0, '.')  # add parent folder to path list


def activate_datastore_testbed():
    active_testbed = testbed.Testbed()
    active_testbed.activate()
    active_testbed.init_datastore_v3_stub()
    active_testbed.init_memcache_stub()
    return active_testbed


class CompleteAndConsistentDataModelTestCase(unittest.TestCase):
    """Verify data model ensures data is well-formed.
    (i.e. consistent and complete)
    1) Assign sample object contents to local variables.
    2) Instantiate component instance with sample object contents.
    3) Assert contents of component instance equals sample object contents.
    4) Validate obja == objb iff obja.contents == objb.contents
    5) Test content type restrictions raise expected exceptions.
    """
    def setUp(self):
        self.testbed = activate_datastore_testbed()
        self.object_factory = model.SampleObjectFactory()

    def runTest(self):
        self.test_socket()
        self.test_node()
        self.test_document()
        self.test_amendment()
        self.test_agreement()

    def test_socket(self):
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
        ####### TEST LINKED NODES #######

    def test_node(self):
        node_variable_keys = []
        test_node = self.object_factory.random_node()
        for socket in test_node.sockets:
            node_variable_keys.extend(socket.get().variables.keys())
        self.assertEquals(sorted(node_variable_keys), sorted(list(set(node_variable_keys))))
        node_sockets = sorted([x for x in test_node.sockets])
        self.assertEquals(node_sockets, sorted(list(set(node_sockets))))
        self.assertRaises(db.BadValueError, lambda: model.Node(sockets=0))
        self.assertRaises(db.BadValueError,
                          lambda: model.Node(sockets=[self.object_factory.random_node().put()]))
    
    def test_document(self):
        document_variable_keys = []
        sample_document = self.object_factory.random_document()
        for node in sample_document.nodes:
            for socket in node.get().sockets:
                document_variable_keys.extend(socket.get().variables.keys())
        self.assertEquals(sorted(document_variable_keys),
                          sorted(list(set(document_variable_keys))))
        document_nodes = sorted([x for x in sample_document.nodes])
        self.assertEquals(document_nodes, sorted(list(set(document_nodes))))
        self.assertRaises(db.BadValueError, lambda: model.Document(nodes=0))
        self.assertRaises(db.BadValueError, lambda: model.Document(nodes=self.object_factory.random_socket().put()))
        self.assertRaises(db.BadValueError, lambda: model.Document(variables=0))

    @unittest.expectedFailure
    def test_amendment(self):
        self.assertEquals(0, 1)
    
    @unittest.expectedFailure
    def test_agreement(self):
        self.assertEquals(0, 1)

    def tearDown(self):
        self.testbed.deactivate()


class RandomDataGeneratorTestCase(unittest.TestCase):
    """Verify helper methods create valid test data.
    Other methods are factory methods.
    Factory methods should be moved to a SampleData factory class in production code.
    
    """
    def setUp(self):
        self.gen_data = model.RandomDataGenerator()
        self.SAMPLE_SIZE = 3
    
    def runTest(self):
        self.assertEquals(len(self.gen_data.random_lines_of_text(self.SAMPLE_SIZE)),
                          self.SAMPLE_SIZE)
        test_dict_keys = self.gen_data.random_dict_keys(self.SAMPLE_SIZE)
        self.assertEquals(len(test_dict_keys), self.SAMPLE_SIZE)
        self.assertEquals(len(self.gen_data.random_dict(self.SAMPLE_SIZE)),
                          self.SAMPLE_SIZE)


class SampleObjectFactoryTestCase(unittest.TestCase):
    """Ensure this class does not overlap with ConsistentAndCompleteDataModelTestCase.

    """
    def setUp(self):
        self.testbed = activate_datastore_testbed()
        self.object_factory = model.SampleObjectFactory()
        self.gen_data = model.RandomDataGenerator()
        self.test_data_set = self.object_factory.random_instance_of_each()

    @unittest.expectedFailure
    def runTest(self):
        for test_item in self.test_data_set:
            test_item_with_variations = self.object_factory.variations_of(test_item)
            test_item_with_variations.append(test_item)
            # TODO verify contents of test_item_with_variations.append(testItem) are unique
            self.assertEquals(len(test_item_with_variations), len(test_item._values)+1)
        data_model_types = []
        for item in dir(model):
            item_class = eval('model.' + item)
            if inspect.isclass(item_class) and issubclass(item_class, ndb.Model):
                data_model_types.append(item_class)
        types_from_factory = [instance.__class__
                                          for instance
                                          in self.object_factory.random_instance_of_each()]
        self.assertEquals(sorted(data_model_types), sorted(types_from_factory))

    def tearDown(self):
        self.testbed.deactivate()


class CRUDInNDBTestCase(unittest.TestCase):
    """Create test data.
    Instantiate test object with test data.
    Save test objects to database, maintaining keys.
    For each key, access objects and compare objects' values to test data.
    Add attribute. Confirm.
    Delete attribute. Confirm.

    """
    def setUp(self):
        self.testbed = activate_datastore_testbed()
        self.object_factory = model.SampleObjectFactory()

    def runTest(self):
        test_data = self.object_factory.random_instance_of_each()
        test_data_keys = [test_item.put() for test_item in test_data]
        # Create // assert keys are returned
        self.assertEquals(len(test_data), len(test_data_keys))
        for test_item in test_data_keys:
            self.assertIsInstance(test_item, ndb.Key)
        # Read // assert keys.get() equals test data items
        self.assertEquals(test_data,
                          [test_item.get() for test_item in test_data_keys])
        # Update // update one property and .put(), assert keys match
        for test_item in test_data:
            self.object_factory.randomly_modify(test_item)
            self.assertIsInstance(test_item.put(), ndb.Key)
        # Delete // delete and assert keys.get() fails
        for test_item in test_data_keys:
            test_item.delete()
            self.assertIsNone(test_item.get())

    def tearDown(self):
        self.testbed.deactivate()


if __name__ == "__main__":
    unittest.main()
