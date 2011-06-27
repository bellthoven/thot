from pkg_resources import iter_entry_points

class ThotPlugin(object):

	def name(self): abstract
	
	def description(self): abstract
	
	def bootstrap(self): pass

	def on_before_parse_args(self, optparser): pass

	def on_after_parse_args(self, options): return dict()

	def on_register_documents(self, options, objs): pass

	def on_before_build_document(self, document): pass

	def on_after_build_document(self, document): pass

	def on_before_export_document(self, document): pass

	def on_after_export_document(self, document): pass

	def __str__(self):
		return self.name()

class PluginManager(object):
	_loaded = []
	_builtins = (
		('thot.plugins.project', 'ThotProject'),
		('thot.plugins.requirements', 'ThotRequirements'),
	)

	def _load_builtin_plugins(self):
		for module,class_name in self._builtins:
			plugin_module = __import__(module, globals(), locals(), [class_name])
			plugin = getattr(plugin_module, class_name)() # Initialize!
			self.add_plugin( plugin )
			globals()[class_name] = plugin

	def load_plugins(self):
		self._load_builtin_plugins()

		for plugin in iter_entry_points(group='thot.plugins'):
			loaded_plugin = plugin.load()
			try:
				plugin = loaded_plugin() # instanciate plugin's class
				self.add_plugin( plugin )
				return True
			except:
				return False

	def add_plugin(self, plugin):
		if isinstance(plugin, ThotPlugin) and plugin not in self._loaded:
			self._loaded.append( plugin )

	def plugins(self):
		return iter(self._loaded)
