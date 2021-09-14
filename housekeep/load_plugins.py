import os
from pydoc import locate
from housekeep.utils import utils
# Get relative path from this file


def locate_plugins(only=None):
    plugins = []
    valid_plugins = []
    must_have_attributes = ['name', 'description', 'run_action']
    for file in os.listdir(utils.get_relative_path_from_utils('../plugins')):
        if not file.startswith('__') and file.endswith('.py'):
            plugins.append(file[:-3])
    for plugin in plugins:
        try:
            plugin_class = locate('housekeep.plugins.{}.{}'.format(plugin, plugin))
            instance = plugin_class()
            if(all(attr in dir(instance) for attr in must_have_attributes)):
                if(instance.name == only):
                    return plugin_class
                valid_plugins.append(plugin_class)
            else:
                print('Plugin class %s is missing required attributes.' % plugin)
        except ImportError:
            print('Plugin %s failed to load' % plugin)
    if(only):
        return [plugin for plugin in valid_plugins if plugin == only]
    return valid_plugins

def locate_interfaces(only=None):
    plugins = []
    valid_interfaces = []
    must_have_attributes = ['name', 'description']
    for file in os.listdir(utils.get_relative_path_from_utils('../interfaces')):
        if not file.startswith('__') and file.endswith('.py'):
            plugins.append(file[:-3])
    for plugin in plugins:
        try:
            plugin_class = locate('housekeep.interfaces.{}.{}'.format(plugin, plugin))
            instance = plugin_class([], None, None)
            if(all(attr in dir(instance) for attr in must_have_attributes)):
                if(instance.name == only):
                    return plugin_class
                valid_interfaces.append(plugin_class)
            else:
                print('Plugin class %s is missing required attributes.' % plugin)
        except ImportError:
            print('Plugin %s failed to load' % plugin)
    if(only):
        return [plugin for plugin in valid_interfaces if plugin == only]
    return valid_interfaces
