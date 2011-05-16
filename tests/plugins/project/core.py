import unittest
from mock import Mock
from thot.plugins.project.core import ProjectCreator

class TestProjectCreator(unittest.TestCase):

	def setUp(self):
		self.creator = ProjectCreator()
	
	def test_create_project(self):
		self.creator.create_root_dir = Mock()
		self.creator.create_metadata_dir = Mock()
		self.creator.create_metadata_file = Mock()
		self.creator.create('/tmp/aaa')
		self.creator.create_root_dir.assert_called_once_with('/tmp/aaa')
		self.creator.create_metadata_dir.assert_called_once_with('/tmp/aaa')
		self.creator.create_metadata_file.assert_called_once_with('/tmp/aaa')
