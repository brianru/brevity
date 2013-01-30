"""Usage: something

"""
import re, os


class socket(object):
	"""Store text. 
	Identify variables present in said text. 
	Enable text (& variables) to be extended.

	"""
	txt = '' #what happens when I remove this line?
	vars = dict() #what happens when I remove this line?
	link = None
	
	def __init__(self, txt = '', vars = dict(), link = None):
		self.txt = txt
		self.vars = vars
		self.link = link

	def __str__(self):
		if self.link:
			return '--->\n' + str(self.link) #refactor to show deprecated socket, with proper formatting
		else:
			return 'Type: %s \n    Text: %s \n    Variables: %s' % (type(self), self.txt, self.vars)

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
	Provide external access to document contents.

	"""
	nodes = []
	
	def __init__(self, nodes):
		self.nodes = nodes
		
	def __str__(self): 
		"""print stuff?"""

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
	Can I link object A to object B, directly, or to any of its children?
	Which objects can be linked to object A, directly, or to any of its children?
	
	"""

	def isCompatible(self, parent, child):
		"""
		Check nodes for compatibility
		Parent node must have a socket whose variables exist in the child's socket(s)
		Expand to return missing vars if there are any?

		"""
		childVars = set(child.getVars())
		for x in parent.sockets:
			if set(x.vars).issubset(childVars):
				return 1
		return -1
		
	def nodeCompare(self, comp1, comp2, recursive = False):
		"""
		1st parameter is the destination -- the tree
		2nd parameter is the alien Node being compared to part or all of the tree at and beneath the 1st parameter
		
		"""
		#if comp1 and comp2 are not both nodes, raise an exception
		place = [isCompatible(comp1, comp2)]
		if recursive == False:
			return place
		
		place = self.__recNodeCompare()
		
#	def __recNodeCompare(self, comp1, comp2):
		#dive!

#class finder(object):
#	"""This class will do something. I promise."""

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
	main()
