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

import re, os, unittest

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

    def __str__(self):
        return 'Component type: %s /nText: %s /nDefault variables: %s /nLinked node? %s' % (type(self), self.text, self.variables, self.linked_node)
    def accept(self, visitor):
        visitor.visit_socket(self)
    def linkNode(self, new_node):
	"""Attempts to update the linked node.
	Does not raise an exception if this is replacing an existing linked node.
	Raises exception if the node is incompatible.

	"""	    
	node_vars = []
	for x in new_node.sockets:
	    node_vars.append(x.variables.keys())
	#build separate method in socket to perform below comparison
	#if new_node >= self
	if self.variables.issubset(node_vars): 
	    linked_node = new_node
	    return True
        return False

class node(object):
    """Intermediary structure. Provides constraints.
    Contains:
        1) Sockets
    
    """
    sockets = []
    def __init__(self, sockets):
	self.sockets = sockets
	#raise exception if 1) sockets does not contain only sockets or 2) sockets is empty
    def __str__(self):
	return 'Component type: %s /nNumber of sockets: %s' % (type(self), self.sockets)
    def accept(self, visitor):
	visitor.visit_node(self)
    
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

    def accept(self, visitor):
	visitor.visit_document(self)

    cached_compile = None
    cached_vars = None

    def stale_cache(self, fresh_compile = None, fresh_vars = None):
	if fresh_compile: cached_compile = fresh_compile
	if fresh_vars: cached_vars = fresh_vars

##### CONTROLLER #####

class docIterator(object):
    """Iterate through document in most efficient manner. """

class visitor(object):
    """Abstract class defines interface for visitor classes."""
    def visit_socket(self, socket):
	pass
    def visit_node(self, node):
	pass
    def visit_document(self, document):
	pass

class compiler(visitor):
    """Iterates through document structure, accumulating text and variables at each step. 
    Attributes: result_text, result_compiled_text, result_variables
    
    """
    def __init__(self):
        result_variables = dict()
        result_text = ''
	result_compiled_text = ''
    def visit_document(self, document):
	result_variables = document.variables
	for x in document.nodes:
	    x.accept(self)
    def visit_node(self, node):
	for y in node.sockets:
	    y.accept(self)
    def visit_socket(self, socket):
	if socket.linked_node:
            socket.linked_node.accept(self)
	else:
	    result_text.append('/n' + socket.text)
	    #this check should only be adding defaults not redefined in doc instance
	    #refactor document construction methods if otherwise
	    for j in socket.variables.iterkeys():
	        if j not in result_variables.keys():
		    result_variables.update(j, y.variables[j])
    def compile(self):
	result_compiled_text = re.sub(r'A{\w.*?)}',result_variables["\1"], result_text)

class printer(visitor):
    """Output raw object with variable placeholders and values.

    """
    def __init__(self):
        result_text = ''

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
    preamble_clause = socket('This is a purchase order for the A{frequency} delivery of socks.', {'frequency': 'monthly'})
    print preamble_clause
    preamble = node(preamble_clause)
    print preamble
    socks = document(preamble)
    print socks


if __name__ == "__main__":
    unittest.main()
