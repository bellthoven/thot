import unittest
from mock import Mock,patch
from thot.plugins.project.core import ProjectCreator

class TestProjectCreator(unittest.TestCase):

	def test_create_project(self):
		with patch("os.path.isdir") as mock_isdir:
			# Force os.mkdir execution
			mock_isdir.return_value = False
			with patch("os.mkdir") as mock_mkdir:
				self.creator = ProjectCreator()
				self.creator.mkdir = Mock()
				self.creator.create_metadata_file = Mock()
				self.creator.create('/tmp/aaa')
				self.creator.mkdir.assert_called_with('/tmp/aaa/.thot')
				self.creator.create_metadata_file.assert_called_with('/tmp/aaa')
