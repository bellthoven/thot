import os
from thot.plugins import PluginManager
from thot.exporter import FileScanner,YamlContent
import optparse
import thot.utils

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
		results = self._event_handler.dispatch('on_after_parse_args', [self._options])
		for plugin_result in results.values():
			for result in plugin_result:
				if isinstance(result, ValueError):
					thot.utils.print_err(result)
					thot.utils.exit( thot.utils.ERROR_EXIT )
	
	def register_documents(self):
		all_docs = self._event_handler.dispatch('on_register_documents', [self._options])
		self.documents = []
		for plugname in all_docs:
			docs = all_docs[plugname]
			self.documents.extend(docs)
	
	def build_documents(self):
		fs = FileScanner()
		srcdir = os.path.join(self._options.project_path, self._options.source_dir)
		foundfiles = fs.scan(srcdir)
		objs = []
		for filepath in foundfiles:
			obj = YamlContent.objectify(filepath, srcdir)
			if obj:
				objs.append(obj)
		for doc in self.documents:
			docinstance = doc(objs)
			self._event_handler.dispatch('on_before_build_document', [docinstance])
			docinstance.build()
			self._event_handler.dispatch('on_after_build_document', [docinstance])
			self._event_handler.dispatch('on_before_export_document', [docinstance])
			docinstance.export("")
			self._event_handler.dispatch('on_after_export_document', [docinstance])
	
	def run(self):
		if not self._initialized:
			self.bootstrap()
		self.parse_args()
		self.register_documents()
		self.build_documents()

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
