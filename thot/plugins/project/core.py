import os

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
