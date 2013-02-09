"""Usage: something
Making a change!

"""
import re, os

##########  MODEL  ##########
class socket(object):
	"""Store text. 
	Identify variables present in said text with default values. 
	Enable text (& variables) to be extended via a linked node.

	"""
	text = ''
	vars = dict()
	link = None
	
	def __init__(self, text = '', vars = {}, link = None):
		self.text = txt
		self.vars = vars
		self.link = link

	def __str__(self):
		if self.link:
			return '--->\n' + str(self.link) #refactor to show deprecated socket, with proper formatting
		else:
			return 'Type: %s \n    Text: %s \n    Variables: %s' % (type(self), self.text, self.vars)

	def linkToNode(self, node):
		self.link = node
		
	def getVars(self, key):#refactor as a vars access method?
		"""Replaces a specified key with its corresponding value in the socket's dictionary.
		
		"""
		return self.vars[key.group(1)]

class node(object):
	"""Define document structure via an [ordered] array of sockets.

	"""
	sockets = []
	
	def __init__(self, sockets):
		self.sockets = sockets
		
	def getVars(self):
		allVars = []
		for x in sockets:
			allVars.append(x.vars.keys())
		return allVars	
	
	def __str__(self):
		"""Print a summary of the Node."""
		output = []
		output.append('Type: %s' % (type(self))) #begin by identifying the node's type
		for x in self.sockets:
			output.append(str(x))
		return '\n'.join(output)

class document(object):
	"""Define initial document structured via an [ordered] array of nodes. 
	Contain instance variables.

	"""
	nodes = []
	instanceVars = dict()
	
	def __init__(self, nodes, instanceVars = {}):
		self.nodes = nodes
		self.instanceVars = instanceVars
		
	def __str__(self): 
		"""print stuff?"""

##########  CONTROLLER  ##########
class traverse(object):
	"""Traverse tree downwards, performing a specified action at each level.

	"""
	pass


class compiler(object): 
	"""
	Recursively compile whichever document component is passed to the compiler.
	Supports raw text or latex code.
	
	"""
	
	output = [] #build code to handle multiple compile calls
	backupOutput = []
	
	def __compileSocket(self, component):
		"""Only compile method to actually update the output array.
		   Which means the # of items in output = the # of active sockets.
		   
		"""
		if component.link:
			self.__compileNode(component.link)
		else:
			self.output.append(re.sub(r'A{(\w.*?)}', component.getVars, component.txt)) 
	
	def __compileNode(self, component):
		for x in component.sockets:
			self.__compileSocket(x)
	
	def __compileDocument(self, component):
		for x in component.nodes:
			self.__compileNode(x)
	
	def compile(self, component, latex = False):
		"""Routing method."""
		if not self.output:
			self.backupOutput.append(self.output)
			self.output = []

		if component.__class__.__name__ == 'socket':
			self.__compileSocket(component)
		elif component.__class__.__name__ == 'node':
			self.__compileNode(component)
		elif component.__class__.__name__ == 'document':
			self.__compileDocument(component)
		else:
			return "What are you passing me?!?"
		
		if latex:
			self.output.insert(0,"\\documentclass[12pt]{article}")
			self.output.insert(0,"\\begin{document}")
			self.output.append("\\end{document}")
			
			f = open('doc.tex', 'w') #append number to filename to enable multiple calls to compile latex
			print f
			f.write('\n'.join(self.output))
			f.close()
			
			os.system("pdflatex doc.tex")
			
			return 'Seccesfully generated doc.pdf!'
			
		else:
			return self.output

class printer(object): 
	"""this will print stuff"""
	
class comparer(object):
	"""
	Q1: Can I link object A to object B[, or to any of its children]?
	Q2: Which objects can be linked to object A, directly, or to any of its children?
	
	"""
	def isCompatible(self, parent, child):
		"""Q1: Can I link object A to object B[, or to any of its children]?  
		Check nodes for compatibility 
		Parent node must have a socket whose variables exist in the child's socket(s) 
		Expand to return missing vars if there are any?  
		
		"""
		childVars = set(child.getVars())
		for x in parent.sockets:
			if set(x.vars).issubset(childVars):
				return 1
		return -1

class USConstitution(unittest.TestCase):
	"""Construct the .txt version of the US constitution.
	Refactor to test a suite of documents.

	"""
	def test_US_Constitution(self):
		pass
	
class SimUser(unittest.TestCase):
	"""Simulate a user defining and drafting a document.

	"""
	def test_Sim_User(self):
		pass

def main():
	#Create Tier 1 Sockets
	test0 = socket('My name is A{name}.', 
	               {'name': 'Brian J Rubinton'})
	test1 = socket('I live at A{address}.', 
	               {'address': '63 Thompson Street'})
	test2 = socket('There is a good A{shop} near me.', 
	               {'shop': 'cigar store'})

#Create Tier 1 Node
	testnode = node([test0, test1, test2])
	
#Create Tier 2 Sockets
	test2a1 = socket('There is a good A{shop} near me. It is in fact my favorite A{shop} in the whole city!', 
	                 {'shop': 'cigar store'})
	test2a2 = socket('Its address is A{shop_address}.', 
	                 {'shop_address': '82 West Broadway'})

#Create Tier 2 Node
	test2a = node([test2a1, test2a2])

#Create Tier 3 Socket
	test2a2a1 = socket('Its address is A{shop_address}, between A{cross_street_1} and A{cross_street_2}.', 
	                   {'shop_address': '82 West Broadway',
	                    'cross_street_1': 'Broome', 
	                    'cross_street_2': 'Spring'})

#Create Tier 3 Node
	test2a2a = node([test2a2a1])

#Link Tier 3 to Tier 2
	test2a2.linkToNode(test2a2a)
	
#Link Tier 2 to Tier 1
	test2.linkToNode(test2a)
	
	c = compiler()
	print c.compile(testnode, False)


if __name__ == "__main__":
	unittest.main()
