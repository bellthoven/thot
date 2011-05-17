import os
from thot.exporter import FileScanner,YamlContent

class Project(object):

	path = None
	_known_files = ('project.yml', 'actors.yml', 'features.yml')

	def __init__(self, path):
		self.path = path
	
	def create(self):
		self.creator = ProjectCreator()
		self.creator.create(self.path)
	
	def parse(self, format, output):
		scanner = FileScanner()
		files = scanner.scan(self.path)
		objects = []
		for knownfile in self._known_files:
			if knownfile in files:
				fullfilepath = os.path.join(self.path, knownfile)
				objects.append( YamlContent.objectify(fullfilepath) )
		# TODO: parse objects =)

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
