"""Brevity 0.2

Usage: 
    brevity -h | --help
    brevity new socket <text> <variables> <linkedNode>
    brevity new node <sockets>
    brevity new document <nodes> <instanceVariables>
    brevity new
    brevity -ls | --list

Options:
    -h | --help Show the help docstring.
    -ls | --list Print cached (working) object list.

"""

import re, os

##### MODEL #####

class socket(object):
    """Lowest level structure.
    Contains:
        1) Uncompiled text (with variable placeholders)
	2) Variable defaults
	3) Linked Node
    
    """
    def __init__(self, text, variables = dict(), linkedNode = None):
	self.text = text
	self.variables = variables
        self.linkNode(linkNode)

    def __str__(self)
        pass #Object type \n Variables \n Uncompiled text

    def linkNode(self, newNode):
	#if node's sockets contain vars in this socket, OK, otherwise raise exception
	pass

class node(object):
    """Intermediary structure. Provides constraints.
    Contains:
        1) Sockets
    
    """
    def __init__(self, sockets):
	self.sockets = sockets
	#raise exception if 1) sockets does not contain only sockets or 2) sockets is empty

    def __str__(self):
	pass #Object type \n Sockets \n Linked Nodes \n ...
    
class document(object):
    """Top structure. Contains instance variables. Separates document components from particular document instance.
    Contains:
        1) Nodes
	2) Instance variables
    """

##### VIEW #####
class compiler(object):
    """Output formatted object.

    """

class printer(object):
    """Output raw object with variable placeholders and values.

    """

##### CONTROLLER #####

class new(object):
    """CLI to create objects.

    """

class br_controller(object):
    """Primary controller class.

    """

class list(object):
    """Display cached (working) objects.

    """

if __name__ == 
