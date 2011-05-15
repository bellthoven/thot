from thot.plugins.project import ThotProject,OptionsValidator
from optparse import Values
import unittest
from mock import Mock

class TestOptionValidator(unittest.TestCase):

	def test_new_project(self):
		options = Values({
			'project_path': '/tmp/',
			'output': None,
			'format': None,
			'create_project': True,
		})
		opt = OptionsValidator(options)
		# make the path a valid one =)
		opt.has_project_metadata = Mock()
		opt.has_project_metadata.return_value = True
		try:
			opt.validate()
		except ValueError as e:
			self.assertTrue(False, "should never hit this line")
	
	def test_new_project_with_output_option(self):
		options = Values({
			'project_path': '/tmp/',
			'output': '/tmp/',
			'format': None,
			'create_project': True,
		})
		opt = OptionsValidator(options)
		# Remove output validation
		opt.validate_output = Mock()
		# make the path a valid one =)
		opt.has_project_metadata = Mock()
		opt.has_project_metadata.return_value = True
		self.assertRaisesRegex(ValueError, "Output path cannot be declared", opt.validate)
	
	def test_new_project_with_format_option(self):
		options = Values({
			'project_path': '/tmp/',
			'output': None,
			'format': 'html',
			'create_project': True,
		})
		opt = OptionsValidator(options)
		# make the path a valid one =)
		opt.has_project_metadata = Mock()
		opt.has_project_metadata.return_value = True
		self.assertRaisesRegex(ValueError, "Format cannot be declared", opt.validate)
	
	def test_output_as_required_option(self):
		options = Values({
			'project_path': '/tmp/',
			'output': None,
			'format': 'html',
			'create_project': None,
		})
		opt = OptionsValidator(options)
		# make the path a valid one =)
		opt.has_project_metadata = Mock()
		opt.has_project_metadata.return_value = True
		self.assertRaisesRegex(ValueError, 'Output path must be declared', opt.validate)
