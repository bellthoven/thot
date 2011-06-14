from thot.docs import ThotDocument,ThotDocumentBuilder
import os.path

class VisionDocument(ThotDocument):

	objects = {}
	_known_files = ('project.yml', 'actors.yml', 'features.yml')
	
	def __init__(self, objects):
		super(VisionDocument, self).__init__();
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
			self.doc.start("section")
			self.doc.append("title", "Positioning")
			self.doc.start("section")
			opportunity = project.get("Positioning.Opportunity")
			if opportunity:
				self.doc.append("title", "Oportunity")
				self.doc.append("paragraph", opportunity)
			self.doc.end()
			problem = project.get("Positioning.ProblemStatement")
			if problem:
				for part in ["Problem", "Affects", "Impact", "Solution"]:
					if part in problem.keys() and problem[part]:
						self.doc.start("section")
						self.doc.append("title", part)
						self.doc.append("paragraph", problem[part])
						self.doc.end() # section
			self.doc.end() # section
		except KeyError:
			pass

	def _export_actors_data(self):
		try:
			actors = self.objects['actors.yml']
			self.doc.start("section")
			self.doc.append("title", "Stakeholders and User Descriptions")
			for actor in actors.get():
				actor_data = actors.get(actor)
				self.doc.start("section")
				self.doc.append("title", actor_data['Name'])
				self.doc.append("paragraph", actor_data['Description'])
				self.doc.start("bullet_list", bullet="*")
				for resp in actor_data['Responsabilities']:
					self.doc.append("list_item", resp)
				self.doc.end() # bullet_list
				self.doc.end() # section
			self.doc.end() # section
		except KeyError:
			pass

	def _export_features_data(self):
		try:
			features = self.objects['features.yml']
			self.doc.start("section")
			self.doc.append("title", "Features")
			self.doc.start("definition_list")
			for feature in features.get('Features'):
				self.doc.append("item_list", feature['Feature'])
				self.doc.end() # section
			self.doc.end() # section
		except KeyError:
			pass
	
	def export(self, output):
		docpath = os.path.join(output, "vision.rst")
		self.doc = ThotDocumentBuilder(docpath, title="Vision")
		self.doc.append("title", "Vision Document")
		self._export_project_data()
		self._export_actors_data()
		self._export_features_data()
		content = self.generate_rst(self.doc)
		print(content)
		self.create_file(docpath, content)
