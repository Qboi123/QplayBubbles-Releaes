import os
import string
from inspect import isclass, getfile
from typing import Optional
from zipimport import zipimporter

from qbubbles.globals import GAME_VERSION
from qbubbles.registry import Registry

MODS = []


def Mod(modid, name, version, qbversion=GAME_VERSION):
    for character in modid:
        if character not in string.ascii_letters:
            raise ValueError(f"Invalid character of modid {repr(modid)}: '{character}' must be a ASCII letter")

    def decorator(func):
        if not isclass(func):
            raise TypeError(f"Object '{func.__name___}' is not a class")
        if qbversion == GAME_VERSION:
            # MODS.append(dict(modid=modid, name=name, version=version, func=func))
            Registry.register_modobject(modid=modid, name=name, version=version, func=func)
            func.modID = modid
            func.name = name
            func.fpath = getfile(func)
            func.modPath = os.path.split(func.fpath)[0]
            func.version = version
            func.zipimport = None
    return decorator


class ModSkeleton(object):
    modID: str
    name: str
    version: str
    fpath: str
    modPath: str
    zipimport: Optional[zipimporter]

    def __repr__(self):
        return f"Mod(<{self.modID}>)"


# @Mod(modid="examplemod", name="Example Mod", version="1.0.0")
# class ExampleMod(ModSkeleton):
#     def __init__(self):
#         print("Loaded mod 'ExampleMod'")
#
#     # def pre_initialize(self, evt: PreInitializeEvent):
#     #     pass
#     #
#     # def initialize(self, evt: InitializeEvent):
#     #     pass
#     #
#     # def post_initialize(self, evt: PostInitializeEvent):
#     #     pass
#
#
# @Mod(modid="examplemod", name="Example Mod", version="1.0.0")
# class ExampleMod2(ModSkeleton):
#     def __init__(self):
#         print("Loaded mod 'ExampleMod'")


if __name__ == '__main__':
    print(MODS)
    for mod in MODS:
        mod_object = mod["func"]()
        print(mod_object.modID)
