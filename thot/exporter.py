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

	def is_valid_file(self, yamlfile):
		return yamlfile.endswith('.yml') and os.path.isfile(yamlfile)
	
	def objectify(self, yamlfile):
		if self.is_valid_file(yamlfile):
			with open(yamlfile, "r") as f:
				yamlcontent = f.read()
				f.close()
			return YamlContent(yamlfile, yamlcontent)
		return False

class YamlContent(object):
	
	def __init__(self, source, content):
		self._source = source
		self.content = yaml.load(content)
	
	def source(self):
		return self._source
	
	def get(self, index):
		elements = index.split(".")
		curr = self.content
		for el in elements:
			try:
				curr = curr[el]
				if hasattr(curr, 'strip'): curr = curr.strip()
			except KeyError:
				return None
		return curr
