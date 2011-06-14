import unittest
import mock
from thot.exporter import YamlContent
from thot.plugins.project.docs import VisionDocument

class TestVisionDocument(unittest.TestCase):

	def test_empty_export(self):
		objs = [
			YamlContent("project.yml", ""),
			YamlContent("actors.yml", ""),
			YamlContent("features.yml", "")
		]
		visiondoc = VisionDocument(objs)
		visiondoc.export("/tmp/")
