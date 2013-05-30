#!/usr/bin/env python
"""Brevity data model."""
import copy
import random
import sys

from google.appengine.ext import ndb, db


def validateDictionary(proposedObject, objectValue):
    if isinstance(objectValue, dict):
        return None
    else:
        raise db.BadValueError

class Agreement(ndb.Model):
    document = ndb.KeyProperty(repeated=True)
    meta_data = ndb.JsonProperty()
    # other meta data (status, dates and stuff)

class Document(ndb.Model):
    node = ndb.KeyProperty(repeated=True)
    variables = ndb.JsonProperty()

class Amendment(Document):
    old_obj = ndb.KeyProperty()
    new_obj = ndb.KeyProperty()

class Node(ndb.Model):
    socket = ndb.KeyProperty(repeated=True)

class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty(validator=validateDictionary)
    linked_node = ndb.StructuredProperty(Node)



def objectFromKey(key):
    return key.get()

def objectFromURLKey(urlKey):
    return objectFromKey(ndb.Key(urlsafe=urlKey))

class RandomDataGenerator(object):
    def __init__(self):
        with open('test/mobydick.txt', 'r') as f:
            self.sample_text = f.readlines()
        with open('test/nounlist.txt', 'r') as f:
            self.noun_list = f.readlines()

    def randomText(self, numberOfLines):
            return str([random.choice(self.sample_text)
                    for x in xrange(0,numberOfLines)])

    def randomDictionary(self, size):
        return self.randomDictionaryFromKeys(self.randomVariableKeys(size))

    def randomVariableKeys(self, numberOfKeys):
        return [random.randint(0,sys.maxint) for x in xrange(0,numberOfKeys)]
    
    def randomDictionaryFromKeys(self, keys):
        return dict(zip(keys, random.choice(self.noun_list))) 

    def randomlyModify(self, original_object):
        return 0

class SampleObjectFactory(object):
    """Define a language for this abstraction layer.
    Keys = 
    Instance = 
    Variable = 

    """
    def __init__(self):
        self.dataGenerator = RandomDataGenerator()
    
    def objectVariationsOf(self, original_object):
        """For each property in original_object,
        return a new object with that property modified.
        
        """
        return [copy.copy(original_object).__setattr__(var,
                                                       self.dataGenerator.randomlyModify(var))
                for var in original_object._values]

    def randomSocket(self):
        return Socket(text=self.dataGenerator.randomText(3),
                         variables=self.dataGenerator.randomDictionary(3),
                         linked_node=None)

    def randomSocketFromKeys(self, keys):
        return Socket(text=self.dataGenerator.randomText(3),
                         variables=self.dataGenerator.randomDictionaryFromKeys(keys),
                         linked_node=None)

    def randomNode(self):
        return Node(socket=[self.randomSocket().put() for x in xrange(0, 3)])

    def randomDocument(self):
        pass
    #   return Document(node=[self.randomNode() for x in xrange(0,3)])

    def randomAmendment(self):
        pass

    def randomAgreement(self):
        pass

    def randomInstanceOfEach(self):
        return [self.randomSocket()]
        #        self.randomNode(),
        #        self.randomDocument(),
        #        self.randomAmendment(),
        #        self.randomAgreement()]
