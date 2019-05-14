import os
from typing import *


class Loader:
    def __init__(self, launcher_cfg: Dict[str, Any]):
        self.mods = []
        version_dir = launcher_cfg["versionDir"]
        self.__mods = os.listdir("../../mods/"+launcher_cfg["versionDir"])
        for index in self.__mods:
            __import__("mods."+version_dir)

    def pre_initialize(self):
        pass

    def post_initialize(self):
