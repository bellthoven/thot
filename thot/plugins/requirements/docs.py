from thot.docs import ThotDocument,ThotDocumentBuilder
import re

class SupplementarySpecification(ThotDocument):

	def __init__(self, objects):
		super(SupplementarySpecification, self).__init__("supplementary_specification.rst", \
			"Supplementary Specification")
		self.objects = self.filter_objects(objects)
	
	def filter_objects(self, objects):
		filtered_objs = {}
		project_reqs = re.compile('^requirements/[^/]+/.+\.yml$')
		for obj in objects:
			if project_reqs.match(obj.source()):
				obj_type = obj.get('Type')
				if obj_type is not None:
					if not filtered_objs.get(obj_type):
						filtered_objs[obj_type] = []
					filtered_objs[obj_type].append( obj )
			elif obj.source() == 'requirements/project.yml':
				filtered_objs['_PROJECT_'] = obj
		return filtered_objs
	
	def append_product_section(self, title, index=None):
		if index is None:
			index = title
		try:
			objects = self.objects[index]
		except KeyError:
			return
		self.start("section")
		self.append("title", title)
		for obj in objects:
			self.start("section")
			self.append("title", obj.get('Name'))
			self.append_raw(obj.get('Description'))
			self.end() # section
		self.end() # section
	
	def append_project_section(self, title, index):
		try:
			obj = self.objects['_PROJECT_']
			content = obj.get(index)
			if content:
				self.start("section")
				self.append("title", title)
				self.append_raw( content )
				self.end() # section
		except KeyError:
			pass

	def build(self):
		self.append_product_section("Functionalities", "Functional")
		self.append_product_section("Usability")
		self.append_product_section("Reliability")
		self.append_product_section("Performance")
		self.append_product_section("Supportability")
		self.append_product_section("Design Constraint")
		self.append_project_section("Online User Documentation and Help System Requirements", "Documentation")
		self.append_project_section("Purchased Components", "Components")
		self.append_project_section("Interfaces", "Interfaces")
		self.append_project_section("Licensing Requirements", "License")
		self.append_project_section("Legal, Copyright and Other Notices", "Copyrights")
		self.append_project_section("Applicable Standards", "Standards")
