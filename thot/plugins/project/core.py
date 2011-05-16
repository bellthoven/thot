import os

class Project(object):

	path = None

	def __init__(self, path):
		self.path = path
	
	def create(self):
		self.creator = ProjectCreator()
		self.creator.create(self.path)
	
	def parse(self, format, output):
		self.parse_to_sphinx(output)
		self.build(format, output)
	
	def parse_to_sphinx(self, output):
		print("parse_to_sphinx")
		pass
	
	def build(self, format, output):
		print("build")
		pass

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
		os.mkdir(mpath)
	
	def create_metadata_file(self, path):
		mpath = os.path.join(path, self.metadata_dir, self.metadata_file)
		f = open(mpath, "w+")
		f.write("\n".join(["Name: Project Name", "Description: Project Description"]))
		f.close()
