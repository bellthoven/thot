import os
import yaml

class FileScanner(object):
	
	def scan(self, scan_root):
		selectedFiles = []
		for root,dirs,files in os.walk(scan_root):
			for f in files:
				if f.endswith('.yml'):
					# Normalize paths
					f = os.path.join(root,f)
					f = os.path.relpath(f, scan_root)
					selectedFiles.append(f)
		return selectedFiles

class YamlContent(object):

	@staticmethod
	def objectify(yamlfile, project_base):
		filepath = os.path.join(project_base, yamlfile)
		if os.path.isfile(filepath):
			with open(filepath, "r") as f:
				yamlcontent = f.read()
				f.close()
			return YamlContent(yamlfile, yamlcontent)
		return False
	
	def __init__(self, source, content):
		self._source = source
		self.content = yaml.load(content)
	
	def source(self):
		return self._source
	
	def get(self, index=None):
		if index is None:
			return self.content.keys()

		elements = index.split(".")
		curr = self.content
		for el in elements:
			try:
				curr = curr[el]
				if hasattr(curr, 'strip'): curr = curr.strip()
			except KeyError:
				return None
		return curr
