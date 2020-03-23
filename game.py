import sys

from background import Background
from bubbleSystem import start
from utils import control

if __name__ == "__main__":
    if "--debug" in sys.argv:
        pass
    else:
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
from scenemanager import CanvasScene

import sys

default_launchercfg = {"version": "v1.5.0-pre1",
                       "versionDir": "v1_5_0_pre1"}

FatalError = Exception

ModRequirementInvalid = FatalError
ClassRequirementInvalid = ModRequirementInvalid

log = Logging("logs", True, True)

log.info("<Root>", "Imports loading success")
log.info("<Root>", "Starting Game")


def control(modes, config, root, canvas, stats, bubbles, back, texts, commands, temp, panels, fore, ship, tp, lang,
            return_main, icons, bub, font, event, c_ammo, laucher_cfg):
    """
    Ship-motion event
    :param laucher_cfg:
    :param c_ammo:
    :param font:
    :param bub:
    :param icons:
    :param ship:
    :param tp:
    :param lang:
    :param return_main:
    :param commands:
    :param fore:
    :param panels:
    :param temp:
    :param modes:
    :param config:
    :param root:
    :param canvas:
    :param stats:
    :param bubbles:
    :param back:
    :param texts:
    :param event:
    """

    if modes["store"] and commands["store"] is not None:
        if event.keysym == "Up":
            commands["store"].set_selected(canvas, -1)
        if event.keysym == "Down":
            commands["store"].set_selected(canvas, 1)
        if event.keysym == "Left":
            commands["store"].set_selected(canvas, int(-((config["height"] - 215) / 140 + 1)))
        if event.keysym == "Right":
            commands["store"].set_selected(canvas, int((config["height"] - 215) / 140 + 1))
        if event.keysym == "space":
            commands["store"].buy_selected(config, modes, log, root, canvas, stats, bubbles, back,
                                           texts,
                                           commands, temp, panels)
        if event.keysym == "BackSpace":
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
        if event.keysym == "Escape":
            sleep(1)
            commands["store"].exit(canvas, log, modes, stats, temp, commands)
            commands["store"] = None
    if modes["present"]:
        if event.keysym == "space":
            if False != commands["present"] != True:
                commands["present"].exit(canvas)
                modes["pause"] = False
                modes["present"] = False
                stats["scorestate_time"] = temp["scorestate-save"] + time()
                stats["secure_time"] = temp["secure-save"] + time()
                stats["timebreak_time"] = temp["timebreak-save"] + time()
                stats["confusion_time"] = temp["confusion-save"] + time()
                stats["slowmotion_time"] = temp["slowmotion-save"] + time()
                stats["paralyse_time"] = temp["paralyse-save"] + time()
                stats["shotspeed_time"] = temp["shotspeed-save"] + time()
                stats["notouch_time"] = temp["notouch-save"] + time()
    if modes["teleport"]:
        x, y = get_coords(canvas, tp["id1"])
        if event.keysym == 'Up':
            if y > 72 + 5:
                canvas.move(tp["id1"], 0, -5)
                canvas.move(tp["id2"], 0, -5)
                canvas.move(tp["id3"], 0, -5)
                canvas.move(tp["id4"], 0, -5)
        if event.keysym == "Down":
            if y < config["height"] - 105 - 5:
                canvas.move(tp["id1"], 0, 5)
                canvas.move(tp["id2"], 0, 5)
                canvas.move(tp["id3"], 0, 5)
                canvas.move(tp["id4"], 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                canvas.move(tp["id1"], -5, 0)
                canvas.move(tp["id2"], -5, 0)
                canvas.move(tp["id3"], -5, 0)
                canvas.move(tp["id4"], -5, 0)
        if event.keysym == "Right":
            if x < config["width"] - 5:
                canvas.move(tp["id1"], 5, 0)
                canvas.move(tp["id2"], 5, 0)
                canvas.move(tp["id3"], 5, 0)
                canvas.move(tp["id4"], 5, 0)
        if event.keysym == "BackSpace":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            modes["pause"] = False

            stats["scorestate_time"] = temp["scorestate-save"] + time()
            stats["secure_time"] = temp["secure-save"] + time()
            stats["timebreak_time"] = temp["timebreak-save"] + time()
            stats["confusion_time"] = temp["confusion-save"] + time()
            stats["slowmotion_time"] = temp["slowmotion-save"] + time()
            stats["paralyse_time"] = temp["paralyse-save"] + time()
            stats["shotspeed_time"] = temp["shotspeed-save"] + time()
            stats["notouch_time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
    elif event.keysym.lower() == "space":
        a = c_ammo()
        a.create(None, None)
    if event.keysym == "Escape" and (not modes["pause"]) and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and (not modes["cheater"]):
        modes["pause"] = True

        canvas.delete(icons["pause"])
        if stats["special-level"]:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="#3f3f3f",
                                                       outline="#3f3f3f")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#afafaf")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#afafaf")

            temp['pause/menu_frame'] = Frame(root, bg="#3f3f3f")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=20, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#1f1f1f", fg="#afafaf", font=font)
            back = "#1f1f1f"
            fore = "yellow"
        else:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="darkcyan",
                                                       outline="darkcyan")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#7fffff")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            temp['pause/menu_frame'] = Frame(root, bg="darkcyan")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=500, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        temp["s_frame"] = Frame(root, bg=back)
        temp["s_frame"].place(x=config["middle-x"], y=config["middle-y"] / 2 + 250, anchor='n', width=1000)

        temp["sw"] = ScrolledWindow(temp["s_frame"], 1020, 321, height=321, width=1000)

        temp["canv"] = temp["sw"].canv
        temp["canv"].config(bg=back)
        temp["sw"].scrollwindow.config(bg=back)

        temp["frame"] = temp["sw"].scrollwindow

        a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
             "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
             "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        c = ("bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
             "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
             "bubble.state.slowmotion",
             "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
             "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
             "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

        canvass = Canvas(temp["frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(a)):
            # print(a[i], b[i])
            place_bubble(canvass, bub, x, y, 25, a[i])
            canvass.create_text(x, y + 40, text=lang[c[i]], fill=fore, font=[font, 10])
            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill="y")

        temp["pause/back-to-menu"].pack(fill="x")

        icons["pause"] = canvas.create_image(config["middle-x"], config["middle-y"] / 2,
                                             image=icons["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()
    elif event.keysym == "Escape" and modes["pause"] and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and (not modes["cheater"]):
        modes["pause"] = False

        canvas.itemconfig(icons["pause"], state="hidden")
        canvas.itemconfig(texts["pause"], text="")

        temp["pause/back-to-menu"].destroy()
        temp['pause/menu_frame'].destroy()
        temp["s_frame"].destroy()

        canvas.delete(temp['pause/toline'])
        # canvas.delete(temp['pause/bottom.line'])
        canvas.delete(temp['pause/menu'])
        canvas.delete(temp['pause/bg'])

        root.update()

        stats["scorestate_time"] = temp["scorestate-save"] + time()
        stats["secure_time"] = temp["secure-save"] + time()
        stats["timebreak_time"] = temp["timebreak-save"] + time()
        stats["confusion_time"] = temp["confusion-save"] + time()
        stats["slowmotion_time"] = temp["slowmotion-save"] + time()
        stats["paralyse_time"] = temp["paralyse-save"] + time()
        stats["shotspeed_time"] = temp["shotspeed-save"] + time()
        stats["notouch_time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not modes["teleport"]):
        modes["pause"] = True

        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()

        modes["teleport"] = True

        tp_mode(canvas, config, stats, modes, tp)
    if event.keysym.lower() == "e" and (not modes["store"]):
        modes["pause"] = True
        temp["scorestate-save"] = stats["scorestate_time"] - time()
        temp["secure-save"] = stats["secure_time"] - time()
        temp["timebreak-save"] = stats["timebreak_time"] - time()
        temp["confusion-save"] = stats["confusion_time"] - time()
        temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        temp["paralyse-save"] = stats["paralyse_time"] - time()
        temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        temp["notouch-save"] = stats["notouch_time"] - time()
        temp["special-level-save"] = stats["special-level_time"] - time()
        modes["store"] = True
        log.debug("bub_move", "Creating Store() to variable \"store\"")
        log.debug("bub_move", "storemode=" + str(modes["store"]))
        commands["store"] = Store(canvas, log, config, modes, stats, icons, fore, font, laucher_cfg)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       modes)

    if event.keysym == "Escape":
        s.save()
    root.update()


# noinspection PyUnusedLocal,PyArgumentList,PyCallByClass
class Game(CanvasScene):
    def __init__(self, launcher_cfg: Dict[str, Any], start_time=0.0, already_opened=False):
        super().__init__(Registry.get_root())

    def exec(self, save_name):
        # Imports
        import config
        import os
        import yaml

        print("started Game")

        # # TODO: make modding compatible
        # if not os.path.exists("mods/%s" % self.versionDir):
        #     os.makedirs("mods/%s" % self.versionDir)
        #
        # # Load Mods
        # self.mod_loader = mods.Loader(launcher_cfg)
        #
        # print("started mods")

        # Define Empty Attributes for use with slots-menu
        self.item_info = None

        self.frame5 = None
        self.frame3 = None
        self.frame4 = None
        self.lang_lbl = None
        self.lang_selected = None
        self.lang_btn = None

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
        self.temp["paralyse-save"] = 0
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

        Registry.register_keybinding("w", player.move_up)

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

        # Collision class
        self.Coll = Collision()

        return

        # if not already_opened:
        #     self.close = Button(self.root, text="x", fg="white", relief="flat", bg="#ff0000",
        #                         command=lambda: os.kill(os.getpid(), -1))
        #     self.close.pack(side=TOP, fill="x")

        self.items = list()

        # Defining self.background class.
        self.background = Background(self.root)

        self.start_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.load(),
                                text=self.lang["home.start"],
                                relief="flat", font=(self.font, 20 + self.f_size))
        self.start_btn.place(x=Registry.gameData["WindowWidth"] / 2, y=Registry.gameData["WindowHeight"] / 2 - 40, width=310, anchor=CENTER)

        self.quit_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.root.destroy(),
                               text=self.lang["home.quit"],
                               relief="flat", font=(self.font, 20 + self.f_size))
        self.quit_btn.place(x=Registry.gameData["WindowWidth"] / 2 + 80, y=Registry.gameData["WindowHeight"] / 2 + 40, width=150, anchor=CENTER)

        self.options_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4,
                                  text=self.lang["home.options"],
                                  relief="flat", font=(self.font, 20 + self.f_size))  # , command=lambda: self.options())
        self.options_btn.place(x=Registry.gameData["WindowWidth"] / 2 - 80, y=Registry.gameData["WindowHeight"] / 2 + 40, width=150,
                               anchor=CENTER)

        # Refresh game.
        self.root.update()

        # Non-stop refreshing the background.
        while True:
            try:
                self.background.create_bubble()
                self.background.move_bubbles()
                self.background.cleanup_bubs()
                self.root.update()
            except TclError:
                break

        self.root.mainloop()

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
        self.frame5.pack(fill="both", expand=True)

        self.frame3 = Frame(self.frame5, height=700, width=1000, bg="#5c5c5c")
        self.frame3.pack()

        self.frame4 = Frame(self.frame5, height=20, bg="#5c5c5c")
        self.frame4.pack(side=BOTTOM, fill="x")

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
        self.canvas = Canvas(self.root, height=Registry.gameData["WindowHeight"], width=Registry.gameData["WindowWidth"], highlightthickness=0)
        self.canvas.pack(expand=True)

        # Run the main method (function).
        self.main()

    def resize(self, event):
        # Reload config resolution.
        Registry.gameData["WindowHeight"] = event.height
        Registry.gameData["WindowWidth"] = event.width

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
                        if y < Registry.gameData["WindowHeight"] - self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0, (self.stats["shipspeed"] / (self.move_fps / 4) + a))
                            self.root.update()
                    elif self.pressed['Left']:
                        if x > 0 + self.config["Game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], (-self.stats["shipspeed"] / (self.move_fps / 4) - a), 0)
                            self.root.update()
                    elif self.pressed['Right']:
                        if x < Registry.gameData["WindowWidth"] - self.config["Game"]["ship-radius"]:
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
                    self.stats["Effects"]["scorestate_time"] = self.temp["scorestate-save"] + time()
                    self.stats["Effects"]["secure_time"] = self.temp["secure-save"] + time()
                    self.stats["Effects"]["timebreak_time"] = self.temp["timebreak-save"] + time()
                    self.stats["Effects"]["confusion_time"] = self.temp["confusion-save"] + time()
                    self.stats["Effects"]["slowmotion_time"] = self.temp["slowmotion-save"] + time()
                    self.stats["Effects"]["paralyse_time"] = self.temp["paralyse-save"] + time()
                    self.stats["Effects"]["shotspeed_time"] = self.temp["shotspeed-save"] + time()
                    self.stats["Effects"]["notouch_time"] = self.temp["notouch-save"] + time()

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
                    #     if y < Registry.gameData["WindowHeight"] - self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], 0, (self.stats["shipspeed"] / (self.move_fps / 4) + a))
                    #         self.root.update()
                    # elif self.xControl['Left']:
                    #     if x > 0 + self.config["Game"]["ship-radius"]:
                    #         self.canvas.move(self.ship["id"], (-self.stats["shipspeed"] / (self.move_fps / 4) - a), 0)
                    #         self.root.update()
                    # elif self.xControl['Right']:
                    #     if x < Registry.gameData["WindowWidth"] - self.config["Game"]["ship-radius"]:
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
                self.commands["store"].set_selected(self.canvas, int((Registry.gameData["WindowHeight"] - 215) / 140 + 1))

    def down_release(self, event):
        self.pressed["Down"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if y < Registry.gameData["WindowHeight"] - 105 - 5:
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
            self.commands["store"].set_selected(self.canvas, int(-((Registry.gameData["WindowHeight"] - 215) / 140 + 1)))

    def right_release(self, event):
        self.pressed["Right"] = False
        if self.modes["teleport"]:
            x, y = get_coords(self.canvas, self.tp["id1"])
            if x < Registry.gameData["WindowWidth"] - 5:
                self.canvas.move(self.tp["id1"], 5, 0)
                self.canvas.move(self.tp["id2"], 5, 0)
                self.canvas.move(self.tp["id3"], 5, 0)
                self.canvas.move(self.tp["id4"], 5, 0)
        if self.modes["store"]:
            self.commands["store"].set_selected(self.canvas, int((Registry.gameData["WindowHeight"] - 215) / 140 + 1))

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

    def show_scene(self, save_name):
        super(Game, self).show_scene()
        self.run(save_name)

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        from threading import Thread
        from lib import xbox

        print("[Game]:", "Starting XboxController")
        self.xbox = xbox.XboxController()
        print("[Game]:", "Started XboxController")

        a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        self.xControl["LeftJoystick"] = a
        self.xControl["RightJoystick"] = b
        self.xControl["A"] = bool(self.xbox.A)
        self.xControl["B"] = bool(self.xbox.B)
        self.xControl["x"] = bool(self.xbox.X)
        self.xControl["y"] = bool(self.xbox.Y)
        self.xControl["Start"] = bool(self.xbox.Start)
        self.xControl["Back"] = bool(self.xbox.Back)
        self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)
        t0 = self.canvas.create_rectangle(0, 0, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"], fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 30,
                                     text="Loading...",
                                     font=(self.font, 50 + self.f_size), fill="#afafaf")
        t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 20,
                                     text="Loading Mods",
                                     font=(self.font, 15 + self.f_size), fill="#afafaf")
        self.canvas.update()

        # Pre-Initialize
        self.mod_loader.pre_initialize(self)

        # Copy self.canvas into c.
        c = self.canvas

        # Reload middle positions.
        mid_x = Registry.gameData["WindowWidth"] / 2
        mid_y = Registry.gameData["WindowHeight"] / 2

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
        self.bub["Paralyse"] = dict()
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
            self.bub["SpeedDown"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f",
                                                                "#373737")
            self.bub["SpeedUp"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
            self.bub["Up"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
            self.bub["Ultimate"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
            self.bub["Kill"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000", )
            self.bub["Teleporter"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020",
                                                                 "#373737")
            self.bub["SlowMotion"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
            self.bub["DoubleState"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
            self.bub["Protect"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
            self.bub["ShotSpdStat"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
            self.bub["HyperMode"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
            self.bub["TimeBreak"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
            self.bub["Confusion"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
            self.bub["Paralyse"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
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
        c.move(self.ship["id"], self.stats["Player"]["ShipStats"]["ShipPosition"][0],
               self.stats["Player"]["ShipStats"]["ShipPosition"][1])

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        # Initializing the panels for the game.
        self.panels["game/top"] = self.canvas.create_rectangle(
            -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        )

        # Create seperating lines.
        self.canvas.create_line(0, 70, Registry.gameData["WindowWidth"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, Registry.gameData["WindowWidth"], 69, fill="white")

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
        c.create_text(850, 30, text=self.lang["info.state.paralyse"], fill="gold", font=[self.font, 15 + self.f_size])
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
        self.texts["paralyse"] = c.create_text(850, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Paralyse")
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
        self.icons["pause"] = c.create_image(mid_x, mid_y, image=self.icons["pause-id"], state="hidden")
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
                                         self.bub, self.font, event, self.c_ammo, self.launcher_cfg, log, s))

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

        print(stats)

        if stats["Effects"]["scorestate_time"] <= time():
            stats["Effects"]["scorestate"] = 1
            stats["Effects"]["scorestate_time"] = time()
        if stats["Effects"]["secure_time"] <= time():
            stats["Effects"]["secure"] = False
            stats["Effects"]["secure_time"] = time()
        if stats["Effects"]["slowmotion_time"] <= time():
            stats["Effects"]["slowmotion"] = False
            stats["Effects"]["slowmotion_time"] = time()
        if stats["Effects"]["timebreak_time"] <= time():
            stats["Effects"]["timebreak"] = False
            stats["Effects"]["timebreak_time"] = time()
        if stats["Effects"]["confusion_time"] <= time():
            stats["Effects"]["confusion"] = False
            stats["Effects"]["confusion_time"] = time()
        if stats["Effects"]["speedboost_time"] <= time():
            stats["Effects"]["speedboost"] = False
            stats["Effects"]["speedboost_time"] = time()
        if stats["Effects"]["paralyse_time"] <= time():
            stats["Effects"]["paralyse"] = False
            stats["Effects"]["paralyse_time"] = time()
        if stats["Effects"]["shotspeed_time"] <= time():
            stats["Effects"]["shotspeed"] = 0.1
            stats["Effects"]["shotspeed_time"] = time()
        if stats["Effects"]["special-level_time"] <= time():
            stats["Effects"]["special-level"] = False
            stats["Effects"]["special-level_time"] = time()
        else:
            self.canvas.itemconfig(self.back["id"], image=self.back["special"])
            self.canvas.itemconfig(self.panels["game/top"], fill="#3f3f3f")
        if stats["Player"]["score"] < 0:
            log.error("Game.main", "The 'Score' variable under zero.")
            stats["Player"]["score"] = 0
        if stats["Player"]["score"] > stats["Player"]["high-score"]:
            stats["Player"]["high-score"] = stats["Player"]["score"]
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

        height = Registry.gameData["WindowHeight"]
        width = Registry.gameData["WindowWidth"]

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
                g2 = c.create_text(mid_x, mid_y + 60, text='Score: ' + str(self.stats["Player"]["score"]), fill='white',
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
    if "--debug" in sys.argv:
        Game(default_launchercfg, time(), False)
    else:
        print("Error: Can't open this file. Please open this file with the launcher.")
