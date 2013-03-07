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
    def __init__(self, text, variables = dict(), linked_node = None):
	self.text = text
	self.variables = variables
        self.linked_node = linked_node

    def __str__(self)
        return 'COmponent type: %s \n
		Text: %s \n
		Default variables: %s \n
		Linked node? %s \n' % (type(self), self.text, self.variables, if(linked_node))

    def linkNode(self, new_node):
	"""Attempts to update the linked node.
	Does not raise an exception if this is replacing an existing linked node.
	Raises exception if the node is incompatible.

	"""	    
	node_vars = []
	for x in new_node.sockets:
	    node_vars.append(x.variables.keys())
	if self.variables.issubset(node_vars):
	    linked_node = new_node
	    return True
        return False

class node(object):
    """Intermediary structure. Provides constraints.
    Contains:
        1) Sockets
    
    """
    def __init__(self, sockets):
	self.sockets = sockets
	#raise exception if 1) sockets does not contain only sockets or 2) sockets is empty

    def __str__(self):
	return 'Component type: %s \n
	        Number of sockets: %d' % (type(self), len(sockets))
    
class document(object):
    """Top structure. Contains instance variables. Separates document components from particular document instance.
    Contains:
        1) Nodes
	2) Instance variables
	3) Cached array of full variable set
	4) Cached compiled document.
    
    """
    def __init__(self, nodes, variables = dict()):
	self.nodes = nodes
	self.variables = variables

    cached_compile = None
    cached_vars = None

    def stale_cache(self, fresh_compile = None, fresh_vars = None):
	if fresh_compile: cached_compile = fresh_compile
	if fresh_vars: cached_vars = fresh_vars

##### CONTROLLER #####

class docIterator(object):
    """Iterate through document in most efficient manner. """

class compiler(object):
    """Use docIterator to aggregate active objects and output formatted object.
    STRATEGY for different raw formats (txt, md, tex)
    
    """

class printer(object):
    """Output raw object with variable placeholders and values.

    """

class new(object):
    """CLI to create objects.

    """

class br_controller(object):
    """Primary controller class.

    """

class list(object):
    """Display cached (working) objects.

    """ 

class us_constitution_static_test(unittest.TestCase):
    """Import US constitution (cumulative of all amendments) from a prepared .brvty file.
    Build .tex file.
    Compile into .txt -- then compare to existing .txt file.
    Compile into .pdf.
    
    """

class us_constitution_dynamic_test(unittest.TestCase):
    """Import US constitution and each amendment independently from a set of prepared .brvty files.
    Build .tex file for each 50 years.
    Compile each into .txt and compare to existing .txt file.
    Compile into .pdf at each point.
    
    """

class core_test(unittest.TestCase):
    """Test core functionality excluding interface """
    preamble_clause = socket('This is a purchase order for the monthly delivery of socks.',[frequency: monthly])) #insert updated variable syntax
    print preamble_clause
    preamble = node(preamble_clause)
    print preamble


    socks = document()
    print socks


if __name__ == "__main__":
    unititest.main()
