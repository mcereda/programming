#!/usr/bin/env python3

plugin_registry = {}

def plugin(name: str|None = None):
    def decorator(func):
        plugin_name: str = name or func.__name__
        plugin_registry[plugin_name] = func
        return func
    return decorator

def get_plugins():
    return plugin_registry
