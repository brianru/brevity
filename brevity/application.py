##### BUSINESS LOGIC #####

class Visitor(object):
    "Abstract class. Defines interface for visitor classes."""
    def visit_socket(self, socket):
	pass
    def visit_node(self, node):
	pass
    def visit_document(self, document):
	pass

#Visitor pattern not supported for generator functions until python 3.3.
#See PEP 380
### Client classes must select correct generator (must know the structure entry-point's type).
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
    """Directs construction of any document component. Visits components to route proper actions.
    
    Refactor-out iterator code. 
    Flow should be driven by a loop containing iter.next().accept(self). 
    Appropriate visit_??? methods then called and information routed to the builder class.
    
    """
    def __init__(self):
	"""Is there anything to do here?"""
	self.builder = ConstructionBuilder()
    def construct(self, component):
	"""Return cumulative active text and variables of component incl. all sub-components."""
	#iterate through component's substructure
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
	#Revisit regex
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
	
class XMLImporter(object):
    """Translates valid XML documents written in Brevity's DOM into a native brevity data structure. """
    def import_xml(self, xml_file):
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
            socketname.linked_node = a
        return socketname

