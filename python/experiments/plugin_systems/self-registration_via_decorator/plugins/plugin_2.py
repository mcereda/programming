#!/usr/bin/env python3

from plugin_manager import plugin

@plugin()
def hello_plugin_2():
    print('Hello from Plugin 2')
