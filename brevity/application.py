"""Brevity 0.2

Tool for... 
- designing contract models,
- drafting contract instances,
- amending existing contracts, and, 
- querying coontract libraries.

Provides a proprietary data structure that promotes internal consistency of documents and clause interoperability across contracts of varying purposes.
Data structure is round-trip convertible into XML and supports plain text, markdown, and LaTeX formatting.
"""

import re, os, unittest, pdb, xml.etree.ElementTree as etree, tests

##### DATA MODEL #####

class Socket(object):
    """Socket is the lowest level component in the data structure. It is the only component to contain document text. 
    Documents can be enhanced by extending a socket with an entire Node (see link_node).
    
    Attributes:
        1) text: uncompiled, unformatted text with formatting tags and variable placeholders (as applicable)
        2) variables: dictionary of variables. Dictionary keys should all be represented in variable placeholders in text (though variable placeholders may refer to keys stored elsewhere in the document).
	3) linked_node: Node object which extends this socket. Any linked node must be compatible with this socket, i.e., it must contain a superset of variable keys. This attribute should never be modified directly. Please use the link_node method instead (it ensures compatibility).

    """
    def __init__(self, text, variables = dict(), linked_node = None):
	self.text = text
	self.variables = variables
        self.linked_node = linked_node
    def __str__(self):
        return 'Component type: %s /nText: %s /nDefault variables: %s /nLinked node? %s'\
	        % (type(self), self.text, self.variables, self.linked_node)
    def accept(self, visitor):
        visitor.visit_socket(self)
    def link_node(self, new_node):
	"""Attempts to update the linked node by first checking node<->socket compatibility (node must contain a superset of variable keys).
        Returns True if update is successful.
	Returns False is update is unsuccessful.
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
    """Node is the intermediary component in the data structure -- it provides constraints. 
    We think about the node as specifying bullets in an outline. Specifying the bullets defines how the content of the document should be organized, and thus, how it may be extended in the future (see linked_node attribute in Socket class).
    
    Attributes:
	1) sockets: list of sockets
    
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
    """Document is the top level component in the data structure -- it is generally the only visible component when interacting with document instances.
    
    Attributes:
        1) nodes: list of nodes
	2) variables: dictionary of variables. Supersedes variable values found in underlying sockets (document-> instance variable values; socket->default variable values).
    """
    nodes = []
    def __init__(self, nodes, variables = dict()):
	self.nodes = nodes
	self.variables = variables
    #def __str__(self):
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
	Arguments: XML file path as a string
        
        """
        self.xml = etree.parse(xml_file)
        self.root = self.xml.getroot()
	#Route flow to proper factory method
        #is there any way to implement a Visitor class based on the element attributes?
        #maybe something I can subclass? or some weird hack of dunder methods?
	if self.root.tag == 'document':
            return self.doc_factory(self.root)
        elif self.root.tag == 'node':
            return self.node_factory(self.root)
        elif self.root.tag == 'socket':
            return self.socket_factory(self.root)
        else:
	    raise #a more specific exception than this
    """Component factory methods recursively generate the document object tree.
    Result accessible via 'root' instance variable.

    """
    def doc_factory(self, xml_document):
        document_children = []
	for child in xml_document.children:
	    document_children.extend(node_factory(self, child))
	return Document(document_children, xml_document.attrib['variables'])
    def node_factory(self, xml_node):
	node_children = []
	for child in xml_node.children:
	    node_children.extend(socket_factory(self, child))
        return Node(node_children)
    def socket_factory(self, xml_socket):
	if xml_socket.children is not None:
	    return Socket(xml_socket.contents,\
			  xml_socket.attrib['variables'],\
			  node_factory(self, xml_socket.children))
	else:
	    return Socket(xml_socket.contents,\
			  xml_socket.attrib['variables'],\
			  None)

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
        self.parent_stack = []
    def build_document(self, document):
	#stack should be empty if we build_document is called (document is always top of the stack)
	if self.parent_stack:
	    raise #a more informative exception than this
        self.root = etree.Element('document', document.variables)
	self.parent_stack.append(self.root)
    def build_node(self, node):
	"""Build node element and add as child to appropriate anchor according to the anchor stack."""
	while True:
	    if not self.parent_stack:
		raise #XML writing requires a document object at the root (so something should be there!)
	    elif self.parent_stack[-1].tag == 'socket':
		parent = self.parent_stack.pop()
		break
	    elif self.parent_stack[-1].tag == 'node':
		self.parent_stack.pop()
		continue
	    elif self.parent_stack[-1].tag == 'document':
		parent = self.parent_stack.pop()
		break
	self.parent_stack.append(etree.SubElement(parent, 'node', node.variables))
    def build_socket(self, socket):
	"""Build socket element and add as child to anchor node."""
	while True:
	    if not self.parent_stack or\
               self.parent_stack[-1].tag == 'document':
	        raise #a more informative exception than this
	    elif self.parent_stack[-1].tag == 'node':
	        parent = self.parent_stack.pop()
		break
	    elif self.parent_stack[-1].tag == 'socket':
		self.parent_stack.pop()
	a = etree.SubElement(parent, 'socket', socket.variables)
	if socket.linked_node is not None:
	    self.parent_stack.append(a)
