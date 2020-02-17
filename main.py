from background import Background
from menus.titleMenu import TitleMenu
from nzt import NZTFile

if __name__ == "__main__":
    print("Error: Can't open this file. Please open the game with the launcher.")
    input()
    exit(1)

import json
# import neural_net as nn

from time import sleep

from ammo import *
from base import Ammo
from bubble import Collision, create_bubble, place_bubble
from components import *
from extras import Logging, refresh, shuffling
from special import ScrolledWindow
from teleport import *

import sys

launcher_config = {"version": "v1.5.0-pre1",
                "versionDir": "v1_5_0_pre1",
                "launcher": None,
                "args": sys.argv
                   }

FatalError = Exception

ModRequirementInvalid = FatalError
ClassRequirementInvalid = ModRequirementInvalid

log = Logging("logs", True, True)

log.info("<Root>", "Imports loading success")
log.info("<Root>", "Starting Game")


class Maintance:
    def __init__(self):
        pass

    @staticmethod
    def auto_save(save_name: str, game_stats: Dict[str, Any], bubble: Dict[str, Any]):
        """
        Saves the game. (For Auto-Save)
        """
        import config as cfg

        import os

        print(os.curdir)

        try:
            cfg.Writer("slots/" + save_name + "/game.nzt", game_stats.copy())
            cfg.Writer("slots/" + save_name + "/bubble.nzt", bubble.copy())
        except FileNotFoundError as e:
            print(e.args)
            print(e.filename)
            print(e.filename2)

    @staticmethod
    def auto_restore(save_name: str):
        """
        Restoring. (For Auto-Restore)
        """
        import config as cfg

        game_stats = cfg.Reader("slots/" + save_name + "/game.nzt").get_decoded()

        return game_stats

    @staticmethod
    def reset(save_name: str):
        """
        Resets the game fully
        """
        global laucher_config

        import config as cfg

        stats = cfg.Reader("versions/" + launcher_config["versionDir"] + "/config/reset.nzt").get_decoded()
        bubble = cfg.Reader("versions/" + launcher_config["versionDir"] + "/config/reset-bubble.nzt").get_decoded()

        cfg.Writer("slots/" + save_name + "/game.nzt", stats.copy())
        cfg.Writer("slots/" + save_name + "/bubble.nzt", bubble.copy())


# noinspection PyUnusedLocal,PyArgumentList,PyCallByClass
class Game(Canvas):
    def __init__(self, launcher_cfg: Dict[str, Any], start_time=0.0, already_opened=False):
        super().__init__()

        # Launcher Config
        self.launcher_cfg = launcher_cfg
        self.version = self.launcher_cfg["version"]
        self.versionDir = self.launcher_cfg["versionDir"]

        # Imports
        import config
        import os
        import yaml
        import mod_support as mods

        print("started Game")

        if not os.path.exists("mods/%s" % self.versionDir):
            os.makedirs("mods/%s" % self.versionDir)

        # Load Mods
        self.mod_loader = mods.Loader(launcher_cfg)

        print("started mods")

        # Define Empty Attributes for use with slots-menu
        self.item_info = None

        self.frame5 = None
        self.frame3 = None
        self.frame4 = None
        self.lang_lbl = None
        self.lang_selected = None
        self.lang_btn = None
        self.save = None
        self.frame2 = None
        self.add = None
        self.add_input = None
        self.main_f = None
        self.s_frame = None
        self.sw = None
        self.canv = None
        self.frame = None
        self.frames = []
        self.canvass = []
        self.buttons = []

        # Start variables for the game
        self.log = log
        self.returnmain = False

        # Startup
        self.root = self.master
        self.time1 = start_time
        self.cfg = Maintance()
        self.save_name = None

        # Stats
        self.stats = dict()
        self.xControl = dict()

        print("stats")

        # Sprites
        self.sprites = dict()
        self.sprites["byClass"] = dict()
        self.sprites["byID"] = dict()

        # Standard Temporaray variables
        self.temp = dict()
        self.temp["scorestate-save"] = 0
        self.temp["secure-save"] = 0
        self.temp["timebreak-save"] = 0
        self.temp["confusion-save"] = 0
        self.temp["slowmotion-save"] = 0
        self.temp["paralis-save"] = 0
        self.temp["shotspeed-save"] = 0
        self.temp["notouch-save"] = 0
        self.temp["special-level-save"] = 0
        self.temp["found-bubble"] = False

        # Modes
        self.modes = dict()
        self.modes["pause"] = False
        self.modes["cheater"] = False
        self.modes["window"] = False
        self.modes["store"] = False
        self.modes["teleport"] = False
        self.modes["present"] = False

        self.pressed = {"Up": False,
                        "Down": False,
                        "Left": False,
                        "Right": False,
                        }

        # Panels (top and bottom, the panels are for information)
        self.panels = dict()

        # Initialize Canvas
        self.canvas = Canvas

        # Icons and texts
        self.icons = dict()
        self.texts = dict()

        # Back- and foreground
        self.back = dict()
        self.fore = dict()

        self.config = config.Reader(
            "config/startup.nzt").get_decoded()

        fd = os.open("lang/" + self.config["Game"]["language"] + ".yaml", os.O_RDONLY | os.O_CREAT)
        self.lang = yaml.safe_load(os.read(fd, 4096).decode())

        os.close(fd)

        if self.config["Game"]["language"] == "tengwar":
            self.font = "Tengwar Annatar Regular"
            self.f_size = 0
        else:
            self.font = "Helvetica"
            self.f_size = -4

        # noinspection PyDictCreation
        self.commands = {"store": False, "present": False, "special-mode": False}
        self.commands["store"]: Union[bool, Store] = False
        self.commands["present"]: Union[bool, Present] = False
        self.commands["special-mode"]: Union[bool, SpecialMode] = False

        # Player-prites
        self.ship = dict()
        self.tp = dict()

        # Configuration
        self.config = config.Reader(
            "config/startup.nzt").get_decoded()

        # Bubble / bubble-info
        self.bub = dict()
        self.bub["normal"] = dict()
        self.bubbles = {"bub-id": list(), "bub-special": list(), "bub-action": list(), "bub-radius": list(),
                        "bub-speed": list(),
                        "bub-position": list(), "bub-hardness": list(), "bub-index": list(), "key-active": False}

        # Ammo id-dictionary
        self.ammo = {"ammo-id": list(), "ammo-radius": 5, "ammo-speed": list(), "ammo-position": list(),
                     "ammo-damage": list(), "retime": start_time}

        # Sets fullscreen if not
        if self.config["Game"]["fullscreen"]:
            self.root.wm_attributes("-fullscreen", True)

        self.root.update()

        # Config resolution / positions
        self.config["width"] = self.root.winfo_width()
        self.config["height"] = self.root.winfo_height()

        self.config["middle-x"] = self.config["width"] / 2
        self.config["middle-y"] = self.config["height"] / 2

        # Collision class
        self.Coll = Collision()

        title_menu = TitleMenu(self.root, self.font, self.f_size, self.config, self.lang, self.load)

        # if not already_opened:
        #     self.close = Button(self.root, text="X", fg="white", relief=FLAT, bg="#ff0000",
        #                         command=lambda: os.kill(os.getpid(), -1))
        #     self.close.pack(side=TOP, fill=X)

    def add_event(self, event):
        """
        The event handler for the "Add"-button.
        :param event:
        :return:
        """
        self.add_save()

    @staticmethod
    def copy(src: str, dist: str):
        """
        Copying a directory or file.
        :param src:
        :param dist:
        :return:
        """
        import os

        log.info("Game.copy", "Copying " + src + " to " + dist)
        fd = os.open(src, os.O_RDONLY)
        fd2 = os.open(dist, os.O_WRONLY | os.O_CREAT)
        a = os.read(fd, 8192)
        os.write(fd2, a)
        os.close(fd)
        os.close(fd2)

    def options(self):
        self.background.destroy()
        self.start_btn.destroy()
        self.quit_btn.destroy()
        self.options_btn.destroy()

        self.frame5 = Frame(self.root, bg="#5c5c5c")
        self.frame5.pack(fill=BOTH, expand=TRUE)

        self.frame3 = Frame(self.frame5, height=700, width=1000, bg="#5c5c5c")
        self.frame3.pack()

        self.frame4 = Frame(self.frame5, height=20, bg="#5c5c5c")
        self.frame4.pack(side=BOTTOM, fill=X)

        self.lang_lbl = Label(self.frame3, text=self.lang["options.language"], bg="#5c5c5c")
        self.lang_lbl.grid(row=0, column=0)

        self.lang_selected = StringVar(self.root)

        self.lang_btn = Menubutton(self.frame3, textvariable=self.lang_selected.set, bg="#3c3c3c", fg="#9c9c9c")
        self.lang_btn.grid(row=0, column=1)

        self.save = Button(self.frame4, text=self.lang["options.save"], width=7, command=self.options_save,
                           bg="#3c3c3c", fg="#9c9c9c")
        self.save.pack(side=RIGHT)

        import os
        import yaml

        a = os.listdir("lang/")
        b = []
        c = []
        self.lang_btn.menu = Menu(self.lang_btn, tearoff=0)
        self.lang_btn["menu"] = self.lang_btn.menu

        for i in a:
            file = open("lang/" + i, "r")
            b.append(yaml.unsafe_load(file)["options.name"])
            c.append(i)
            file.close()

        d = 0
        for i in range(len(b)):
            self.lang_btn.menu.add_checkbutton(label=b[i], command=lambda: self.lang_selected.set(c[i]))
            d += 1

    def options_save(self):
        import yaml

        file = open("lang/" + self.lang_selected.get(), "r")
        self.lang = yaml.safe_load(file)
        file.close()

        self.options_close()

    def options_close(self):
        self.frame5.destroy()

    def load(self, menu: TitleMenu):
        """
        This is the Slots Menu.

        Loading slots-menu.
        :return:
        """
        import os

        # Remove menu
        menu.destroy()

        # Log
        log.info("Game.load", "Loading...")

        # Getting list of slots.
        path = "slots/"
        try:
            index = os.listdir(path)
        except FileNotFoundError:
            os.makedirs(path, exist_ok=True)
            index = os.listdir(path)
        dirs = []
        for item in index:
            file_path = path + item

            if os.path.isdir(file_path):
                dirs.append(item)

        # Frame for adding slots.
        self.frame2 = Frame(bg="#5c5c5c")

        # Save add button
        self.add = Button(self.frame2, text=self.lang["slots.add"], relief=FLAT, bg="#7f7f7f", fg="white",
                          command=self.add_save, font=[self.font, 15 + self.f_size])
        self.add.pack(side=RIGHT, padx=2, pady=5)

        # Save add entry (input)
        self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT, font=("helvetica"))
        self.add_input.pack(side=LEFT, fill=X, expand=TRUE, padx=2, pady=5)
        self.add_input.bind("<Return>", self.add_event)

        # Update root GUI.
        self.root.update()

        # Packing the config frame for adding a slot.
        self.frame2.pack(side=BOTTOM, fill=X)

        # Main frame.
        self.main_f = Frame(self.root, background="#3c3c3c", height=self.root.winfo_height() - 100)
        self.main_f.pack(fill=BOTH, expand=True)

        # Slots frame.
        self.s_frame = Frame(self.main_f, height=self.main_f.winfo_height() - 100, width=700)
        self.s_frame.pack(fill=Y)

        # Scrollwindow for the slots frame
        self.sw = ScrolledWindow(self.s_frame, 700, self.root.winfo_height() + 0, expand=True, fill=BOTH)

        # Configurate the canvas from the scrollwindow
        self.canv = self.sw.canv
        self.canv.config(bg="#2e2e2e")

        # self.frame.
        self.frame = self.sw.scrollwindow
        self.frames = []

        # Defining the list of widgets
        self.canvass = []
        self.buttons = []

        # Getting the list of directories in the slots-folder.
        import os

        names = os.listdir("slots/")

        # Information variables for each slot.
        infos = {"dates": [], "score": [], "level": []}

        import time

        # Prepare info variables
        for i in names.copy():
            if not os.path.exists("slots/" + i + "/bubble.nzt"):
                names.remove(i)
                continue
            mtime = os.path.getmtime("slots/" + i + "/bubble.nzt")
            a = time.localtime(mtime)

            b = list(a)

            if a[4] < 10:
                b[4] = "0" + str(a[4])
            else:
                b[4] = str(a[4])
            if a[5] < 10:
                b[5] = "0" + str(a[5])
            else:
                b[5] = str(a[5])

            tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            infos["dates"].append(tme_var)

            a = Reader("slots/" + i + "/game.nzt").get_decoded()
            infos["score"].append(a["Player"]["score"])
            infos["level"].append(a["Player"]["level"])

        self.item_info = names

        # Define the index variable.
        i = 0

        # Startloop
        for name in names:
            self.frames.append(Frame(self.frame, height=200, width=700))
            self.canvass.append(Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()

            self.canvass[-1].create_text(10, 10, text=name, fill="gold", anchor=NW,
                                         font=("Helvetica", 26, "bold"))
            self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))
            self.canvass[-1].create_text(240, 50, text="Level: " + str(infos["level"][i]), fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))
            self.canvass[-1].create_text(370, 50, text="Score: " + str(infos["score"][i]), fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))

            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.open"], bg="#afafaf", width=7,
                       font=[self.font, 15 + self.f_size]))
            self.buttons.copy()[-1].place(x=675, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", lambda event: self.open(event))

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.rename"], bg="#afafaf", width=7,
                       font=[self.font, 15 + self.f_size]))
            self.buttons.copy()[-1].place(x=600, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.rename)

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.remove"], bg="#afafaf", width=7,
                       font=[self.font, 15 + self.f_size]))
            self.buttons.copy()[-1].place(x=525, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.remove)

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.reset"], bg="#afafaf", width=7,
                       font=[self.font, 15 + self.f_size]))
            self.buttons.copy()[-1].place(x=450, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.reset_save)

            self.frames[-1].grid(row=i)

            i += 1

        # Using this so the program doesn't exit automaticly
        self.root.mainloop()

    def reset_save(self, event):
        import os

        # Getting row-index.
        y = event.widget.master.grid_info()["row"]

        # Getting source dir.
        src = self.item_info[y]

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("slots/" + src)

        # Disabling the input and the button.
        self.add_input.config(state=DISABLED)
        self.add.config(state=DISABLED)

        # Getting the input text.
        if src in ("aux", "con", ".", ".."):
            return

        # Creating dir for the game.
        os.makedirs("slots/" + src, exist_ok=True)

        game_data = {"Player": {"Money": {"diamonds": 0, "coins": 0},
                                "ShipStats": {"ship-speed": 10, "ShipPosition": [960, 540]},
                                "Abilities": {"teleports": 0, "level-score": 10000},
                                "lives": 7, "score": 0, "high-score": 0, "teleports": 0, "level": 1},
                     "BubbleStats": {"bubspeed": 5},
                     "Effects": {"confusion": False, "confusion-time": 0, "notouch": False, "notouch-time": 0,
                                 "paralis": False, "paralis-time": 0, "scorestate": 1, "scorestate-time": 0,
                                 "secure": False, "secure-time": 0, "shotspeed": 0.1, "shotspeed-time": 0,
                                 "slowmotion": False, "slowmotion-time": 0, "special-level": False, "special-level-time": 0,
                                 "speedboost": False, "speedboost-time": 0, "timebreak": False, "timebreak-time": 0}}

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile("slots/" + src + "/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        game_data_file = NZTFile("slots/" + src + "/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()

        # Refreshing slots-menu
        self.delete_all()
        self.load()

    def add_save(self):
        """
        Adding a slot to your game.
        :return:
        """
        import os

        if len(os.listdir("slots/")) <= 4000:
            # Disabling the input and the button.
            self.add_input.config(state=DISABLED)
            self.add.config(state=DISABLED)

            # Getting the input text.
            new = self.add_input.get()
            if (new in ("aux", "con", "num", "..")) or (len(new) < 3) or (new.lower() in [f.lower() for f in os.listdir("slots/")]):
                return

            # Creating dir for the game.
            os.makedirs("slots/" + new, exist_ok=True)

            game_data = {"Player": {"Money": {"diamonds": 0, "coins": 0},
                                    "ShipStats": {"ship_speed": 10, "ShipPosition": [960, 540]},
                                    "Abilities": {"teleports": 0, "level-score": 10000},
                                    "lives": 7, "score": 0, "high_score": 0, "teleports": 0, "level": 1},
                         "BubbleStats": {"bubspeed": 5},
                         "Effects": {"confusion": False, "confusion_time": 0, "notouch": False, "notouch_time": 0,
                                     "paralis": False, "paralis_time": 0, "scorestate": 1, "scorestate_time": 0,
                                     "secure": False, "secure_time": 0, "shotspeed": 0.1, "shotspeed_time": 0,
                                     "slowmotion": False, "slowmotion_time": 0, "special_level": False,
                                     "special_level_time": 0,
                                     "speedboost": False, "speedboost_time": 0, "timebreak": False,
                                     "timebreak_time": 0}}

            bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                           "bub-position": [], "bub-index": [], "key-active": False}

            game_data_file = NZTFile("slots/" + new + "/game.nzt", "w")
            game_data_file.data = game_data
            game_data_file.save()
            game_data_file.close()

            game_data_file = NZTFile("slots/" + new + "/bubble.nzt", "w")
            game_data_file.data = bubble_data
            game_data_file.save()
            game_data_file.close()

            # Refresh slots-menu
            self.delete_all()
            self.load()

    # noinspection PyTypeChecker
    def remove(self, event):
        import os

        # Getting row-index.
        y = event.widget.master.grid_info()["row"]

        # Getting source dir.
        src = self.item_info[y]

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("slots/" + src)

        # Refreshing slots-menu
        self.delete_all()
        self.load()

    def rename(self, event):
        import os

        # Getting row-index.
        y = event.widget.master.grid_info()["row"]

        # Getting source dir.
        src = self.item_info[y]

        # Getting new name.
        new = self.add_input.get()

        # noinspection PyTypeChecker
        # Rename the dir for the slot.
        os.rename("slots/" + src, "slots/" + new)

        # Refreshing slots-menu
        self.delete_all()
        self.load()

    def open(self, event):
        # Getting row-index
        y = event.widget.master.grid_info()["row"]

        # Getting source dir.
        src = self.item_info[y]

        # Remove slots menu and run the game.
        self.delete_all()
        self.run(src)

    def delete_all(self):
        # Delete all main frames
        self.main_f.destroy()
        self.frame2.destroy()

    def run(self, save_name):
        # Getting save-name and copy this in the self.
        self.save_name = save_name

        # Reload stats with the reader.
        self.stats = Reader("slots/" + self.save_name + "/game.nzt").get_decoded()

        # Create canvas.
        self.canvas = Canvas(self.root, height=self.config["height"], width=self.config["width"], highlightthickness=0)
        self.canvas.pack(expand=TRUE)

        # Run the main method (function).
        self.main()

    def resize(self, event):
        # Reload config resolution.
        self.config["height"] = event.height
        self.config["width"] = event.width

    def return_main(self):
        # Returning to title menu.
        Maintance().auto_save(self.save_name, self.stats, self.bubbles)
        self.returnmain = True
        try:
            self.t_auto_save.stop()
        except AttributeError:
            pass
        sleep(2)
        self.canvas.destroy()
        self.__init__(self.launcher_cfg, time(), True)

    def _movent(self):
        if (not self.modes["teleport"]) and (not self.modes["store"]) and (not self.modes["window"]):
            if not self.modes["pause"]:
                if not self.stats["Effects"]["paralyse"]:
                    x, y = get_coords(self.canvas, self.ship["id"])
                    if self.stats["Effects"]["speedboost"]:
                        a = 6
                    else:
                        a = 1
                    if self.pressed['Up']:
                        if y > 72 + self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0, (-self.stats["shipspeed"] / (self.move_fps / 4) - a))
                            self.root.update()
                    elif self.pressed['Down']:
                        if y < self.config["height"] - self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0, (self.stats["shipspeed"] / (self.move_fps / 4) + a))
                            self.root.update()
                    elif self.pressed['Left']:
                        if x > 0 + self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], (-self.stats["shipspeed"] / (self.move_fps / 4) - a), 0)
                            self.root.update()
                    elif self.pressed['Right']:
                        if x < self.config["width"] - self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], (self.stats["shipspeed"] / (self.move_fps / 4) + a), 0)
                            self.root.update()
                    self.stats["ship-position"] = get_coords(self.canvas, self.ship["id"])

    def movent_change(self):
        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.move_fps = 1
            time2 = time()
            Thread(None, lambda: self._movent()).start()
            sleep(0.01)
            
    def _xbox_input(self):
        time2 = time()
        while not self.returnmain:
            self.xbox.update()
            a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
            b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
            self.xControl["LeftJoystick"] = a
            self.xControl["RightJoystick"] = b
            self.xControl["A"] = bool(self.xbox.A)
            self.xControl["B"] = bool(self.xbox.B)
            self.xControl["X"] = bool(self.xbox.X)
            self.xControl["Y"] = bool(self.xbox.Y)
            self.xControl["Start"] = bool(self.xbox.Start)
            self.xControl["Back"] = bool(self.xbox.Back)
            self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
            self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
            self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
            self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)
            
    def xboxDeamon(self):
        time2 = time()
        while not self.returnmain:
            time1 = time()

            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.move_fps = 1
            time2 = time()
            Thread(None, lambda: self.xMovent()).start()
            sleep(0.01)
            
    def xMovent(self):
        if self.modes["present"]:
            if self.xControl["A"]:
                if False != self.commands["present"] != True:
                    self.commands["present"].exit(self.canvas)
                    self.modes["pause"] = False
                    self.modes["present"] = False
                    self.stats["Effects"]["scorestate-time"] = self.temp["scorestate-save"] + time()
                    self.stats["Effects"]["secure-time"] = self.temp["secure-save"] + time()
                    self.stats["Effects"]["timebreak-time"] = self.temp["timebreak-save"] + time()
                    self.stats["Effects"]["confusion-time"] = self.temp["confusion-save"] + time()
                    self.stats["Effects"]["slowmotion-time"] = self.temp["slowmotion-save"] + time()
                    self.stats["Effects"]["paralyse-time"] = self.temp["paralis-save"] + time()
                    self.stats["Effects"]["shotspeed-time"] = self.temp["shotspeed-save"] + time()
                    self.stats["Effects"]["notouch-time"] = self.temp["notouch-save"] + time()

        if (not self.modes["teleport"]) and (not self.modes["store"]) and (not self.modes["window"]):
            if not self.modes["pause"]:
                if not self.stats["Effects"]["paralyse"]:
                    x, y = get_coords(self.canvas, self.ship["id"])
                    if self.stats["Effects"]["speedboost"]:
                        a = 6
                    else:
                        a = 1

                    self.canvas.move(self.ship["id"],
                                     ((self.stats["shipspeed"] / (self.move_fps / 4) + a)) * self.xControl[
                                         "LeftJoystick"][0] / 7,
                                     -(((self.stats["shipspeed"] / (self.move_fps / 4) + a)) * self.xControl[
                                         "LeftJoystick"][1] / 7))

                    # if self.xControl['Up']:
                    #     if y > 72 + self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], 0, (-self.stats["shipspeed"] / (self.move_fps / 4) - a))
                    #         self.root.update()
                    # elif self.xControl['Down']:
                    #     if y < self.config["height"] - self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], 0, (self.stats["shipspeed"] / (self.move_fps / 4) + a))
                    #         self.root.update()
                    # elif self.xControl['Left']:
                    #     if x > 0 + self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], (-self.stats["shipspeed"] / (self.move_fps / 4) - a), 0)
                    #         self.root.update()
                    # elif self.xControl['Right']:
                    #     if x < self.config["width"] - self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], (self.stats["shipspeed"] / (self.move_fps / 4) + a), 0)
                    #         self.root.update()
                    # self.stats["ship-position"] = get_coords(self.canvas, self.ship["id"])

    def _press(self, e):
        if e.keysym == "Up":
            self.pressed["Up"] = True
        if e.keysym == "Down":
            self.pressed["Down"] = True
        if e.keysym == "Left":
            self.pressed["Left"] = True
        if e.keysym == "Right":
            self.pressed["Right"] = True

    def _release(self, e):
        if e.keysym == "Up":
            self.pressed["Up"] = False
        if e.keysym == "Down":
            self.pressed["Down"] = False
        if e.keysym == "Left":
            self.pressed["Left"] = False
        if e.keysym == "Right":
            self.pressed["Right"] = False

    def up_press(self, event):
        self.pressed["Up"] = True

    def down_press(self, event):
        self.pressed["Down"] = True

    def left_press(self, event):
        self.pressed["Left"] = True

    def right_press(self, event):
        self.pressed["Right"] = True

    def up_release(self, event):
        self.pressed["Up"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if y > 72 + 5:
                self.canvas.move(self.tp["id1"], 0, -5)
                self.canvas.move(self.tp["id2"], 0, -5)
                self.canvas.move(self.tp["id3"], 0, -5)
                self.canvas.move(self.tp["id4"], 0, -5)
        if self.modes["store"]:
            if event.keysym == "Up":
                self.commands["store"].set_selected(self.canvas, -1)
            if event.keysym == "Right":
                self.commands["store"].set_selected(self.canvas, int((self.config["height"] - 215) / 140 + 1))

    def down_release(self, event):
        self.pressed["Down"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if y < self.config["height"] - 105 - 5:
                self.canvas.move(self.tp["id1"], 0, 5)
                self.canvas.move(self.tp["id2"], 0, 5)
                self.canvas.move(self.tp["id3"], 0, 5)
                self.canvas.move(self.tp["id4"], 0, 5)
        if self.modes["store"]:
            self.commands["store"].set_selected(self.canvas, 1)

    def left_release(self, event):
        self.pressed["Left"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if x > 0 + 5:
                self.canvas.move(self.tp["id1"], -5, 0)
                self.canvas.move(self.tp["id2"], -5, 0)
                self.canvas.move(self.tp["id3"], -5, 0)
                self.canvas.move(self.tp["id4"], -5, 0)
        if self.modes["store"]:
            self.commands["store"].set_selected(self.canvas, int(-((self.config["height"] - 215) / 140 + 1)))

    def right_release(self, event):
        self.pressed["Right"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if x < self.config["width"] - 5:
                self.canvas.move(self.tp["id1"], 5, 0)
                self.canvas.move(self.tp["id2"], 5, 0)
                self.canvas.move(self.tp["id3"], 5, 0)
                self.canvas.move(self.tp["id4"], 5, 0)
        if self.modes["store"]:
            self.commands["store"].set_selected(self.canvas, int((self.config["height"] - 215) / 140 + 1))

    def shot(self, event):
        if (not self.modes["teleport"]) and (not self.modes["store"]) and (not self.modes["window"]):
            if not self.modes["pause"]:
                if not self.stats["Effects"]["paralyse"]:
                    if event.keysym == "space":
                        # noinspection PyTypeChecker
                        create_shot(self.canvas, self.ammo, self.config, self.ship, self.stats)

    def auto_save(self):
        while not self.returnmain:
            Maintance.auto_save(self.save_name, self.stats, self.bubbles)
            print(self.returnmain)
            sleep(2)

    def update(self):
        self.canvas.tag_raise(self.ship["id"])
        if not self.stats["Effects"]["timebreak"]:
            if len(self.bubbles["bub-id"]) < self.config["Bubble"]["max-amount"]:
                if not self.stats["Effects"]["special-level"]:
                    Thread(None,
                           lambda: create_bubble(self.stats, self.config, self.bub, self.canvas,
                                                 self.bubbles),
                           name="CreateBubbleThread").start()
                else:
                    Thread(None, lambda: SpecialMode().create_bubble(self.canvas, self.config,
                                                                     self.bubbles, self.stats,
                                                                     self.bub),
                           name="SpecialModeCreateBubbleThread").start()
        if self.commands["present"] is True:
            # noinspection PyTypeChecker
            self.commands["present"] = Present(self.canvas, self.stats, self.temp, self.modes,
                                               self.config, self.icons, self.fore, self.log, self.font)
        if self.commands["special-mode"] is True:
            State.set_state(self.canvas, log, self.stats, "SpecialLevel", self.back)
            self.commands["special-mode"] = False
        Collision().check_collision(self.root, self.commands, self.bubbles, self.config,
                                    self.stats,
                                    self.ammo,
                                    self.ship, self.canvas, log, self.back,
                                    self.texts, self.panels)
        Thread(None, lambda: refresh(self.stats, self.config, self.bubbles, self.bub, self.canvas,
                                     self.back, self.texts, self.modes, self.panels),
               name="RefreshThread").start()
        for events in self.mod_loader.events.values():
            for event in events:
                event.on_update(self)

    def t_update(self):
        # print(self.mod_loader.events)
        for events in self.mod_loader.events.values():
            for event in events:
                Thread(None, lambda: event.on_t_update(self)).start()

    def r_update(self):
        self.update()
        Thread(None, lambda: self.t_update(), "UpdateThread")

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        from threading import Thread
        from lib import xbox

        print("[Game]:", "Starting XboxController")
        self.xbox = xbox.XboxController()
        print("[Game]:", "Started XboxController")

        self.xControl = dict()

        a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        self.xControl["LeftJoystick"] = a
        self.xControl["RightJoystick"] = b
        self.xControl["A"] = bool(self.xbox.A)
        self.xControl["B"] = bool(self.xbox.B)
        self.xControl["X"] = bool(self.xbox.X)
        self.xControl["Y"] = bool(self.xbox.Y)
        self.xControl["Start"] = bool(self.xbox.Start)
        self.xControl["Back"] = bool(self.xbox.Back)
        self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)
        t0 = self.canvas.create_rectangle(0, 0, self.config["width"], self.config["height"], fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(self.config["middle-x"], self.config["middle-y"] - 30,
                                     text="Loading...",
                                     font=(self.font, 50 + self.f_size), fill="#afafaf")
        t2 = self.canvas.create_text(self.config["middle-x"], self.config["middle-y"] + 20,
                                     text="Loading Mods",
                                     font=(self.font, 15 + self.f_size), fill="#afafaf")
        self.canvas.update()

        # Pre-Initialize
        self.mod_loader.pre_initialize(self)

        self.canvas.itemconfig(t1, text="Loading...")
        self.canvas.itemconfig(t2, text="Loading Config")
        self.canvas.update()

        # Reload config resolution.
        self.config["height"] = self.canvas.winfo_height()
        self.config["width"] = self.canvas.winfo_width()

        # Copy self.canvas into c.
        c = self.canvas

        # Reload middle positions.
        mid_x = self.config["width"] / 2
        mid_y = self.config["height"] / 2

        self.canvas.itemconfig(t1, text="Loading Bubbles")
        self.canvas.itemconfig(t2, text="Creating Dicts")
        self.canvas.update()

        # Adding the dictionaries for the bubbles. With different res.
        self.bub["Normal"] = dict()
        self.bub["Triple"] = dict()
        self.bub["Double"] = dict()
        self.bub["Kill"] = dict()
        self.bub["SpeedUp"] = dict()
        self.bub["SpeedDown"] = dict()
        self.bub["Ultimate"] = dict()
        self.bub["Up"] = dict()
        self.bub["Teleporter"] = dict()
        self.bub["SlowMotion"] = dict()
        self.bub["DoubleState"] = dict()
        self.bub["Protect"] = dict()
        self.bub["ShotSpdStat"] = dict()
        self.bub["HyperMode"] = dict()
        self.bub["TimeBreak"] = dict()
        self.bub["Confusion"] = dict()
        self.bub["Paralis"] = dict()
        self.bub["StoneBub"] = dict()
        self.bub["NoTouch"] = dict()
        self.bub["Key"] = dict()
        self.bub["Diamond"] = dict()
        self.bub["Present"] = dict()
        self.bub["SpecialKey"] = dict()
        from lib import utils

        _min = 21
        _max = 80

        # Adding the different resolutions to the bubbles.
        for i in range(_min, _max + 1):
            self.bub["Normal"][i] = utils.createbubble_image((i, i), None, "white")
            self.bub["Double"][i] = utils.createbubble_image((i, i), None, "gold")
            self.bub["Triple"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
            self.bub["SpeedDown"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
            self.bub["SpeedUp"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
            self.bub["Up"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
            self.bub["Ultimate"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
            self.bub["Kill"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000",)
            self.bub["Teleporter"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
            self.bub["SlowMotion"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
            self.bub["DoubleState"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
            self.bub["Protect"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
            self.bub["ShotSpdStat"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
            self.bub["HyperMode"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
            self.bub["TimeBreak"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
            self.bub["Confusion"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
            self.bub["Paralis"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
            self.bub["StoneBub"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
            self.bub["NoTouch"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")

            self.canvas.itemconfig(t1, text="Loading Bubbles Sizes")
            self.canvas.itemconfig(t2, text="Loading %s of %s" % (i - _min, _max - 1 - _min))
            self.canvas.update()

        # Adding the static-resolution-bubbles.
        self.bub["Key"][60] = PhotoImage(file="assets/bubbles/Key.png")
        self.bub["Diamond"][36] = PhotoImage(
            file="assets/bubbles/Diamond.png")
        self.bub["Present"][40] = PhotoImage(
            file="assets/bubbles/Present.png")
        # noinspection PyTypeChecker
        self.bub["Coin"] = PhotoImage(file="assets/CoinBub.png")
        self.bub["SpecialKey"][48] = PhotoImage(
            file="assets/bubbles/SpecialMode.png")

        for i in self.bub.keys():
            print("%s: %s" % (i, self.bub[i]))

        # Adding ship image.
        self.ship["image"] = PhotoImage(file="assets/Ship.png")

        # Reload stats with auto-restore.
        self.stats = Maintance().auto_restore(self.save_name)

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Normal")
        self.canvas.update()

        # Getting the normal background.
        self.back["normal"] = PhotoImage(file="assets/BackGround.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="")
        self.canvas.update()

        # Getting the store-icons.
        self.icons["store-pack"] = list()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/Key.png"))
        self.canvas.itemconfig(t2, text="Store Item: Key")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/Teleport.png"))
        self.canvas.itemconfig(t2, text="Store Item: Teleport")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/Shield.png"))
        self.canvas.itemconfig(t2, text="Store Item: Shield")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/DiamondBuy.png"))
        self.canvas.itemconfig(t2, text="Store Item: Diamond")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/BuyACake.png"))
        self.canvas.itemconfig(t2, text="Store Item: Buy A Cake")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/Pop_3_bubs.png"))
        self.canvas.itemconfig(t2, text="Store Item: Pop 3 Bubbles")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/PlusLife.png"))
        self.canvas.itemconfig(t2, text="Store Item: PlusLife")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/SpeedBoost.png"))
        self.canvas.itemconfig(t2, text="Store Item: Speedboost")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/SpecialMode.png"))
        self.canvas.itemconfig(t2, text="Store Item: Special Mode")
        self.canvas.update()
        self.icons["store-pack"].append(
            PhotoImage(file="assets/Images/StoreItems/DoubleScore.png"))
        self.canvas.itemconfig(t2, text="Double Score")
        self.canvas.update()
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Line")
        self.canvas.update()
        # Unknown
        self.back["line"] = PhotoImage(file="assets/LineIcon.png")

        self.canvas.itemconfig(t1, text="Loading Foreground")
        self.canvas.itemconfig(t2, text="For Bubble Gift")
        self.canvas.update()

        # Setting present foreground
        self.fore["present-fg"] = PhotoImage(
            file="assets/EventBackground.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Circle")
        self.canvas.update()

        # Setting present icons.
        self.icons["circle"] = PhotoImage(file="assets/Circle.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Present")
        self.canvas.update()

        self.icons["present"] = PhotoImage(file="assets/Present.png")

        self.canvas.itemconfig(t1, text="Loading Foreground")
        self.canvas.itemconfig(t2, text="Store FG")
        self.canvas.update()

        # Setting store foreground
        self.fore["store-fg"] = PhotoImage(file="assets/FG2.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Store: Diamond & Coin")
        self.canvas.update()

        # Setting standard store icons.
        self.icons["store-diamond"] = PhotoImage(
            file="assets/Diamond.png")
        self.icons["store-coin"] = PhotoImage(file="assets/Coin.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Pause")
        self.canvas.update()

        # Setting pause-icon.
        self.icons["pause-id"] = PhotoImage(file="assets/Pause.png")

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="SlowMotion")
        self.canvas.update()

        # Setting slowmotion-icon.
        self.icons["slowmotion"] = PhotoImage(
            file="assets/SlowMotionIcon.png")

        self.canvas.itemconfig(t1, text="Loading Background")
        self.canvas.itemconfig(t2, text="Special")
        self.canvas.update()

        # Setting special background.
        self.back["special"] = PhotoImage(
            file="assets/Images/Backgrounds/GameBG Special2.png")

        # Setting normal background.
        self.back["normal"] = PhotoImage(
            file="assets/Images/Backgrounds/GameBG2.png")
        self.canvas.itemconfig(t2, text="Normal")
        self.canvas.update()

        # Setting background from nothing to normal.
        self.back["id"] = self.canvas.create_image(0, 0, anchor=NW, image=self.back["normal"])

        # Creating shi
        self.ship["id"] = c.create_image(7.5, 7.5, image=self.ship["image"])
        print(self.ship["id"])

        # Moving ship to position
        c.move(self.ship["id"], self.stats["Player"]["ShipStats"]["ShipPosition"][0], self.stats["Player"]["ShipStats"]["ShipPosition"][1])

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        # Initializing the panels for the game.
        self.panels["game/top"] = self.canvas.create_rectangle(
            -1, -1, self.config["width"], 69, fill="darkcyan"
        )

        # Create seperating lines.
        self.canvas.create_line(0, 70, self.config["width"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, self.config["width"], 69, fill="white")

        c.create_text(55, 30, text=self.lang["info.score"], fill='orange', font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Score")
        c.create_text(110, 30, text=self.lang["info.level"], fill='orange', font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Level")
        c.create_text(165, 30, text=self.lang["info.speed"], fill='orange', font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Speed")
        c.create_text(220, 30, text=self.lang["info.lives"], fill='orange', font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Lives")
        c.create_text(330, 30, text=self.lang["info.state.score"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Score State")
        c.create_text(400, 30, text=self.lang["info.state.protect"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Protect")
        c.create_text(490, 30, text=self.lang["info.state.slowmotion"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Slow Motion")
        c.create_text(580, 30, text=self.lang["info.state.confusion"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Confusion")
        c.create_text(670, 30, text=self.lang["info.state.timebreak"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Time Break")
        c.create_text(760, 30, text=self.lang["info.state.spdboost"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        c.create_text(850, 30, text=self.lang["info.state.paralis"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Paralize")
        c.create_text(940, 30, text=self.lang["info.state.shotspeed"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        c.create_text(1030, 30, text=self.lang["info.state.notouch"], fill="gold", font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        c.create_text(1120, 30, text=self.lang["info.tps"], fill='gold', font=[self.font, 15 + self.f_size])
        self.canvas.itemconfig(t2, text="Teleports")
        c.create_image(1185, 30, image=self.icons["store-diamond"])
        self.canvas.itemconfig(t2, text="Diamonds")
        c.create_image(1185, 50, image=self.icons["store-coin"])
        self.canvas.itemconfig(t2, text="Coins")

        self.canvas.itemconfig(t1, text="Creating Stats Data")
        self.canvas.itemconfig(t2, text="")

        # Game information values.
        self.texts["score"] = c.create_text(55, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Score")
        self.texts["level"] = c.create_text(110, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Level")
        self.texts["speed"] = c.create_text(165, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Speed")
        self.texts["lives"] = c.create_text(220, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Lives")
        self.texts["scorestate"] = c.create_text(330, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Score")
        self.texts["secure"] = c.create_text(400, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Protection")
        self.texts["slowmotion"] = c.create_text(490, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Slowmotion")
        self.texts["confusion"] = c.create_text(580, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Confusion")
        self.texts["timebreak"] = c.create_text(670, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Time Break")
        self.texts["speedboost"] = c.create_text(760, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        self.texts["paralis"] = c.create_text(850, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Paralis")
        self.texts["shotspeed"] = c.create_text(940, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        self.texts["notouch"] = c.create_text(1030, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        self.texts["shiptp"] = c.create_text(1120, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = c.create_text(1210, 30, fill='cyan')
        self.canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = c.create_text(1210, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = c.create_text(mid_x, mid_y, fill='Orange', font=(self.font, 50 + self.f_size))
        self.canvas.itemconfig(t2, text="Level View")

        self.texts["pause"] = c.create_text(mid_x, mid_y, fill='Orange', font=(self.font, 60 + self.f_size, "bold"))
        self.canvas.itemconfig(t2, text="Pauze")
        self.icons["pause"] = c.create_image(mid_x, mid_y, image=self.icons["pause-id"], state=HIDDEN)
        self.canvas.itemconfig(t2, text="Pauze")

        # Threaded Automatic Save (TAS)
        # self.t_auto_save = StoppableThread(None, lambda: self.auto_save(), name="AutoSaveThread").start()

        kw = {}

        for i in Ammo.requires:
            if i in self.__dict__.keys():
                kw[i] = self.__dict__[i]
            else:
                raise ClassRequirementInvalid("Requirement \"%s\" of class Ammo is invalid." % i)

        self.c_ammo = Ammo()

        # Binding key-events for control
        self.canvas.itemconfig(t1, text="Binding Objects")
        self.canvas.itemconfig(t2, text="Main Binding")
        c.bind_all('<Key>',
                   lambda event: control(self.modes, self.config, self.root, self.canvas, self.stats, self.bubbles,
                                         self.back, self.texts, self.commands, self.temp, self.panels, self.fore,
                                         self.ship, self.tp, self.lang, self.return_main, self.icons,
                                         self.bub, self.font, event, self.c_ammo, self.launcher_cfg))

        self.canvas.itemconfig(t2, text="Player Motion")
        c.bind_all("<KeyPress-Up>", lambda event: self.up_press(event))
        c.bind_all("<KeyPress-Down>", lambda event: self.down_press(event))
        c.bind_all("<KeyPress-Left>", lambda event: self.left_press(event))
        c.bind_all("<KeyPress-Right>", lambda event: self.right_press(event))

        c.bind_all("<KeyRelease-Up>", lambda event: self.up_release(event))
        c.bind_all("<KeyRelease-Down>", lambda event: self.down_release(event))
        c.bind_all("<KeyRelease-Left>", lambda event: self.left_release(event))
        c.bind_all("<KeyRelease-Right>", lambda event: self.right_release(event))
        c.bind_all("<Key-Z>", lambda event: self.r_update())

        # Binding other key-events.
        c.bind_all('Configure', lambda event: self.resize)

        log.info("Game.main", "Key-bindings binded to 'move_ship'")
        if len(self.bubbles["bub-id"]) == 0:
            log.warning("Game.main", "Bubbel-ID lijst is gelijk aan lengte nul.")

        if len(self.bubbles["bub-action"]) == 0:
            log.warning("Game.main", "Bubble-actie lijst is gelijk aan lengte nul.")

        if len(self.bubbles["bub-speed"]) == 0:
            log.warning("Game.main", "Bubbel-snelheid lijst is gelijk aan lengte nul.")

        self.ammo["retime"] = time()

        stats = self.stats

        self.canvas.itemconfig(t1, text="Fixing Saved States")
        self.canvas.itemconfig(t2, text="")

        if stats["Effects"]["scorestate-time"] <= time():
            stats["Effects"]["scorestate"] = 1
            stats["Effects"]["scorestate-time"] = time()
        if stats["Effects"]["secure-time"] <= time():
            stats["Effects"]["secure"] = False
            stats["Effects"]["secure-time"] = time()
        if stats["Effects"]["slowmotion-time"] <= time():
            stats["Effects"]["slowmotion"] = False
            stats["Effects"]["slowmotion-time"] = time()
        if stats["Effects"]["timebreak-time"] <= time():
            stats["Effects"]["timebreak"] = False
            stats["Effects"]["timebreak-time"] = time()
        if stats["Effects"]["confusion-time"] <= time():
            stats["Effects"]["confusion"] = False
            stats["Effects"]["confusion-time"] = time()
        if stats["Effects"]["speedboost-time"] <= time():
            stats["Effects"]["speedboost"] = False
            stats["Effects"]["speedboost-time"] = time()
        if stats["Effects"]["paralyse-time"] <= time():
            stats["Effects"]["paralyse"] = False
            stats["Effects"]["paralyse-time"] = time()
        if stats["Effects"]["shotspeed-time"] <= time():
            stats["Effects"]["shotspeed"] = 0.1
            stats["Effects"]["shotspeed-time"] = time()
        if stats["Effects"]["special-level-time"] <= time():
            stats["Effects"]["special-level"] = False
            stats["Effects"]["special-level-time"] = time()
        else:
            self.canvas.itemconfig(self.back["id"], image=self.back["special"])
            self.canvas.itemconfig(self.panels["game/top"], fill="#3f3f3f")
        if stats["score"] < 0:
            log.error("Game.main", "The 'Score' variable under zero.")
            stats["score"] = 0
        if stats["score"] > stats["hiscore"]:
            stats["hiscore"] = stats["score"]
        if stats["Effects"]["confusion"] and not stats["Effects"]["secure"]:
            shuffling(self.bubbles)

        self.bubbles["active2"] = []
        self.bubbles["active"] = 0

        self.stats = self.cfg.auto_restore(self.save_name)

        start(self.bubbles, self.save_name, self.stats, self.config, self.bub, self.modes, self.canvas)

        Maintance.auto_save(self.save_name, self.stats, self.bubbles)

        global Mainloop
        Mainloop = False

        self.stats = stats

        # Post Initalize mods

        self.canvas.itemconfig(t1, text="Post Initialize Mods")
        self.canvas.itemconfig(t2, text="")
        self.mod_loader.post_initialize(self)

        height = self.config["height"]
        width = self.config["width"]

        a = randint(0, width)
        b = randint(0, width)
        c = randint(0, width)

        d = stats["ship-position"][0]

        e = 40

        if a + e < d or d > a - e:
            a = d - e
        if b + e < d or d > b - e:
            b = d - e - 20
        if c + e < d or d > c - e:
            c = d - e - 40

        # bariers = [BaseBarier(self), BaseBarier(self), BaseBarier(self)]
        # bariers[0].create(a, height / 2 + 72 / 2)
        # bariers[1].create(b, height / 2 + 72 / 2)
        # bariers[2].create(c, height / 2 + 72 / 2)

        c = self.canvas

        print("[XboxController]:", "Starting Daemons")

        Thread(None, lambda: self._xbox_input(), daemon=True).start()
        Thread(None, lambda: self.xboxDeamon(), daemon=True).start()
        Thread(None, lambda: self.movent_change(), "MotionThread").start()

        try:
            # MAIN GAME LOOP
            while True:
                # self.stats = self.cfg.auto_restore(self.save_name)
                while self.bubbles["active"] <= len(self.bubbles["bub-index"]) - 1:
                    self.canvas.itemconfig(t2, text="Created " + str(self.bubbles["active"]) + " of " + str(
                        len(self.bubbles["bub-index"]) - 1) + " active...")
                    self.canvas.update()
                    self.root.update()
                    sleep(0.1)

                self.canvas.delete(t0)
                self.canvas.delete(t1)
                self.canvas.delete(t2)

                while self.stats["lives"] > 0:
                    if not self.modes["pause"]:
                        self.update()
                        Thread(None, lambda: self.t_update()).start()

                    self.root.update()
                    self.root.update_idletasks()
                self.root.update()
                # for barier in bariers:
                #     barier.destroy()
                g1 = c.create_text(mid_x, mid_y, text='GAME OVER', fill='Red', font=('Helvetica', 60, "bold"))
                g2 = c.create_text(mid_x, mid_y + 60, text='Score: ' + str(self.stats["score"]), fill='white',
                                   font=('Helvetica', 30))
                g3 = c.create_text(mid_x, mid_y + 90, text='Level: ' + str(self.stats["level"]), fill='white',
                                   font=('Helvetica', 30))
                log.info("Game.main", "Game Over!")
                self.root.update()
                sleep(4)
                c.delete(g1)
                c.delete(g2)
                c.delete(g3)
                del g1, g2, g3
                Maintance().reset(self.save_name)
                self.return_main()
        except TclError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == 'can\'t invoke "update" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'can\'t invoke "update_idletasks" command: application has been destroyed':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    exit(0)
                elif e.args[0] == 'invalid command name ".!canvas"':
                    log.info('<root>', "Exit...")
                    exit(0)
                else:
                    print('TclError: ' + e.args[0] + "Line: " + str(e.__traceback__.tb_next.tb_lineno))
                    exit(1)
        except AttributeError as e:
            if self.returnmain:
                pass
            else:
                if e.args[0] == "self.tk_widget is None. Not hooked into a Tk instance.":
                    exit(0)
                else:
                    raise AttributeError(e.args[0])


class S:
    def __init__(self):
        self.inputs = []
        self.outputs = [[]]

    def save(self):
        with open("input.nzt", "w") as file:
            json_str = self.inputs
            json_inputs = json.encoder.JSONEncoder().encode(json_str)

        with open("output.nzt", "w") as file:
            json_str = self.outputs
            json_outputs = json.encoder.JSONEncoder().encode(json_str)
        #
        # neural_network = nn.NeuralNetwork()
        # print("Random synaptic weights: \n%s" % neural_network.synaptic_weights)
        #
        # self.training_inputs = np.array(json_inputs)
        #
        # self.training_outputs = np.array(json_outputs).T
        #
        # neural_network.train(self.training_inputs, self.training_outputs, 100000)
        #
        # print("Synaptic weights after training: \n%s" % neural_network.synaptic_weights)

    def update(self, input, output):
        print()
        print("> [player_x, player_y, player_r, bubble_x, bubble_y, bubble_r, bubble_bad")
        print("  %s = %s" % (input, output))
        self.inputs.append(input)
        self.outputs[0].append(output)


s = S()

if __name__ == "__main__":
    print("Error: Can't open this file. Please open this file with the launcher.")
