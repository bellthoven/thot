from thot.plugins import ThotPlugin
from thot.plugins.usecases.docs import SingleUseCaseDocument
import re

class ThotUseCase(ThotPlugin):

	def name(self):
		return 'ThotUseCase'
	
	def description(self):
		return 'This is a use case parser.'
	
	def on_before_parse_args(self, optparser):
		optparser.add_option('-u', '--single-usecase-docs', action="store_true",
			help="Exports a document for each use case of the project", dest="single_usecase_doc")
		return optparser
	
	def on_register_documents(self, options, objs):
		ucregex = re.compile('^usecases/.*.yml')
		ucs_objs = filter(lambda obj: ucregex.match(obj.source()), objs)

		docs = []
		if options.single_usecase_doc:
			docs = [SingleUseCaseDocument(obj) for obj in ucs_objs]
		return docs
