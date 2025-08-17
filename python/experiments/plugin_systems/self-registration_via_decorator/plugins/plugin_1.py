#!/usr/bin/env python3

from plugin_manager import plugin

@plugin()
def hello_plugin_1():
    print('Hello from Plugin 1')
