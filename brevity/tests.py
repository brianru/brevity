import re, os, pdb, unittest, xml.etree.ElementTree as etree
from application import *
###### UNIT TESTS ######

class us_constitution_static_test(unittest.TestCase):
    """Import US constitution from a prepared .xml file.
    Build .tex file and compare to original .tex file.
    Compile into .txt.
    Compile into .html.
    Compile into .pdf.
    
    """
    def runTest(self):
	testxml = etree.parse('samples/constitution.xml')
#	im = XMLImporter()
#	constitution = im.import_xml(testxml)

#	with open('constitution_test.xml', mode = 'w', encoding = 'utf-8') as result_xml:
#	    ex = XMLExporter()
#	    result_xml.write(ex.export_xml(constitution))
	self.assertEqual(etree.parse('samples/constitution.xml'), etree.parse('constitution_text.xml'))

	p = Printer()
	const_tex = p.print_to_tex(constitution, 'tex', 'tests/constitution_test.tex')
	self.assertEqual('samples/constitution.tex', const_tex)

	c = Compiler()
	compiled_constitution = c.compile(constitution)
	self.assertEqual(p.print_to_txt(compiled_consititution), 'samples/constitution.txt')
	self.assertEqual(p.print_to_html(compiled_constitution), 'samples/constitution.html')
	self.assertEqual(p.print_to_pdf(compiled_constitution), 'samples/constitution.pdf')

class us_constitution_dynamic_test(unittest.TestCase):
    """Import US constitution and each amendment independently from a set of prepared .brvty files.
    Build .tex file for each 50 year slice.
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
	t = TraversalVisitor()
	socket1 = Socket('I like breakfast A{item1}.', {'item1': 'tacos'})
    	socket2 = Socket('Especially with A{condiment}...', {'condiment': 'salsa'})
    	socket3 = Socket('...AND A{extra1}!', {'extra1': 'bacon'})
    	node1 = Node([socket1, socket2, socket3])
	socket4 = Socket('I also like breakfast A{item2}.', {'item2': 'pizzas'})
        socket5 = Socket('The best breakfast A{item2} are at A{location1}.', {'location1': 'Pizza Hut'})
	node2 = Node([socket4, socket5])
	document1 = Document([node1, node2])
        
	#Node with sockets (not linked)
        counter = 0
	ng = t.get_generator(node1)
	for x in ng:
	    counter += 1
        self.assertEqual(counter, 4) #ensure iterator passes over every object in the substructure exactly once
	
	#Node with sockets (linked)
	socket6 = Socket('...AND A{extra1}, A{extra2} and A{extra3}!', {'extra1': 'bacon', 'extra2': 'eggs', 'extra3': 'cheese'})
	node3 = Node([socket6])
        socket3.link_node(node3)
	self.assertEqual(socket3.linked_node, node3)
        counter = 0
	ng = t.get_generator(node1)
	#pdb.set_trace()
	for x in ng:
	    counter += 1
	self.assertEqual(counter, 6)

	#Document with nodes
	counter = 0
        dg = t.get_generator(document1)
	for x in dg:
	    counter += 1
	self.assertEqual(counter, 10)
	
	#Socket with linked node
	counter = 0
        sg = t.get_generator(socket3)
	for x in sg:
	    counter += 1
	self.assertEqual(counter, 3)
	
	#Socket without linked node
        counter = 0
	sg = t.get_generator(socket5)
	for x in sg:
	    counter += 1
	self.assertEqual(counter, 1)

class Visitor_Test(unittest.TestCase):
    """Create a visitor subclass and assert the following on every type of component object:
    1) Component has an accept() method
    2) Component's accept() method calls correct visit_???() method on the visitor

    """

class Constructor_Test(unittest.TestCase):
    """Construct a document."""

class Printer_Test(unittest.TestCase):
    """Print a variety of component structures."""
#    p = Printer()
#
#    p.print_to_txt()
#    p.print_to_html()
#    p.print_to_tex()

if __name__ == "__main__":
    unittest.main()
