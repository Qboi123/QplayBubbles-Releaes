import os
import sys
from typing import Dict, Callable

from threadsafe_tkinter import Tk

from lib import registry
from lib.base import Accent
from lib.init import Init
from lib.slots import SlotsMenu
from lib.title import TitleMenu
from lib.utils.get_set import set_root


class RootWindow(Tk):
    def __init__(self, launcher_cfg: Dict, start_command: Callable):
        super(RootWindow, self).__init__()

        self.startCommand = start_command

        self.launcherConfig = launcher_cfg

        if launcher_cfg["debug"] is True:
            self.DEBUG = True
        if self.DEBUG is True:
            self.gameversion_dir = os.getcwd()
        else:
            self.gameversion_dir = os.path.abspath(
                os.path.join(os.getcwd(), "../../versions", self.launcherConfig["versionDir"]))
        set_root(self)
        self.wm_attributes("-fullscreen", True)
        self.registry = registry

        self.init = Init(self.registry, self.launcherConfig)

        self.version = self.launcherConfig["version"]
        self.versionDir = self.launcherConfig["versionDir"]
        self.gameBuild = self.launcherConfig["build"]

        self.accent = Accent("gold")

        self.init.pre_initialize()
        self.init.initialize()
        self.init.post_initialize()

        self.update()
        self.update_idletasks()
        self.titleChoice = TitleMenu().get()
        self.active = True

        while self.active:
            if self.titleChoice == "start":
                self.slotsMenu = SlotsMenu(self.startCommand, self.return_title)
            elif self.titleChoice == "quit":
                print("Quit")
                self.active = False
            elif self.titleChoice == "options":
                self.titleChoice = TitleMenu().get()
                self.active = True
                continue
            else:
                sys.exit(0)
        sys.exit(0)

    def return_title(self, slots_menu: SlotsMenu):
        from .title import TitleMenu
        slots_menu.destroy()
        self.titleChoice = TitleMenu().get()
