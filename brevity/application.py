"""Brevity 0.2"""

import re, os, unittest, pdb, xml.etree.ElementTree as etree, tests

##### DATA MODEL #####

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
	
	
##### BUSINESS LOGIC #####

class Visitor(object):
    """Visitor pattern is used when actions differ by component type and the component type is not always known."""
    def visit_socket(self, socket):
	pass
    def visit_node(self, node):
	pass
    def visit_document(self, document):
	pass

class TraversalVisitor(Visitor):
    """Lets clients iterate over data structure without knowing how the data structure is constructed."""
    def get_generator(self, component):
        component.accept(self)
	return self.generator
    def visit_document(self, document): #cannot return generator directly until later version of python: see PEP 380
	self.generator = doc_gen(document)
    def visit_node(self, node):
	self.generator = node_gen(node)
    def visit_socket(self, socket):
        self.generator = sock_gen(socket)
    
    ## GENERATORS ##
def doc_gen(doc):
    yield doc
    for x in doc.nodes:
	for y in node_gen(x):
	    yield y
def node_gen(node):
    yield node
    for y in node.sockets:
	for z in sock_gen(y):
	    yield z
def sock_gen(socket):
    yield socket
    if socket.linked_node is not None:
	for x in node_gen(socket.linked_node):
            yield x

class ConstructionDirectorVisitor(Visitor):
    """Directs construction of any document component. Visits components to route proper actions.
    
    """
    def construct(self, component):
	"""Return cumulative active text and variables of component incl. all sub-components."""
	self.builder = ConstructionBuilder()
	t = TraversalVisitor()
	gen = t.get_generator(component)
	for x in gen:
	    x.accept(self)
        return self.builder.raw_text, self.builder.variables
    def visit_socket(self, socket):
	if socket.linked_node is not None:
	    pass
	else:
            self.builder.build_socket(socket)
    def visit_node(self, node):
	pass
    def visit_document(self, document):
	self.builder.build_document(document)

class Builder(object):
    """Allows client separation of product creation logic from product input logic."""
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
        self.raw_text += socket.text
	for x in socket.variables:
	    if x not in self.variables:
		self.variables.update({x: socket.variables[x]})
    def build_node(self, node):
	pass
    def build_document(self, document):
	self.variables = document.variables

class Compiler(object):
    """Constructs component structure then inserts variable values into text."""
    def compile(self, component):
	constructor = ConstructionDirectorVisitor()
	raw_text, variables = constructor.construct(component)
	#Revisit regex
	compiled_text = re.sub(r'A{(\w.*?)}', variables["\1"], raw_text)

class Writer(Visitor):
    """Output raw object with variable placeholders and values.
    Use STRATEGY pattern to for different document formats.

    """
    def write_to_txt():
	pass
    def write_to_html():
	pass
    def write_to_pdf():
	pass
    def write_to_tex():
	pass

class Reader(object):
    def read_from_xml(self, xml_file):
        """Imports specified xml document.
        Supply xml document as a filepath string.
        
        """
        self.xml = etree.parse(xml_file)
        self.root = self.xml.getroot()
        #is there any way to implement a Visitor class based on the element attributes?
        #maybe something I can subclass? or some weird hack of dunder methods?
	if root.attrib['name'] == 'document':
            return self.doc_factory(root)
        elif root.attib['name'] == 'node':
            return self.node_factory(root)
        elif root.attrib['name'] == 'socket':
            return self.socket_factory(root)
        else:
	    raise #a more specific exception than this
        
    def doc_factory(self, doc):
        #create doc using name specified in doc.attrib['name'] ('docname')
        for x in doc.children:
            a = node_factory(x)
            docname.nodes.extend(a)
        return docdname
    def node_factory(self, node):
        #create node using name specified in node.attrib['name'] ('nodename')
        for x in node.children:
            a = socket_factory(x)
            nodename.sockets.extend(a)
    def socket_factory(self, socket):
        #create socket using name specified in socket.attrib['name'] ('socketname')
        for x in socket.children:
            a = node_factory(x)
	    socketname.linked_node = a #refactor to use link_node method, raise exception if incompatible
        return socketname

class WriterDirectorVisitor(Visitor):
    def write_to_xml(self, component):
        t = TraversalVisitor()
	gen = t.get_generator(component)
	self.b = WriterBuilder()
	for x in gen:
	    x.accept(self)
	xml_tree = etree.ElementTree(b.root)
	filename = 'writer_director_output.xml'
	xml_tree.write(filename)
	return xml_tree, filename
    def visit_document(self, document):
	self.b.build_document(document)
    def visit_node(self, node):
	self.b.build_node(node)
    def visit_socket(self, socket):
	self.b.build_socket(socket)

class WriterBuilder(Builder):
    """Given input components in top-down left-right order, build corresponding xml tree.
    Refactor out anchor stack maintenance lines? 
    
    """
    def __init__(self):
        self.stack = []
	#counters used to create unique component names in xml
	self.doc_counter = 0
	self.node_counter = 0
	self.socket_counter = 0
    def build_document(self, document):
	"""Build root element."""
	self.stack.append(document)
        self.doc_counter += 1
        a = dict()
	a.extend('name': 'document' + str(self.doc_counter)})
	a.update(document.variables)
        self.root = etree.Element('document', a) #superstructure creates root element. must be accessible to other instance methods.
    def build_node(self, node):
	"""Build node element and add as child to appropriate anchor according to the anchor stack."""
	self.stack.append(node)
        self.node_counter += 1
	a = dict()
	a.extend({'name': 'node' + str(self.node_counter)})
	if type(self.stack[-1:]) == Socket: #If there's a socket above, this node must be linked to a socket.
            anchor_element = self.stack.pop()
        else: #Otherwise, we're iterating through nodes linked to a document object. Find that document object.
	    doc_stack = [i for i in self.stack if type(i) == Document]
	    anchor_element = doc_stack[-1:] #highest document
	    while type(self.stack[-1:]) == Node:
		self.stack.pop()
        etree.SubElement(anchor_element, 'node', a)
    def build_socket(self, socket):
	"""Build socket element and add as child to anchor node."""
        self.socker_counter += 1
	if socket.linked_node is not None:
            self.stack.append(socket)
	a = dict()
	a.extend({'name': 'socket' + str(self.socket_counter)})
	a.update({'text': socket.text})
	a.update(socket.variables)
	node_stack = [i for i in self.stack if type(i) == Node] #If iterating through socket list, must remove that noise to find nearest anchor node.
	anchor_node = node_stack[-1:] #highest node
	etree.SubElement(anchor_node, 'socket', a)
