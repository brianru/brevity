#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
"""Brevity data model."""
import copy
import random
import sys

from google.appengine.ext import ndb, db

# Validators
def isDictionary(proposedObject, objectValue):
    """Check if objectValue is of type dict."""
    if isinstance(objectValue, dict):
        return None
    else:
        raise db.BadValueError

def isSocket(proposedObject, objectValue):
    """Check if objectValue is a key for type Socket."""
    return isComponentType(proposedObject, objectValue, 'Socket')

def isNode(proposedObject, objectValue):
    """Check if objectValue is a key for type Node."""
    return isComponentType(proposedObject, objectValue, 'Node')

def isDocument(proposedObject, objectValue):
    return isComponentType(proposedObject, objectValue, 'Document')

def isComponentType(proposedObject, objectValue, componentType):
    if objectValue.kind() == componentType:
        return None
    else:
        raise db.BadValueError

def objectFromKey(key):
    """Get object instance from NDB using key."""
    return key.get()

def objectFromURLSafeKey(urlKey):
    """Get object instance from NDB using url safe key."""
    return objectFromKey(ndb.Key(urlsafe=urlKey))

# Data model
class Agreement(ndb.Model):
    documents = ndb.KeyProperty(repeated=True, validator=isDocument)
    meta_data = ndb.JsonProperty(validator=isDictionary)

class Document(ndb.Model):
    nodes = ndb.KeyProperty(repeated=True, validator=isNode)
    variables = ndb.JsonProperty(validator=isDictionary)

class Amendment(Document):
    old_obj = ndb.KeyProperty()
    new_obj = ndb.KeyProperty()

class Node(ndb.Model):
    sockets = ndb.KeyProperty(repeated=True, validator=isSocket)

class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty(validator=isDictionary)
    linked_node = ndb.StructuredProperty(Node)


# Test data generator
class RandomDataGenerator(object):
    def __init__(self):
        with open('test/mobydick.txt', 'r') as f:
            self.sample_text = f.readlines()
        with open('test/nounlist.txt', 'r') as f:
            self.noun_list = f.readlines()

    def randomLinesOfText(self, numberOfLines):
            return [random.choice(self.sample_text)
                    for x in xrange(0,numberOfLines)]

    def randomDictionary(self, size):
        return self.randomDictionaryFromKeys(self.randomVariableKeys(size))

    def randomVariableKeys(self, numberOfKeys):
        return [random.randint(0,sys.maxint) for x in xrange(0,numberOfKeys)]
    
    def randomDictionaryFromKeys(self, keys):
        return dict(zip(keys, [random.choice(self.noun_list) for i in keys])) 

    def randomlyModify(self, original_object):
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
        self.dataGenerator = RandomDataGenerator()
        self.SAMPLE_SIZE = 3
        # add randomlyModify methods to model.(Socket, Node, Document, Amendment, Agreement)
    
    def randomlyModify(self, original_object):
        target_attribute = original_object._values[original_object._values.keys()[0]]
        if isinstance(target_attribute, (str, dict, type(None))):
            return self.dataGenerator.randomlyModify(target_attribute)
        else:
            self.randomlyModify(target_attribute)
    
    def objectVariationsOf(self, original_object):
        """For each property in original_object,
        create a copy of original_object,
        randomlyModify attribute in copy
        
        """
        objectVariations = []
        for var in original_object._values:
            if isinstance(var, (str, dict, None)):
                objectCopy = copy.copy(original_object)
                objectCopy._values.__setitem__(str(var), self.dataGenerator.randomlyModify(var))
                objectVariations.append(objectCopy)
            else:
                self.objectVariationsOf(var)
        return objectVariations
    
    def randomSocket(self):
        return Socket(text=str(self.dataGenerator.randomLinesOfText(self.SAMPLE_SIZE)),
                         variables=self.dataGenerator.randomDictionary(self.SAMPLE_SIZE),
                         linked_node=None)

    def randomSocketFromKeys(self, keys):
        return Socket(text=str(self.dataGenerator.randomLinesOfText(self.SAMPLE_SIZE)),
                         variables=self.dataGenerator.randomDictionaryFromKeys(keys),
                         linked_node=None)

    def randomNode(self):
        return Node(sockets=[self.randomSocket().put() for x in xrange(0, self.SAMPLE_SIZE)])

    def randomDocument(self):
        return Document(nodes=[self.randomNode().put() for x in xrange(0, self.SAMPLE_SIZE)],
                        variables=self.dataGenerator.randomDictionary(self.SAMPLE_SIZE))

    def randomAmendment(self):
        pass

    def randomAgreement(self):
        pass

    def randomInstanceOfEach(self):
        return [self.randomSocket(),
                self.randomNode(),
                self.randomDocument()]
        #        self.randomAmendment(),
        #        self.randomAgreement()]

