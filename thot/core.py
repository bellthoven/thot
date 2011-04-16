
__all__ = ['Application']

import os
from pkg_resources import iter_entry_points

class Application(object):

	def __init__(self, args):
		self.args = args

	def bootstrap(self):
		self.initialized = True
		for module in iter_entry_points('plugins'):
			print("module")
	
	def run(self):
		pass
	
#class ModuleFinder(object):
#	
#	def get_list(self):
#		modules = []
#		modules_dir = os.path.join(os.getcwd(), "modules")
#		for filename in os.listdir(modules_dir):
#			print(filename)
#			if os.path.isdir(filename):
#				try:
#					__import__(filename)
#					modules.push(filename)
#				except ImportError:
#					pass
#		return modules
#
#class Modules:
#	modules = set()
#
#	def append(self, module):
#		self.modules.append(module)
#	
#	def remove(self, module):
#		if module in self.modules:
#			self.modules.remove(module)
#
