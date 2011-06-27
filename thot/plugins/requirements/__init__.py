from thot.plugins import ThotPlugin
from thot.plugins.requirements.docs import SupplementarySpecification,SingleRequirementDocument
import re

class ThotRequirements(ThotPlugin):

	def name(self):
		return 'ThotRequirements'
	
	def description(self):
		return 'This is a requirements parser.'
	
	def on_before_parse_args(self, optparser):
		optparser.add_option('-r', '--sup-specs-doc', action="store_true",
			help="Exports supplementary specifications document", dest="sup_specs_doc")
		optparser.add_option('--single-requirement-docs', action="store_true",
			help="Exports a document for each requirement of the project", dest="single_req_doc")
		return optparser

	def on_register_documents(self, options, objs):
		reqregex = re.compile('^requirements/([^/]+/)?.+\.yml$')
		req_objs = filter(lambda obj: reqregex.match(obj.source()), objs)

		docs = []
		if options.sup_specs_doc:
			docs.append(SupplementarySpecification(req_objs))
		if options.single_req_doc:
			for obj in req_objs:
				docs.append(SingleRequirementDocument(obj))
		return docs
