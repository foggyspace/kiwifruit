import os
from functools import partial
from pluginbase import PluginBase


here = os.path.abspath(os.path.dirname(__file__))

get_path = partial(os.path.join, here)


plugin_base = PluginBase(package='scanner.plugins', searchpath=[get_path('./plugins')])


class Application(object):
    def __init__(self, name):
        self.name = name
        self.plugins = {}

        self.source = plugin_base.make_plugin_source(searchpath=[get_path('./%s/plugins' % name)], identifier=self.name)

        for plugin_name in self.source.list_plugins():
            plugin = self.source.load_plugin(plugin_name)
            plugin.setup(self)

    def register_plugins(self, name, func):
        self.plugins[name] = func


def run_plugins(app, source):
    pass


def start():
    pass

