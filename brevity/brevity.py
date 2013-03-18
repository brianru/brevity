"""Brevity 0.2"""

import re, os, unittest, pdb

##### MODEL #####

class Socket(object):
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
    def link_node(self, new_node):
	"""Attempts to update the linked node.
	Does not raise an exception if this is replacing an existing linked node.
	Raises exception if the node is incompatible.

	"""	    
	node_vars = []
	for x in new_node.sockets:
	    node_vars.extend(x.variables.keys())
	#build separate method in socket to perform below comparison
	#if new_node >= self
	for y in self.variables.keys():
	    if y not in node_vars:
		return False
	self.linked_node = new_node
	return True

class Node(object):
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
    
class Document(object):
    """Top structure. Contains instance variables. Separates document components from particular document instance.
    Contains:
        1) Nodes
	2) Instance variables
    
    """
    nodes = []
    def __init__(self, nodes, variables = dict()):
	self.nodes = nodes
	self.variables = variables
    def accept(self, visitor):
	visitor.visit_document(self)

##### CONTROLLER #####

class Visitor(object):
    "Abstract class. Defines interface for visitor classes."""
    def visit_socket(self, socket):
	pass
    def visit_node(self, node):
	pass
    def visit_document(self, document):
	pass

#Visitor pattern not supported for generator functions until python 3.3.
#See PEP 382
#class TraversalVisitor(Visitor):
#    def get_generator(self, component):
#       return component.accept(self)
#    def visit_document(self, document):
#	return doc_gen(document)
#    def visit_node(self, node):
#	return node_gen(node)
#    def visit_socket(self, socket):
#       return sock_gen(socket)

## GENERATORS ##
def doc_gen(doc):
    yield doc
    for x in doc.nodes:
        yield node_gen(x)
def node_gen(node):
    yield node
    for y in node.sockets:
	yield sock_gen(y)
def sock_gen(socket):
    yield socket
    if socket.linked_node:
	yield node_gen(socket.linked_node)

class ConstructionDirectorVisitor(Visitor):
    """Directs construction of any document component. Visits components to route proper actions."""
    def __init__(self):
	"""Is there anything to do here?"""
	self.builder = ConstructionBuilder()
    def construct(self, component):
	"""Return cumulative active text and variables of component incl. all sub-components."""
	#reset constructor, builder and iterator
	self.iter = TraversalVisitor(component)
	component.accept(self)
        return self.builder.raw_text, self.builder.variables
    def visit_socket(self, socket):
	if socket.linked_node:
	    self.iter.next()
	else:
            self.builder.build_socket(socket)
    def visit_node(self, node):
	self.iter.next(node)
    def visit_document(self, document):
	self.builder.build_document(document)
	self.iter.next(document)

class Builder(object):
    "Abstract class. Defines interface for builder classes."""
    def __init__(self):
	pass
    def build_socket(self, socket):
	pass
    def build_node(self, node):
        pass
    def build_document(self, document):
	pass

class ConstructionBuilder(Builder):
    def __init__(self):
	"""Hide internal representation of document.
	Must suffice for all potential uses.
	
	"""
	self.raw_text = ''
	self.variables = dict()
    def build_socket(self, socket):
        self.raw_text.append(socket.text)
	#add dictionary components only if names are not already there
    def build_node(self, node):
	pass
    def build_document(self, document):
	variables = document.variables

class Compiler(object):
    """Constructs component structure then inserts variable values into text."""
    def __init__(self):
	"""Does anything need to be done here?"""
    def compile(self, component):
	constructor = ConstructionDirectorVisitor()
	raw_text, variables = constructor.construct(component)
	compiled_text = re.sub(r'A{\w.*?)}', variables["\1"], raw_text)

class Printer(Visitor):
    """Output raw object with variable placeholders and values.
    Use STRATEGY pattern to for different document formats.

    """
    def export(self, component):
	constructor = ConstructionDirectorVisitor()
	raw_text, variables = constructor.construct(component)
	print raw_text
	print variables

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
class Socket_Test(unittest.TestCase):
    """Try linking compatible and incompatible nodes. """
    def runTest(self):
    	socket1 = Socket('I like breakfast A{item1}', {'item1': 'tacos'})
    	socket2 = Socket('Especially with A{condiment}', {'condiment': 'salsa'})
    	socket3 = Socket('...AND A{extra}', {'extra': 'bacon'})
    	node1 = Node([socket1, socket2, socket3])
    	socket4 = Socket('I like lots of different kinds of A{meal} food.', {'meal': 'breakfast'})
	socket5 = Socket('Items suchs as A{item1}, A{item2}, A{item3} are among my favorites.', \
			 {'item1': 'tacos', 'item2': 'omelettes', 'item3':'leftover pizza'})
    	node2a = Node([socket4]) #incompatible with socket1
	node2b = Node([socket4, socket5]) #compatible with socket1: see 'item1'
	
	self.assertFalse(socket1.link_node(node2a))
	self.assertEqual(socket1.linked_node, None)
	self.assertTrue(socket1.link_node(node2b))
    	self.assertEqual(socket1.linked_node, node2b)

class Node_Test(unittest.TestCase):
    """Create a node.
    Determine how empty nodes should be handled.
    Ensure sockets are stored appropriately.

    """
    def runTest(self):
	socket1 = Socket('I like breakfast A{item1}', {'item1': 'tacos'})
    	socket2 = Socket('Especially with A{condiment}', {'condiment': 'salsa'})
    	socket3 = Socket('...AND A{extra}', {'extra': 'bacon'})
    	node1 = Node([socket1, socket2, socket3])
        
	self.assertRaises(TypeError, lambda: Node())
	self.assertEqual(node1.sockets, [socket1, socket2, socket3])

class Document_Test(unittest.TestCase):
    """Figure out the stale cache thing."""
    def runTest(self):
	socket1 = Socket('I like breakfast A{item1}.', {'item1': 'tacos'})
    	socket2 = Socket('Especially with A{condiment}...', {'condiment': 'salsa'})
    	socket3 = Socket('...AND A{extra}!', {'extra': 'bacon'})
    	node1 = Node([socket1, socket2, socket3])
	socket4 = Socket('I also like breakfast A{item2}.', {'item2': 'pizzas'})
        socket5 = Socket('The best breakfast A{item2} are at A{location1}.', {'location1': 'Pizza Hut'})
	node2 = Node([socket4, socket5])
	document1 = Document([node1, node2])

	self.assertRaises(TypeError, lambda: Document())
	self.assertEqual(document1.nodes, [node1, node2])

class Iterator_Test(unittest.TestCase):
    """Build multi-tier document.
    Iterate over full document as well as sub-structures.

    """
    def runTest(self):
	socket1 = Socket('I like breakfast A{food}', {'food': 'tacos'})
        socket2 = Socket('Especially with A{condiment}', {'condiment': 'salsa'})
        socket3 = Socket('...AND A{extra}', {'extra': 'bacon'})
        node1 = Node([socket1, socket2, socket3])
        counter = 0
	gen = node_gen(node1)
	for x in gen:
	    counter += 1
        self.assertEqual(counter, 4) #ensure iterator passes over every object in the substructure exactly once

class Visitor_Test(unittest.TestCase):
    """Create a visitor subclass and assert the following on every type of component object:
    1) Component has an accept() method
    2) Component's accept() method calls correct visit_???() method on the visitor

    """

class Constructor_Test(unittest.TestCase):
    """Construct a document."""

class Printer_Test(unittest.TestCase):
    """Print a variety of component structures."""

if __name__ == "__main__":
    unittest.main()
