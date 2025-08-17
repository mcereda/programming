# Plugin system with self-registration via decorator

Directory structure:

```plaintext
project/
├── app.py
├── plugin_manager.py
└── plugins/
    ├── __init__.py
    ├── plugin_1.py
    └── plugin_2.py
```

The plugin manager (`plugin_manager.py`) defines a decorator that can be used to register plugins:

```py
plugin_registry = {}

def plugin(name=None):
    def decorator(func):
        plugin_name = name or func.__name__
        plugin_registry[plugin_name] = func
        return func
    return decorator

def get_plugins():
    return plugin_registry
```

Plugins use the decorator to register themselves:

```py
from plugin_manager import plugin

@plugin()
def hello_plugin_X():
    print('Hello from Plugin X')
```

The __init__.py dynamically imports plugins in the same directory:

```py
import os
import importlib

current_dir = os.path.dirname(__file__)
for filename in os.listdir(current_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = filename[:-3]
        importlib.import_module(f'{__name__}.{module_name}')
```

Main app:

```py
import plugins  # triggers dynamic load of all plugins in the directory
from plugin_manager import get_plugins

print('Available plugins:')
for name, plugin_func in get_plugins().items():
    print(f'- {name}')
    plugin_func()
```
