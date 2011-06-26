from thot.plugins import ThotPlugin
from thot.plugins.requirements.docs import SupplementarySpecification

class ThotRequirements(ThotPlugin):

	def name(self):
		return 'ThotRequirements'
	
	def description(self):
		return 'This is a requirements parser.'
	
	def on_before_parse_args(self, optparser):
		optparser.add_option('-r', '--sup-specs-doc', action="store_true",
			help="Exports supplementary specifications document", dest="sup_specs_doc")
		return optparser

	def on_register_documents(self, options):
		docs = []
		if options.sup_specs_doc:
			docs.append(SupplementarySpecification)
		return docs
