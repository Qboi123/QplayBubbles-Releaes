import os
import re
import sys
import time
from ctypes import windll
from tkinter import Tk, Toplevel
from tkinter.messagebox import showerror
from typing import Optional, Callable

from game import default_launchercfg
from load import Load
from registry import Registry


class NewRoot(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)
        self.bind("<Map>", self.onRootDeiconify)
        self.bind("<Unmap>", self.onRootIconify)

    # toplevel follows root taskbar events (minimize, restore)
    def onRootIconify(self, evt):
        self.child.withdraw()

    def onRootDeiconify(self, evt):
        self.lower()
        self.iconify()
        self.child.deiconify()

    def bind_events(self, toplevel):
        self.child = toplevel


def get_hwnd_dpi(window_handle):
    # To detect high DPI displays and avoid need to set Windows compatibility flags
    import os
    if os.name == "nt":
        from ctypes import windll, pointer, wintypes
        windll.shcore.SetProcessDpiAwareness(1)
        DPI100pc = 96  # DPI 96 is 100% scaling
        DPI_type = 0  # MDT_EFFECTIVE_DPI = 0, MDT_ANGULAR_DPI = 1, MDT_RAW_DPI = 2
        winH = wintypes.HWND(window_handle)
        monitorhandle = windll.user32.MonitorFromWindow(winH, wintypes.DWORD(2))  # MONITOR_DEFAULTTONEAREST = 2
        X = wintypes.UINT()
        Y = wintypes.UINT()
        try:
            windll.shcore.GetDpiForMonitor(monitorhandle, DPI_type, pointer(X), pointer(Y))
            return X.value, Y.value, (X.value + Y.value) / (2 * DPI100pc)
        except Exception:
            return 96, 96, 1  # Assume standard Windows DPI & scaling
    else:
        return None, None, 1  # What to do for other OSs?


def tk_geometry_scale(s, cvtfunc):
    patt = r"(?P<W>\d+)x(?P<H>\d+)\+(?P<X>\d+)\+(?P<Y>\d+)"  # format "WxH+X+Y"
    R = re.compile(patt).search(s)
    G = str(cvtfunc(R.group("W"))) + "x"
    G += str(cvtfunc(R.group("H"))) + "+"
    G += str(cvtfunc(R.group("X"))) + "+"
    G += str(cvtfunc(R.group("Y")))
    return G


def make_tk_dpiaware(root: Tk):
    root.dpiX, root.dpiY, root.dpiScaling = get_hwnd_dpi(root.winfo_id())
    root.tkScale = lambda v: int(float(v) * root.dpiScaling)
    root.tkGeometryScale = lambda s: tk_geometry_scale(s, root.tkScale)


class Main(Tk):
    def __init__(self):
        # self.fakeRoot = NewRoot()
        #
        # self.pre_run()
        super(Main, self).__init__()  # self.fakeRoot)
        # self.fakeRoot.bind_events(self)

        self.dpiX: float
        self.dpiY: float
        self.dpiScaling: float
        self.tkScale: Callable
        self.tkGeometryScale: Callable

        make_tk_dpiaware(self)

        if self.dpiScaling != 1.0:
            self.wm_attributes("-alpha", 0.0)
            self.overrideredirect(1)
            showerror("Load Failure", f"This game is not compalible with DPI other than 100%:\n"
                                      f"Currently: {int(self.dpiScaling * 100)}%")
            os.kill(os.getpid(), 1)

        Registry.register_root(self)
        Registry.gameData["startTime"] = time.time()

        # self.wm_attributes("-topmost", True)
        self.overrideredirect(1)
        width = self.tkScale(self.winfo_screenwidth())
        self.geometry(self.tkGeometryScale(f"{width}x{self.winfo_screenheight()}+0+0"))
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
