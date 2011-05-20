import thot.docs

class VisionDocument(thot.docs.ThotDocument):

	objects = {}
	_known_files = ('project.yml', 'actors.yml', 'features.yml')
	
	def __init__(self, objects):
		self.objects = self.filter_objects(objects)
	
	def filter_objects(self, objects):
		filtered_objs = {}
		for obj in objects:
			if obj.source() in self._known_files:
				filtered_objs[obj.source()] = obj
		return filtered_objs
	
	def export_project_data(self):
		try:
			project = self.objects['project.yml']

		except KeyError:
			pass

	def export_actors_data(self):
		pass

	def export_features_data(self):
		pass
	
	def export(self, output):
		self.export_project_data()
		self.export_actors_data()
		self.export_features_data()
		pass
