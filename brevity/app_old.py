"""Brevity 0.2

A tool for...
- designing contract models,
- drafting contract instances,
- amending existing contracts, and,
- querying coontract libraries.

Provides a proprietary data structure that promotes internal consistency of
documents and clause interoperability across contracts of varying purposes.
Data structure is round-trip convertible into XML while supporting plain text,
markdown, HTML and LaTeX formatting.

"""

# import pdb
import re
from lxml import etree


class Socket(object):
    """Socket is the lowest level component in the data structure.
    It is the only component to contain document text.
    Documents can be enhanced by extending a socket with an entire Node
    (see link_node).

    Attributes:
        1) text: uncompiled, unformatted text with formatting tags and variable placeholders (as applicable)
        2) variables: dictionary of variables. Dictionary keys should all be represented in variable placeholders in text (though variable placeholders may refer to keys stored elsewhere in the document).
        3) linked_node: Node object which extends this socket. Any linked node must be compatible with this socket, i.e., it must contain a superset of variable keys. This attribute should never be modified directly. Please use the link_node method instead (it ensures compatibility).

    """
    socket_counter = 0

    def __init__(self, text='', variables=dict(), link_this_node=None):
        self.text = text
        self.variables = variables
        if not self.link_node(link_this_node):
            raise ValueError
        self.oid = 's' + str(self.__class__.socket_counter)
        self.__class__.socket_counter += 1

    def __str__(self):
        return 'Component type: %s \nText: %s \nDefault variables: %s \nLinked node? %s'\
            % (type(self), self.text, self.variables, self.linked_node)

    def __eq__(self, other):  # does not consider formatting
        return self.text == other.text and\
            self.variables == other.variables and\
            self.linked_node == other.linked_node

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        visitor.visit_socket(self)

    def link_node(self, new_node):
        """Attempts to update the linked node by first checking node<->socket compatibility (node must contain a superset of variable keys).
        Returns True if update is successful.
        Returns False is update is unsuccessful.
        """
        if new_node is None:
            self.linked_node = None
            return True
        else:
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
    node_counter = 0

    def __init__(self, sockets):
        self.sockets = sockets
        #raise exception if 1) sockets does not contain only sockets or 2) sockets is empty
        self.oid = 'n' + str(self.__class__.node_counter)
        self.__class__.node_counter += 1

    def __str__(self):
        return 'Component type: %s \nNumber of sockets: %s' % (type(self), len(self.sockets))

    def __eq__(self, other):
        return self.sockets == other.sockets

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        visitor.visit_node(self)


class Document(object):
    """Document is the top level component in the data structure -- it is generally the only visible component when interacting with document instances.

    Attributes:
        1) nodes: list of nodes
        2) variables: dictionary of variables. Supersedes variable values found in underlying sockets (document->instance variable values; socket->default variable values).

    """
    document_counter = 0

    def __init__(self, nodes, variables=dict()):
        if len(nodes) == 0:
            raise ValueError
        else:
            self.nodes = nodes
        self.variables = variables
        self.oid = 'd' + str(self.__class__.document_counter)
        self.__class__.document_counter += 1

    def __str__(self):
        return 'Component type: %s \n'\
               'Number of nodes: %s \n'\
               'Dictionary: %s' %\
               (type(self),
               len(self.nodes),
               '\n'.join(self.variables))

    def __eq__(self, other):
        return self.nodes == other.nodes and self.variables == other.variables

    def __ne__(self, other):
        return not self == other

    def accept(self, visitor):
        visitor.visit_document(self)


class Amendment(Document):
    def __init__(self, nodes, old_node, new_node, variables=dict()):
        super(Amendment, self).__init__(nodes, variables)
        self.old_node = old_node
        self.new_node = new_node

    def __str__(self):
        # return ('Compnent type: %s\n'
        #         'Number of nodes: %s\n') % (type(self, ...))
        return 'Component type: %s \n'\
               'Number of nodes: %s \n'\
               'Node being deleted: %s \n'\
               'Node replacing deleted node: %s \n'\
               'Dictionary: %s' %\
               (type(self),
               len(self.nodes),
               self.old_node,
               self.new_node,
               '\n'.join(self.variables))

    def __eq__(self, other):
        return self.old_node == other.old_node and\
            self.new_node == other.new_node and\
            super(Document, self).__eq__(other)

    def accept(self, visitor):
        visitor.visit_amendment(self)


class Agreement(object):
    def __init__(self, documents):
        self.documents = documents

    def __str__(self):
        return 'Component type: %s \n'\
               'Number of documents %s \n' %\
               (type(self),
                len(self.documents))

    def __eq__(self, other):
        return self.documents == other.documents

    def __ne__(self, other):
        return not self == other

    def __getslice__(self, start, end):
        return self.documents[start:end]

    def __setslice__(self, start, end, value):
        self.documents[start:end] = value
        # confirm interface / implementation is consistent

    def __delslice__(self, start, end):
        del(self.documents[start:end])
        # confirm interface / implementation is consistent

    def _slice_from_date(self, start, end):
        pass

    def accept(self, visitor):
        visitor.visit_agreement(self)


class Visitor(object):
    """Visitor pattern is used when actions differ by component type and the component type is not reliably known by the requestor.

    """
    def visit_socket(self, socket):
        pass

    def visit_node(self, node):
        pass

    def visit_document(self, document):
        pass

    def visit_amendment(self, amendment):
        pass

    def visit_agreement(self, agreement):
        pass


class TraversalVisitor(Visitor):
    """TraversalVisitor is an interface for component generators.
    This lets you iterate over a data structure, from any starting component, without understanding the underlying composition.

    """
    def get_generator(self, component):
        component.accept(self)
        return self.generator

    # cannot return generator directly until later version of python
    # see PEP 380
    def visit_document(self, document):
        self.generator = _doc_gen(document)

    def visit_amendment(self, amendment):
        self.generator = _doc_gen(amendment)

    def visit_node(self, node):
        self.generator = _node_gen(node)

    def visit_socket(self, socket):
        self.generator = _sock_gen(socket)


## GENERATORS ##
# rename using underscores to indicate these are internal methods
def _agrmt_gen(agreement):
    yield agreement
    for doc in agreement.documents:
        for node in doc.nodes:
            for socket in _node_gen(node):
                yield socket


def _doc_gen(doc):
    yield doc
    for node in doc.nodes:
        for socket in _node_gen(node):
            yield socket


def _node_gen(node):
    yield node
    for socket in node.sockets:
        for item in _sock_gen(socket):
            yield item


def _sock_gen(socket):
    yield socket
    if socket.linked_node is not None:
        for socket in _node_gen(socket.linked_node):
            yield socket


class ConstructionDirectorVisitor(Visitor):
    """Directs construction (flattening) of any document component and its substructure. The client does not need to be aware of the component's type.

    """
    def construct(self, component):
        """Return complete active text and variables of component -- including all components in sub-structure."""
        self.builder = ConstructionBuilder()
        t = TraversalVisitor()
        gen = t.get_generator(component)
        for x in gen:
            x.accept(self)
        return self.builder.raw_text, self.builder.variables

    def visit_socket(self, socket):
        if socket.linked_node is None:
            self.builder.build_socket(socket)

    def visit_node(self, node):
        self.builder.build_node(node)  # should this be "pass"?

    def visit_document(self, document):
        self.builder.build_document(document)

    def visit_amendment(self, amendment):
        self.builder.build_amendment()

    def visit_agreement(self, agreement):
        self.builder.build_agreement()


class Builder(object):
    """Allows separation of product creation logic from product input logic."""
    def build_socket(self, socket):
        pass

    def build_node(self, node):
        pass

    def build_document(self, document):
        pass

    def build_amendment(self, amendment):
        pass

    def build_agreement(self, agreement):
        pass


class ConstructionBuilder(Builder):
    """Separate knowledge of internal representation of components from the client-facing (Director) class.

    """
    def __init__(self):
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

    def build_agreement(self, agreement):
        """Identify a master set of nodes then build from there."""


class Compiler(object):
    """Inserts variable values into text.
    Returns compiled text if successfully generated, returns False otherwise.
    Note:
    -- Does not construct (flatten) component data structure.
    -- Component should be self-contained (all variable placeholders present in text should be defined within the inputs).

    """
    def compile(self, text, variables):
        self.text = text
        self.variables = variables
        try:
            return re.sub(r'A{(\w.*?)}', self.repl, text)
        except KeyError as e:
            # rework as loop through each match,
            #aggregating errors for improved debugging
            print 'key is not defined in variable dictionary: '\
                  + e.message
            return False

    def repl(self, key):
        return self.variables[key.group(1)]


class Printer(object):
    """Interface to latex command line utilities.

    """
    def print_to_text(self, text):
        pass

    def print_to_html(self, text):
        pass

    def print_to_pdf(self, text):
        pass

    def print_to_md(self, text):
        pass

    def _print(self, text, outputformat):
        pass


class Importer(object):
    """Component factory methods recursively generate the document object tree.
    Result accessible via 'root' instance variable.

    """
    def import_from_xml(self, xml_file):
        """Imports specified xml document.
        Arguments: XML file path as a string

        """
        parser = etree.XMLParser(remove_blank_text=True)
        self.xml = etree.parse(xml_file, parser)
        self.root = self.xml.getroot()
        #Route flow to proper factory method
        #is there any way to implement a Visitor class based on the element attributes?
        #maybe something I can subclass? or some weird hack of dunder methods?
        if self.root.tag == 'document' or self.root.tag == 'amendment':
            return self.doc_factory(self.root)
        elif self.root.tag == 'node':
            return self.node_factory(self.root)
        elif self.root.tag == 'socket':
            return self.socket_factory(self.root)
        else:
            raise ValueError

    def doc_factory(self, xml_document):
        linked_nodes = []
        for node in xml_document:
            linked_nodes.append(self.node_factory(node))
        return Document(linked_nodes, xml_document.attrib)

    def node_factory(self, xml_node):
        linked_sockets = []
        for socket in xml_node:
            linked_sockets.append(self.socket_factory(socket))
        return Node(linked_sockets)

    def socket_factory(self, xml_socket):
        if len(xml_socket) > 0:
            return Socket(xml_socket.text,
                          xml_socket.attrib,
                          self.node_factory(xml_socket[0]))
        else:
            return Socket(xml_socket.text,
                          xml_socket.attrib,
                          None)


class ExporterDirector(Visitor):
    """Facilitates exporting components (complete data representation) to portable formats.
    All components exported via this class are can be round-tripped back into the application without any data loss.

    """
    def export_to_xml(self, component, path):
        t = TraversalVisitor()
        gen = t.get_generator(component)
        self.b = Exporter(next(gen))  # instantiate Exporter with first item from generator
        for x in gen:  # event loop
            x.accept(self)
        xml_tree = etree.ElementTree(self.b.root)
        xml_tree.write(path)
        return path

    def visit_agreement(self, agreement):
        self.b.build_agreement(agreement)

    def visit_document(self, document):
        self.b.build_document(document)

    def visit_amendment(self, amendment):
        self.b.build_document(amendment)

    def visit_node(self, node):
        self.b.build_node(node)

    def visit_socket(self, socket):
        self.b.build_socket(socket)


class Exporter(Builder):
    """Given input components in top-down left-right order, builds a corresponding xml tree.
    REFACTOR out anchor stack maintenance lines.
    Make above assumption (input order) explicit?

    """
    def __init__(self, component):
        # tag must be in lowercase?
        self.root = etree.Element(type(component), component.variables)
        self.parent_stack = ParentStackHandler(self.root)

    def build_agreement(self, agreement):
        raise ValueError

    def build_document(self, document):
        """1) get parent element
        2) create subelement with parent
        3) update stack with subelement

        """

    def build_amendment(self, amendment):
        self.build_document(amendment)

    def build_node(self, node):
        """Build node element and add as child to appropriate anchor according to the anchor stack."""
        # self.parent_stack.append(etree.SubElement(parent, 'node'))

    def build_socket(self, socket):
        """Build socket element and add as child to anchor node."""
        # a = etree.SubElement(parent, 'socket', socket.variables)
        # a.text = socket.text


class ParentStackHandler(Visitor):
    """Maintains a stack of components for clients when clients must know a component's parent object.
    This class only works when the ParentStackHandler is sent every element in the data structure.
    Implments Visitor pattern if client is unaware of element type. Client can also access update methods directly.
    2 sets of methods:
        1) find_parent: delete items at top until parent is found, return parent
        2) add_element: append parent to stack

    """
    def __init__(self, element):
        self.stack = [element]

    def update_with_agreement(self, agreement):
        """Replace stack with agreement."""
        if self.stack:
            raise ValueError
        self.stack = [agreement]

    def update_with_document(self, document):
        """Remove all intervening documents.

        """
        while self.stack[-1].tag != 'agreement':
            del(self.stack[-1])
        return self.stack[-1]

    def update_with_amendment(self, amendment):
        return self.update_with_document(amendment)

    def update_with_node(self, node):
        while True:
            if self.stack[-1].tag == 'document' or\
               self.stack[-1].tag == 'amendment':
                return self.stack[-1]
            elif self.stack[-1].tag == 'node':
                del(self.stack[-1])
            elif self.stack[-1].tag == 'socket':
                return self.stack.pop()
            else:
                raise ValueError

    def update_with_socket(self, socket):
        while self.stack[-1].tag != 'node':
            if self.stack[-1].tag == 'socket':
                del(self.stack[-1])
            else:
                raise ValueError
        return self.stack[-1]

    def visit_agreement(self, agreement):
        self.update_with_agreement(agreement)

    def visit_document(self, document):
        self.update_with_document(document)

    def visit_amendment(self, amendment):
        self.update_with_amendment(amendment)

    def visit_node(self, node):
        self.update_with_node(node)

    def visit_socket(self, socket):
        self.update_with_socket(socket)
