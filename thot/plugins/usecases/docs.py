from thot.docs import ThotDocument

class SingleUseCaseDocument(ThotDocument):

	def __init__(self, usecase):
		filepath = usecase.source().replace('.yml', '.rst')
		title = usecase.get('Name')
		super(SingleUseCaseDocument, self).__init__(filepath, title)
		self.usecase = usecase
	
	def _append_description(self):
		description = self.usecase.get('Description')
		if description:
			self.start("section")
			self.append("title", "Description")
			self.append_raw(description)
			self.end() # section
	
	def _append_performers(self):
		actors = self.usecase.get('Actors')
		if actors:
			self.start("section")
			self.append("title", "Performers")
			self.start("bullet_list", bullet="*")
			for actor in actors:
				self.start("list_item")
				self.append("paragraph", ":ref:`%s`" % "/".join(actor))
				self.end() # list_item
			self.end() # bullet_list
			self.end() # section
	
	def _append_preconditions(self):
		preconditions = self.usecase.get('PreConditions')
		if preconditions:
			self.start("section")
			self.append("title", "Pre-Conditions")
			self.start("bullet_list", bullet="*")
			for precond in preconditions:
				self.start("list_item")
				self.append("paragraph", precond)
				self.end() # list_item
			self.end() # bullet_list
			self.end() # section

	def _append_postconditions(self):
		postconditions = self.usecase.get('PostConditions')
		if postconditions:
			self.start("section")
			self.append("title", "Post-Conditions")
			self.start("bullet_list", bullet="*")
			for postcond in postconditions:
				self.start("list_item")
				self.append("paragraph", postcond)
				self.end() # list_item
			self.end() # bullet_list
			self.end() # section
	
	def build(self):
		self._append_description()
		self._append_performers()
		self._append_preconditions()
		self._append_postconditions()
