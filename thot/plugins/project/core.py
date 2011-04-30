
class Project(object):

	path = None

	def __init__(self, path):
		self.path = path
	
	def parse(self, format, output):
		self.parse_to_sphinx(output)
		self.build(format, output)
	
	def parse_to_sphinx(self, output):
		print("parse_to_sphinx")
		pass
	
	def build(self, format, output):
		print("build")
		pass
