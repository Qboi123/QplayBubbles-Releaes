import os
from typing import *


class Loader:
    def __init__(self, launcher_cfg: Dict[str, Any], **kw):
        self.mods = list()
        self.modsByID = dict()
        self.modsByModule = dict()
        version_dir = launcher_cfg["versionDir"]
        self.__mods = os.listdir("mods/"+launcher_cfg["versionDir"])
        self.bubbles = dict()
        self.events = dict()
        self.items = dict()

        for index in self.__mods:
            self.mods.append(__import__("mods."+version_dir+"."+index+".__main__", fromlist=["__main__"]).Initialize())
            self.modsByID[self.mods[-1].ID] = self.mods[-1]
            self.modsByModule[self.mods[-1]] = self.mods[-1].ID
            print(self.mods[-1].__dict__.keys())

    def pre_initialize(self, **kw):
        for mod in self.mods:
            mod.PreInitialize(**kw)
            if "bubbles" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.bubbles:
                    self.bubbles[self.modsByModule[mod]] = self.bubbles[self.modsByModule[mod]]+mod.bubbles
                else:
                    self.bubbles[self.modsByModule[mod]] = mod.bubbles
            if "events" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.events:
                    self.events[self.modsByModule[mod]] = self.events[self.modsByModule[mod]]+mod.events
                else:
                    self.events[self.modsByModule[mod]] = mod.events
            if "items" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.items:
                    self.items[self.modsByModule[mod]] = self.items[self.modsByModule[mod]]+mod.items
                else:
                    self.items[self.modsByModule[mod]] = mod.items
            if "sprites" in mod.__dict__.keys():
                if self.modsByModule[mod] in self.items:
                    self.items[self.modsByModule[mod]] = self.items[self.modsByModule[mod]]+mod.items
                else:
                    self.items[self.modsByModule[mod]] = mod.items
        print(self.events)

    def post_initialize(self, parent):
        for mod in self.mods:
            mod.post_initialize(parent)
