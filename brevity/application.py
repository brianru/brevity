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
	return self.generator #does this have to be a yield statement?
    def visit_document(self, document): #does not return generator directly per PEP 380
	self.generator = doc_gen(document)
    def visit_node(self, node):
	self.generator =  node_gen(node)
    def visit_socket(self, socket):
        self.generator = sock_gen(socket)
    
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
	if socket.linked_node: #refactor to see if there is NO linked node, else pass
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
        self.raw_text.append(socket.text)
	#add dictionary components only if names are not already there
    def build_node(self, node):
	pass
    def build_document(self, document):
	variables = document.variables

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

    def export(self, component):
	constructor = ConstructionDirectorVisitor()
	raw_text, variables = constructor.construct(component)
	print raw_text
	print variables
	
class Reader(object):
    """Implement STRATEGY pattern to enable reading different filetypes."""
    def read_from_xml(self, xml_file):
        """Imports specified xml document.
        Supply xml document as a filepath string.
        
        """
        self.xml = etree.parse(xml_file)
        self.root = self.xml.getroot()
        if root.attrib['name'] == 'document':
            return self.doc_factory(root)
        elif root.attib['name'] == 'node':
            return self.node_factory(root)
        elif root.attrib['name'] == 'socket':
            return self.socket_factory(root)
        else:
            raise 
        
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
        return nodename
    def socket_factory(self, socket):
        #create socket using name specified in socket.attrib['name'] ('socketname')
        for x in socket.children:
            a = node_factory(x)
	    socketname.linked_node = a #refactor to use link_node method, raise exception if incompatible
        return socketname

