#!/usr/bin/env python3

import plugins  # triggers dynamic load of all plugins in the directory
from plugin_manager import get_plugins

print('Available plugins:')
for name, plugin_func in get_plugins().items():
    print(f'- {name}')
    plugin_func()

plugins.plugin_1.hello_plugin_1()
