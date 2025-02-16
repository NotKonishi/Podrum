################################################################################
#                                                                              #
#  ____           _                                                            #
# |  _ \ ___   __| |_ __ _   _ _ __ ___                                        #
# | |_) / _ \ / _` | '__| | | | '_ ` _ \                                       #
# |  __/ (_) | (_| | |  | |_| | | | | | |                                      #
# |_|   \___/ \__,_|_|   \__,_|_| |_| |_|                                      #
#                                                                              #
# Copyright 2021 Podrum Studios                                                #
#                                                                              #
# Permission is hereby granted, free of charge, to any person                  #
# obtaining a copy of this software and associated documentation               #
# files (the "Software"), to deal in the Software without restriction,         #
# including without limitation the rights to use, copy, modify, merge,         #
# publish, distribute, sublicense, and/or sell copies of the Software,         #
# and to permit persons to whom the Software is furnished to do so,            #
# subject to the following conditions:                                         #
#                                                                              #
# The above copyright notice and this permission notice shall be included      #
# in all copies or substantial portions of the Software.                       #
#                                                                              #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR   #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,     #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING      #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS #
# IN THE SOFTWARE.                                                             #
#                                                                              #
################################################################################

from constant.version import version
import importlib
import json
import os
import sys
from zipfile import ZipFile

class plugin_manager:
    def __init__(self, server: object) -> None:
        self.server: object = server
        self.plugins: dict = {}
        
    def load(self, path: str) -> None:
        plugin_file = ZipFile(path, "r")
        plugin_info: dict = json.loads(plugin_file.read("info.json"))
        if plugin_info["name"] in self.plugins:
            self.server.logger.alert(f"A plugin with the name {plugin_info['name']} already exists.")
            return
        if plugin_info["api_version"] != version.podrum_api_version:
            self.server.logger.alert(f"A plugin with the name {plugin_info['name']} could not be loaded due to incompatible api version ({plugin_info['api_version']}).")
            return
        self.server.logger.info(f"Loading {plugin_info['name']}...")
        sys.path.append(path)
        main: str = plugin_info["main"].rsplit(".", 1)
        module: object = importlib.import_module(main[0])
        main_class: object = getattr(module, main[1])
        self.plugins[plugin_info["name"]]: object = main_class()
        self.plugins[plugin_info["name"]].server: object = self.server
        self.plugins[plugin_info["name"]].path: str = path
        self.plugins[plugin_info["name"]].version: str = plugin_info["version"] if "version" in plugin_info else ""
        self.plugins[plugin_info["name"]].description: str = plugin_info["description"] if "description" in plugin_info else ""
        self.plugins[plugin_info["name"]].author: str = plugin_info["author"] if "author" in plugin_info else ""
        if hasattr(main_class, "on_load"):
            self.plugins[plugin_info["name"]].on_load()
        self.server.logger.success(f"Successfully loaded {plugin_info['name']}.")
        
    def load_all(self, path: str) -> None:
        for top, dirs, files in os.walk(path):
            for file_name in files:
                full_path: str = os.path.abspath(os.path.join(top, file_name))
                if full_path.endswith(".pyz") or full_path.endswith(".zip"):
                    self.load(full_path)
        
    def unload(self, name: str) -> None:
        if name in self.plugins:
            if hasattr(self.plugins[name], "on_unload"):
                self.plugins[name].on_unload()
            del self.plugins[name]
            self.server.logger.info(f"Unloaded {name}.")
            
    def unload_all(self) -> None:
        for name in dict(self.plugins):
            self.unload(name)
                                   
    def reload(self, name: str) -> None:
        if name in self.plugins:
            path: str = self.plugins[name].path
            self.unload(name)
            self.load(path)
                                   
    def reload_all(self) -> None:
        for name in dict(self.plugins):
            self.reload(name)
