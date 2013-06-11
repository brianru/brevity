#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Brevity data model."""
import copy
import random
import sys

from google.appengine.ext import ndb, db
from functools import partial

# Validators
def _is_dictionary(proposed_object, object_values):
    """Check if object_values is of type dict."""
    if isinstance(object_values, dict):
        return None
    else:
        raise db.BadValueError


def _is_data_type(object_type, proposed_object, object_values):
    if object_values.kind() == object_type:
        return None
    else:
        raise db.BadValueError


def view_data_from(url_safe_key):
    return {
        'key': url_safe_key,
        'kind': str(type_from_urlsafe(url_safe_key)).lower(),
        'instance': instance_from_urlsafe(url_safe_key),
    }


def instance_from_urlsafe(key):
    """Get object instance from NDB using url safe key."""
    return ndb.Key(urlsafe=key).get()


def type_from_urlsafe(url_key):
    return ndb.Key(urlsafe=url_key).kind()


def _key_from(instance):
    return instance.put()


def urlsafekey_from(original_object):
    return _key_from(original_object).urlsafe()


# Data model
class Agreement(ndb.Model):
    documents = ndb.KeyProperty(repeated=True, validator=partial(_is_data_type, 'Document'))
    meta_data = ndb.JsonProperty(validator=_is_dictionary)


class Document(ndb.Model):
    nodes = ndb.KeyProperty(repeated=True, validator=partial(_is_data_type, 'Node'))
    variables = ndb.JsonProperty(validator=_is_dictionary)


class Amendment(Document):
    old_obj = ndb.KeyProperty()
    new_obj = ndb.KeyProperty()


class Node(ndb.Model):
    sockets = ndb.KeyProperty(repeated=True, validator=partial(_is_data_type, 'Socket'))


class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty(validator=_is_dictionary)
    linked_node = ndb.StructuredProperty(Node)


# Test data generator
class RandomDataGenerator(object):
    def __init__(self):
        with open('test/mobydick.txt', 'r') as f:
            self.sample_text = f.readlines()
        with open('test/nounlist.txt', 'r') as f:
            self.noun_list = f.readlines()

    def random_text(self):
        return str(self.random_lines_of_text(3))

    def random_lines_of_text(self, numberOfLines):
            return [random.choice(self.sample_text)
                    for x in xrange(0, numberOfLines)]

    def random_dict(self, size):
        return self.random_dict_from(self.random_dict_keys(size))

    def random_dict_keys(self, num_keys):
        return [random.randint(0, sys.maxint) for x in xrange(0, num_keys)]

    def random_dict_from(self, keys):
        return dict(zip(keys, [random.choice(self.noun_list) for i in keys]))

    def randomly_change(self, original_object):
        if original_object is None:
            return None
        elif isinstance(original_object, str):
            return original_object + '\nrandomModification'
        elif isinstance(original_object, dict):
            return original_object.update({'randomModification': 0})
        else:
            raise db.BadValueError


class SampleObjectFactory(object):
    """Define a language for this abstraction layer.
    Keys =
    Instance =
    Variable =

    """
    def __init__(self):
        self.gen_data = RandomDataGenerator()
        self.SAMPLE_SIZE = 3
        # add randomlyModify methods to model.(Socket, Node, ...)

    def _randomly_modify_socket(self, original_socket):
        original_socket.text = self.gen_data.random_text()
        return original_socket

    def _randomly_modify_node(self, original_node):
        original_node.sockets[0] = self.random_socket().put()

    def _randomly_modify_document(self, original_document):
        original_document.nodes[0] = self.random_node().put()

    def _randomly_modify_amendment(self, original_amendment):
        pass

    def _randomly_modify_agreement(self, original_agreement):
        pass

    # TODO refactor to remove massive switch block
    def randomly_modify(self, original_object):
        if isinstance(original_object, (str, dict, type(None))):
            return self.gen_data.randomly_change(original_object)
        elif isinstance(original_object, Socket):
            return self._randomly_modify_socket(original_object)
        elif isinstance(original_object, Node):
            return self._randomly_modify_node(original_object)
        elif isinstance(original_object, Document):
            return self._randomly_modify_document(original_object)
        elif isinstance(original_object, Amendment):
            return self._randomly_modify_amendment(original_object)
        elif isinstance(original_object, Agreement):
            return self._randomly_modify_agreement(original_object)
        else:
            raise db.BadValueError

    def variations_of(self, original_object):
        """For each property in original_object,
        create a copy of original_object,
        randomlyModify attribute in copy

        """
        object_varations = []
        for var in original_object._values:
            object_copy = copy.copy(original_object)
            object_copy._values.__setitem__(
                str(var),
                self.gen_data.randomly_change(var),
            )
            object_varations.append(object_copy)
        return object_varations

    def random_socket(self):
        return Socket(
            text=str(self.gen_data.random_lines_of_text(self.SAMPLE_SIZE)),
            variables=self.gen_data.random_dict(self.SAMPLE_SIZE),
            linked_node=None,
        )

    def random_socket_from(self, keys):
        return Socket(
            text=str(self.gen_data.random_lines_of_text(self.SAMPLE_SIZE)),
            variables=self.gen_data.random_dict_from(keys),
            linked_node=None,
        )

    def random_node(self):
        return Node(sockets=[self.random_socket().put()
                             for x
                             in xrange(0, self.SAMPLE_SIZE)])

    def random_document(self):
        return Document(
            nodes=[self.random_node().put()
                   for x
                   in xrange(0, self.SAMPLE_SIZE)],
            variables=self.gen_data.random_dict(self.SAMPLE_SIZE),
        )

    def random_amendment(self):
        pass

    def random_agreement(self):
        pass

    def random_instance_of_each(self):
        return [self.random_socket(),
                self.random_node(),
                self.random_document()]
        #        self.random_amendment(),
        #        self.random_agreement()]
