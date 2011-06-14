import lxml.etree as etree
from io import StringIO
import docutils.nodes
import docutils.utils
import os.path

class ThotDocument(object):

	def __init__(self):
		self.xml2rst_file = os.path.join(
			os.path.dirname(__file__),
			'files',
			"xml2rst.xsl"
		)

	def generate_rst(self, document):
		rst = ""
		with  open(self.xml2rst_file) as xml2rst_xslt:
			xml2rst = etree.XSLT(etree.parse(xml2rst_xslt, etree.XMLParser()))
			xml = etree.parse(StringIO(str(document)), etree.XMLParser())
			rst = xml2rst( xml );
		return rst

	def create_file(self, filepath, content):
		print("Creating %s" % filepath)
		pass

class ThotDocumentBuilder(object):
	""" This class was based on http://docutils.sourceforge.net/sandbox/tibs/pysource/buildtree.py """
	def __init__(self, document, **params):
		self.root = docutils.utils.new_document(document)
		self.stack = []

	def start(self, element, *args, **kargs):
		instance = self.instantiate(element, *args, **kargs)
		if instance is not None:
			if len(self.stack) > 0:
				self.stack[-1].append( instance )
			else:
				self.root.append( instance )
			self._push( instance )
		return instance

	def end(self):
		if len(self.stack) == 0:
			instance = self.root
		else:
			instance = self._pop()
		return instance

	def _push(self, instance):
		self.stack.append( instance )

	def _pop(self):
		return self.stack.pop()

	def append(self, element, *args, **kargs):
		if element == "text": element = "Text"
		instance = self.instantiate(element, *args, **kargs)
		if len(self.stack) == 0:
			self.root.append( instance)
		else:
			self.stack[-1].append( instance )

	def instantiate(self, element, *args, **kargs):
		node = getattr(docutils.nodes, element)
		realargs = []
		# Text elements doesn't need first arg
		if element != "Text":
			realargs.append(None)
		for x in args: 
			# list_item requires text nodes, so let's make it easier
			if element == "list_item":
				x = self.instantiate("Text", x)
			realargs.append(x) 
		return node(*realargs, **kargs)

	def __str__(self):
		return str(self.root)

