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
    documents = ndb.KeyProperty(repeated=True)
    meta_data = ndb.JsonProperty()
    # other meta data (status, dates and stuff)

class Document(ndb.Model):
    nodes = ndb.KeyProperty(repeated=True)
    variables = ndb.JsonProperty()

class Amendment(Document):
    old_obj = ndb.KeyProperty()
    new_obj = ndb.KeyProperty()

class Node(ndb.Model):
    sockets = ndb.KeyProperty(repeated=True)

class Socket(ndb.Model):
    text = ndb.StringProperty()
    variables = ndb.JsonProperty(validator=validateDictionary)
    linked_node = ndb.StructuredProperty(Node)

def objectFromKey(key):
    return key.get()

def objectFromURLSafeKey(urlKey):
    return objectFromKey(ndb.Key(urlsafe=urlKey))

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
    
    #FIXME I do not understand this code.
    def objectVariationsOf(self, original_object):
        """For each property in original_object,
        return a new object with that property modified.
        
        """
        print('original_object._values: %s' % (original_object._values))
#        print('dir(original_object._values[0]): %s' % (dir(original_object._values['linked_node'])))
        # i should not be looking at var but at var's value.
        # original_object._values is a dictionary of keys and values -- keys are the properties
        # i want to look at the type of the property's value
        return [copy.copy(original_object).\
                __setattr__(original_object._values[var], self.dataGenerator.randomlyModify(original_object._values[var]))\
                if isinstance(var, (str, dict))\
                else (self.objectVariationsOf(var))\
                for var in original_object._values]

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
        pass
    #   return Document(node=[self.randomNode() for x in xrange(0,self.SAMPLE_SIZE)])

    def randomAmendment(self):
        pass

    def randomAgreement(self):
        pass

    def randomInstanceOfEach(self):
        return [self.randomSocket(),
                self.randomNode()]
        #        self.randomDocument(),
        #        self.randomAmendment(),
        #        self.randomAgreement()]

