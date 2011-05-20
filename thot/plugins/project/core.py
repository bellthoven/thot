import os
from thot.exporter import FileScanner,YamlContent
from thot.plugins.project.docs import VisionDocument

class Project(object):

	path = None

	def __init__(self, path):
		self.path = path
	
	def create(self):
		self.creator = ProjectCreator()
		self.creator.create(self.path)
	
	def export_vision(self, objects, output):
		vision = VisionDocument(objects)
		vision.export(output)

class ProjectCreator(object):

	metadata_dir = ".thot"
	metadata_file = "project.yml"

	def create(self, path):
		self.create_root_dir(path)
		self.create_metadata_dir(path)
		self.create_metadata_file(path)
	
	def mkdir(self, path):
		if not os.path.isdir(path):
			os.mkdir(path)

	def create_root_dir(self, path):
		self.mkdir(path)
	
	def create_metadata_dir(self, path):
		mpath = os.path.join(path, self.metadata_dir)
		self.mkdir(mpath)
	
	def create_metadata_file(self, path):
		mpath = os.path.join(path, self.metadata_dir, self.metadata_file)
		f = open(mpath, "w+")
		f.write("\n".join(["Name: Project Name", "Description: Project Description"]))
		f.close()
