from thot.core import EventHandler,Application
from thot.plugins import ThotPlugin,PluginManager
import unittest
import optparse

class TestPlugin(ThotPlugin):
	def name(self):	return "ThotPlugin"

	def description(self): return "test test test"

	def on_before_parse_args(self, optparse):
		return "on_before_parse_args"

	def on_after_parse_args(self, options):
		return "on_after_parse_args"

class TestEventHandler(unittest.TestCase):

	def test_initial_state(self):
		""" Tests if on init everything is clear """
		event_handler = EventHandler([])
		self.assertEqual(event_handler._plugins, [])

		plugins = [TestPlugin()]
		event_handler = EventHandler(plugins)
		self.assertEqual(event_handler._plugins, plugins)
	
	def test_event_dispatch_specific_method(self):
		""" Tests if events are being dispatched for all plugins """
		event_handler = EventHandler([TestPlugin()])
		result = event_handler.dispatch('on_before_parse_args', [optparse.OptionParser()])
		for plugin in event_handler._plugins:
			self.assertEqual("on_before_parse_args", result[plugin.name()])
	
	def test_event_dispatch_default_method(self):
		""" Tests if events are being dispatched for all plugins """
		event_handler = EventHandler([TestPlugin()])
		result = event_handler.dispatch('on_after_parse_args', [dict()])
		for plugin in event_handler._plugins:
			self.assertEqual("on_after_parse_args", result[plugin.name()])

class TestApplication(unittest.TestCase):
	app = None

	def setUp(self):
		self.app = Application([])

	def test_initial_state(self):
		self.assertFalse(self.app._initialized)
		self.assertIsInstance(self.app._plugin_manager, PluginManager)
		self.assertEqual(self.app._event_handler, None)
	
	def test_bootstrap(self):
		self.app.bootstrap()
		self.assertTrue(self.app._initialized)
		self.assertIsInstance(self.app._event_handler, EventHandler)
