from thot.plugins import ThotPlugin
from thot.plugins.project.docs import (VisionDocument, Glossary)
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
		optparser.add_option('-g', '--glossary', action="store_true",
			help="Exports the glossary", dest="glossary")
		optparser.add_option('-v', '--vision-doc', action="store_true",
			help="Exports the vision document", dest="vision_doc")
		return optparser
	
	def on_after_parse_args(self, options):
		errors = []
		return errors
	
	def on_register_documents(self, options, objs):
		docs = []
		if options.vision_doc:
			docs.append(VisionDocument(objs))
		if options.glossary:
			docs.append(Glossary(objs))
		return docs
