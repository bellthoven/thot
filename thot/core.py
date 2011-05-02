import os
from thot.plugins import PluginManager
import optparse

class Application(object):
	_initialized = False
	_options = None
	_plugin_manager = None
	_event_handler = None

	def __init__(self, args):
		self.args = args
		self._plugin_manager = PluginManager()
	
	def bootstrap(self):
		self._initialized = True
		self._plugin_manager.load_plugins()
		self._event_handler = EventHandler(self._plugin_manager.plugins())

	def _parse_args(self):
		parser = optparse.OptionParser()
		self._event_handler.dispatch('on_before_parse_args', [parser])
		(self._options,_) = parser.parse_args(self.args)
		results = self._event_handler.dispatch('on_after_parse_args', [parser, self._options])
		for plugin_result in results:
			print(plugin_result)
			if ValueError in list(plugin_result):
				for result in plugin_results:
					if type(result) == ValueError: raise result

	def run(self):
		if not self._initialized:
			self.bootstrap()
		self._parse_args()
		for plugin in self._plugin_manager.plugins():
			plugin.run(self._options)

class EventHandler(object):

	_plugins = None

	def __init__(self, plugins):
		self._plugins = list(plugins)

	def dispatch(self, event_name, args):
		event = hasattr(self, event_name)
		ret = dict()
		if event:
			ret = getattr(self, event_name)(*args)
		else:
			ret = dict()
			for plugin in self._plugins:
				ret[plugin.name()] = getattr(plugin, event_name)(*args)
		return ret
	
	def on_before_parse_args(self, parser):
		optgroups = dict()
		for plugin in self._plugins:
			optgroup = optparse.OptionGroup(parser, "Options for %s" % plugin.name(),
				""" This options are available only for this plugin """)
			retval = plugin.on_before_parse_args(optgroup)
			parser.add_option_group( retval )
			optgroups[plugin.name()] = retval
		return optgroups
