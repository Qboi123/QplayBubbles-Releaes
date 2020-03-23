import os
import shlex
import sys
from tkinter import Tk
from typing import Optional

from game import Game, default_launchercfg
from load import Load
from registry import Registry


class Main(Tk):
    def __init__(self):
        self.pre_run()
        super(Main, self).__init__()
        Registry.register_root(self)

        self.geometry("1920x1080")
        # self.after(30000, lambda: os.kill(os.getpid(), 0))

        # self.wm_protocol("WM_DELETE_WINDOW", ...)

        if "launcherConfig" not in Registry.gameData.keys():
            game_dir: Optional[str] = None
            for argv in sys.argv[1:]:
                if argv.startswith("gameDir="):
                    game_dir = argv[8:]
            if game_dir is None:
                raise RuntimeError("Argument 'gameDir' is not defined, Q-Bubbles cannot continue")
            Registry.gameData["launcherConfig"] = {"gameDir": game_dir}

        Registry.register_scene("LoadScreen", Load(Registry.get_root()))

        Load.scenemanager.change_scene("LoadScreen")

    def pre_run(self):
        if "--debug" in sys.argv:
            Registry.gameData["launcherConfig"] = default_launchercfg
            self.debug = True


if __name__ == '__main__':
    main = Main()
    main.mainloop()
