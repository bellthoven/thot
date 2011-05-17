import thot.exporter as exporter
import mock
import unittest
import os

class TestFileScanner(unittest.TestCase):

	def test_scanning_yml_files(self):
		with mock.patch('os.walk') as mock_oswalk:
			mock_oswalk.return_value = (
				("tmp", ["lero", "lira"], ["hahaha.yml"]),
				("tmp/lero", [], ["hehehe.yml"]),
				("tmp/lira", ["a"], []),
				("tmp/lira/a", [], ["jota.yml", "dirty.txt"])
			)
			expected = ["hahaha.yml", "lero/hehehe.yml", "lira/a/jota.yml"]
			fs = exporter.FileScanner()
			result = fs.scan('tmp')
			self.assertEqual(expected, result)
	
	def test_valid_yml_files(self):
		with mock.patch("os.path.isfile") as mock_isfile:
			mock_isfile.return_value = True
			fs = exporter.FileScanner()
			self.assertFalse(fs.is_valid_file("teste.yyml"))
			self.assertTrue(fs.is_valid_file("teste.yml"))
	
	def test_objectify_yml_files(self):
		with mock.patch("%s.open" % __name__, create=True) as mock_open:
			mock_open.return_value = mock.Mock()
			fs = exporter.FileScanner()
			filename = "projectsample/project.yml"
			obj = fs.objectify(filename)
			self.assertIsInstance(obj, exporter.YamlContent)

			obj = fs.objectify("something.txt")
			self.assertFalse(obj)
	

class TestYamlContent(unittest.TestCase):

	def setUp(self):
		content = """
Content: 1st Level
ContentWithSub:
    Second : Second Level
    HTML: |
        Very large HTML
        Very
        Very
        Large
    Literal: >
        This text has
        no line breaks
List:
  - item 1
  - item 2
"""
		self.yaml = exporter.YamlContent("source.yaml", content)
	
	def test_source(self):
		self.assertEqual("source.yaml", self.yaml.source())

	def test_first_level_yaml(self):
		self.assertEqual(self.yaml.get('Content'), "1st Level")
	
	def test_multiple_levels_yaml(self):
		self.assertEqual(self.yaml.get('ContentWithSub.Second'), "Second Level")
	
	def test_long_texts_yaml(self):
		expected = "Very large HTML\nVery\nVery\nLarge"
		self.assertEqual(self.yaml.get("ContentWithSub.HTML"), expected)
	
	def test_noline_breaks_yaml(self):
		expected = "This text has no line breaks"
		self.assertEqual(self.yaml.get("ContentWithSub.Literal"), expected)

	def test_lists(self):
		self.assertEqual(["item 1", "item 2"], self.yaml.get("List"))
