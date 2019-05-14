import os
from typing import *


class Loader:
    def __init__(self, launcher_cfg: Dict[str, Any]):
        self.mods = list()
        self.modsByID = dict()
        self.modsByModule = dict()
        version_dir = launcher_cfg["versionDir"]
        self.__mods = os.listdir("../../mods/"+launcher_cfg["versionDir"])
        for index in self.__mods:
            self.mods.append(__import__("mods."+version_dir+"."+index+".__main__", fromlist=["__main__"]).Initialize())
            self.modsByID[self.mods[-1].ID] = self.mods[-1]
            self.modsByModule[self.mods[-1]] = self.mods[-1].ID
            print(self.mods[-1].__dict__.keys())

    def pre_initialize(self, parent):
        for mod in self.mods:
            mod.pre_initialize(parent)

    def post_initialize(self, parent):
        for mod in self.mods:
            mod.post_initalize(parent)
