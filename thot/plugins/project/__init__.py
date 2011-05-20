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
		optparser.add_option('-o', '--output', action="store", default=os.getcwd(), type="string",
			help="Sets the output path for the project.", dest="output")
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

		srcdir = os.path.join(options.output, 'source')
		if options.vision_doc:
			project.export_vision(self.objects, srcdir)

class OptionsValidator(object):

	_options = None
	
	def __init__(self, options):
		self._options = options
	
	def validate(self):
		if self._options.create_project is None and self._options.format is None:
			self.format = 'html'

		self.validate_project_path()
		if self._options.create_project:
			self.validate_create_opts()
		elif self._options.format:
			self.validate_format_opts()
	
	def validate_project_path(self):
		if not os.path.isdir(self._options.project_path):
			raise ValueError('%s is not a valid path for the project.' % self._options.project_path)
		if not self.has_project_metadata(self._options.project_path):
			raise ValueError('%s seems to be an invalid project path.' % self._options.project_path)
	
	def has_project_metadata(self, path):
		return os.path.isdir(os.path.join(path, '.thot'))
	
	def validate_output(self):
		if os.path.isdir(self._options.output):
			raise ValueError('Output path %s already exists. Cannot output to this folder.' 
				% self._options.output)
		parent_dir = os.relpath(os.path.join(self._options.output, '..'))
		if not os.access(parent_dir, os.W_OK):
			raise ValueError('%s is not writable, so %s cannot be created.' % 
				(parent_dir, os.path.basename(self._options.outpu)))
	
	def validate_create_opts(self):
		if self._options.output is not None:
			raise ValueError('Output path cannot be declared with --create-project')
		elif self._options.format is not None:
			raise ValueError('Format cannot be declared with --create-project')

	def validate_format_opts(self):
		if self._options.output is None:
			raise ValueError('Output path must be declared with --output')
		else:
			self.validate_output()
