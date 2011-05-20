import os
from thot.plugins import PluginManager
from thot.exporter import FileScanner,YamlContent
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

	def parse_args(self):
		parser = optparse.OptionParser()
		self._event_handler.dispatch('on_before_parse_args', [parser])
		(self._options,_) = parser.parse_args(self.args)
		results = self._event_handler.dispatch('on_after_parse_args', [parser, self._options])
		for plugin_result in results:
			if ValueError in list(plugin_result):
				for result in plugin_results:
					if type(result) == ValueError: raise result
	
	def register_objects(self):
		fs = FileScanner()
		foundfiles = fs.scan(self._options.project_path)
		objs = []
		for filepath in foundfiles:
			obj = YamlContent.objectify(filepath, self._options.project_path)
			if obj:
				objs.append(obj)
		self._event_handler.dispatch('on_register_objects', [objs])
	
	def parse(self):
		self._event_handler.dispatch('on_before_parse', [])
		self._event_handler.dispatch('on_parse', [self._options])
		self._event_handler.dispatch('on_after_parse', [])

	def run(self):
		if not self._initialized:
			self.bootstrap()
		self.parse_args()
		self.register_objects()
		self.parse()

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
				if hasattr(plugin, event_name):
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
