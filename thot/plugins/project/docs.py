from thot.docs import ThotDocument,ThotDocumentBuilder
import os.path

class VisionDocument(ThotDocument):

	objects = {}
	_known_files = ('project.yml', 'actors.yml', 'features.yml')
	
	def __init__(self, objects):
		super(VisionDocument, self).__init__("vision.rst", "Vision Document")
		self.objects = self.filter_objects(objects)
	
	def filter_objects(self, objects):
		filtered_objs = {}
		for obj in objects:
			if obj.source() in self._known_files:
				filtered_objs[obj.source()] = obj
		return filtered_objs
	
	def _export_project_data(self):
		try:
			project = self.objects['project.yml']
			self.start("section")
			self.append("title", "Positioning")
			self.start("section")
			opportunity = project.get("Positioning.Opportunity")
			if opportunity:
				self.append("title", "Oportunity")
				self.append("paragraph", opportunity)
			self.end()
			problem = project.get("Positioning.ProblemStatement")
			if problem:
				for part in ["Problem", "Affects", "Impact", "Solution"]:
					if part in problem.keys() and problem[part]:
						self.start("section")
						self.append("title", part)
						self.append("paragraph", problem[part])
						self.end() # section
			self.end() # section
		except KeyError:
			pass

	def _export_actors_data(self):
		try:
			actors = self.objects['actors.yml']
			self.start("section")
			self.append("title", "Stakeholders and User Descriptions")
			for actor in actors.get():
				actor_data = actors.get(actor)
				self.start("section")
				self.append("title", actor_data['Name'])
				self.append("paragraph", actor_data['Description'])
				self.start("bullet_list", bullet="*")
				for resp in actor_data['Responsabilities']:
					self.append("list_item", resp)
				self.end() # bullet_list
				self.end() # section
			self.end() # section
		except KeyError:
			pass

	def _export_features_data(self):
		try:
			features = self.objects['features.yml']
			self.start("section")
			self.append("title", "Features")
			self.start("definition_list")
			for feature in features.get():
				self.start("definition_list_item")
				self.append("term", features.get("%s.Name" % feature))
				self.append("definition", features.get("%s.Description" % feature))
				self.end() # definition_list_item
			self.end() # definition_list
			self.end() # section
		except KeyError:
			pass
	
	def build(self):
		docpath = os.path.join(output, )
		self._export_project_data()
		self._export_actors_data()
		self._export_features_data()

class Glossary(ThotDocument):

	def __init__(self, objects):
		super(Glossary, self).__init__('glossary.rst', "Glossary")
		self.objects= self.filter_objects(objects)
	
	def filter_objects(self, objects):
		try:
			for obj in objects:
				if obj.source() == 'glossary.yml':
					return {'glossary.yml': obj}
		except KeyError:
			pass
		return {}

	def build(self):
		try:
			self.start("definition_list")
			glossary = self.objects['glossary.yml']
			for term in glossary.get():
				self.start("definition_list_item")
				self.append("term", glossary.get("%s.Name" % feature))
				self.append("definition", glossary.get("%s.Description" % feature))
				self.end() # definition_list_item
			self.end() # definition_list
		except KeyError:
			pass
