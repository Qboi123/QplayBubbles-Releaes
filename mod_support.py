import os
from typing import *


class Loader:
    def __init__(self, launcher_cfg: Dict[str, Any]):
        self.mods = list()
        self.modsByID = dict()
        self.modsByModule = dict()

        version_dir = launcher_cfg["versionDir"]
        self.__mods = os.listdir("../../mods/"+launcher_cfg["versionDir"])

        self.bubbles = dict()
        self.events = dict()
        self.items = dict()

        for index in self.__mods:
            self.mods.append(__import__("mods."+version_dir+"."+index+".__main__", fromlist=["__main__"]).Initialize())
            self.modsByID[self.mods[-1].ID] = self.mods[-1]
            self.modsByModule[self.mods[-1]] = self.mods[-1].ID
            print(self.mods[-1].__dict__.keys())

    def pre_initialize(self, parent):
        for mod in self.mods:
            mod.pre_initialize(parent)

            if "events" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.events:
                    self.events[self.modsByModule[mod]] = tuple(
                        list(self.events[self.modsByModule[mod]]) + list(mod.events))
                else:
                    self.events[self.modsByModule[mod]] = mod.events
            if "items" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.items:
                    self.items[self.modsByModule[mod]] = tuple(
                        list(self.items[self.modsByModule[mod]]) + list(mod.items))
                else:
                    self.items[self.modsByModule[mod]] = mod.items
            if "bubbles" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.bubbles:
                    self.bubbles[self.modsByModule[mod]] = tuple(
                        list(self.bubbles[self.modsByModule[mod]]) + list(mod.bubbles))
                else:
                    self.bubbles[self.modsByModule[mod]] = mod.bubbles

    def post_initialize(self, parent):
        for mod in self.mods:
            mod.post_initalize(parent)
