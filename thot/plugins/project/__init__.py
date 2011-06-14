from thot.plugins import ThotPlugin
from thot.plugins.project.core import Project
import os

class ThotProject(ThotPlugin):
	
	objects = []
	
	def name(self):
		return 'ThotProject'
	
	def description(self):
		return 'This is a project parser.'
	
	def on_before_parse_args(self, optparser):
		optparser.add_option('-p', '--project-path', action="store", default=os.getcwd(),  type="string",
			help="Sets the path for the project.", dest="project_path")
		optparser.add_option('-s', '--source-dir', action="store", default="source", type="string",
			help="Sets the source directory for the project (relative to the project path)", dest="source_dir")
		optparser.add_option('-b', '--build-dir', action="store", default="build", type="string",
			help="Sets the build directory for the project (relative to the project path)", dest="build_dir")
		optparser.add_option('-f', '--format', action="append", choices=('html', 'pdf'),
			help="Sets the output format", dest="format")
		optparser.add_option('-c', '--create-project', action="store_true",
			help="Sets the output format", dest="create_project")
		optparser.add_option('-v', '--vision-doc', action="store_true",
			help="Exports the vision document", dest="vision_doc")
		return optparser
	
	def on_after_parse_args(self, optparser, options):
		opt = OptionsValidator(options)
		errors = []
		try:
			opt.validate()
		except ValueError as e:
			errors.append(e)
		return errors
	
	def on_register_objects(self, objs):
		self.objects = objs
	
	def on_parse(self, options):
		project = Project(options.project_path)
		if options.create_project:
			project.create()
			return None

		builddir = os.path.join(options.project_path, options.build_dir)
		if options.vision_doc:
			project.export_vision(self.objects, builddir)

class OptionsValidator(object):

	_options = None
	
	def __init__(self, options):
		self._options = options
	
	def validate(self):
		if self._options.create_project is None:
			self.validate_project_path()
	
	def validate_project_path(self):
		dirs_to_test = ('', self._options.source_dir, self._options.build_dir)
		for filepath in dirs_to_test:
			path = os.path.join(self._options.project_path, filepath)
			if not os.path.isdir(path):
				raise ValueError('%s is not a valid path for the project, bacause %s is not a directory.' % (self._options.project_path, path))
