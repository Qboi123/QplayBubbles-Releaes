if __name__ == "__main__":
    print("Error: Can't open this file. Please open the game with the launcher.")
    input()
    exit(1)

import json
import numpy as np
import neural_net as nn

from time import sleep

from .ammo import *
from .bubble import Collision, create_bubble, place_bubble
from .components import *
from .extras import Logging, refresh, shuffling
from .special import ScrolledWindow
from .teleport import *

log = Logging("logs", True, True)

log.info("<Root>", "Imports loading success")
log.info("<Root>", "Starting Game")


def control(modes, config, root, canvas, stats, bubbles, back, texts, commands, temp, panels, fore, ship, tp, lang,
            return_main, icons, parent, bub, font, event):
    """
    Ship-motion event
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
    :param parent:
    :param event:
    """
    from .base import Ammo

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
                stats["scorestate-time"] = temp["scorestate-save"] + time()
                stats["secure-time"] = temp["secure-save"] + time()
                stats["timebreak-time"] = temp["timebreak-save"] + time()
                stats["confusion-time"] = temp["confusion-save"] + time()
                stats["slowmotion-time"] = temp["slowmotion-save"] + time()
                stats["paralis-time"] = temp["paralis-save"] + time()
                stats["shotspeed-time"] = temp["shotspeed-save"] + time()
                stats["notouch-time"] = temp["notouch-save"] + time()
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

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            modes["pause"] = False

            stats["scorestate-time"] = temp["scorestate-save"] + time()
            stats["secure-time"] = temp["secure-save"] + time()
            stats["timebreak-time"] = temp["timebreak-save"] + time()
            stats["confusion-time"] = temp["confusion-save"] + time()
            stats["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["paralis-time"] = temp["paralis-save"] + time()
            stats["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, modes, ship, tp, tp["id1"])
    elif event.keysym.lower() == "space":
        a = Ammo(parent)
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
                                                relief=FLAT, bg="#1f1f1f", fg="#afafaf", font=font)
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
                                                relief=FLAT, bg="#005f5f", fg="#7fffff", font=[font])

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
             "Coin", "NoTouch", "Paralis", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        c = ("bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
             "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
             "bubble.state.slowmotion",
             "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
             "bubble.coin", "bubble.state.notouch", "bubble.state.paralis", "bubble.diamond", "bubble.stonebubble",
             "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

        canvass = Canvas(temp["frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(a)):
            # print(a[i], b[i])
            place_bubble(canvass, bub, x, y, 25, a[i])
            canvass.create_text(x, y + 40, text=lang[c[i]], fill=fore, font=[font])
            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill=Y)

        temp["pause/back-to-menu"].pack(fill=X)

        icons["pause"] = canvas.create_image(config["middle-x"], config["middle-y"] / 2,
                                             image=icons["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()
    elif event.keysym == "Escape" and modes["pause"] and (not modes["store"]) and (not modes["teleport"]) and \
            (not modes["window"]) and (not modes["present"]) and (not modes["cheater"]):
        modes["pause"] = False

        canvas.itemconfig(icons["pause"], state=HIDDEN)
        canvas.itemconfig(texts["pause"], text="")

        temp["pause/back-to-menu"].destroy()
        temp['pause/menu_frame'].destroy()
        temp["s_frame"].destroy()

        canvas.delete(temp['pause/toline'])
        # canvas.delete(temp['pause/bottom.line'])
        canvas.delete(temp['pause/menu'])
        canvas.delete(temp['pause/bg'])

        root.update()

        stats["scorestate-time"] = temp["scorestate-save"] + time()
        stats["secure-time"] = temp["secure-save"] + time()
        stats["timebreak-time"] = temp["timebreak-save"] + time()
        stats["confusion-time"] = temp["confusion-save"] + time()
        stats["slowmotion-time"] = temp["slowmotion-save"] + time()
        stats["paralis-time"] = temp["paralis-save"] + time()
        stats["shotspeed-time"] = temp["shotspeed-save"] + time()
        stats["notouch-time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not modes["teleport"]):
        modes["pause"] = True

        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()

        modes["teleport"] = True

        tp_mode(canvas, config, stats, modes, tp)
    if event.keysym.lower() == "e" and (not modes["store"]):
        modes["pause"] = True
        temp["scorestate-save"] = stats["scorestate-time"] - time()
        temp["secure-save"] = stats["secure-time"] - time()
        temp["timebreak-save"] = stats["timebreak-time"] - time()
        temp["confusion-save"] = stats["confusion-time"] - time()
        temp["slowmotion-save"] = stats["slowmotion-time"] - time()
        temp["paralis-save"] = stats["paralis-time"] - time()
        temp["shotspeed-save"] = stats["shotspeed-time"] - time()
        temp["notouch-save"] = stats["notouch-time"] - time()
        temp["special-level-save"] = stats["special-level-time"] - time()
        modes["store"] = True
        log.debug("bub_move", "Creating Store() to variable \"store\"")
        log.debug("bub_move", "storemode=" + str(modes["store"]))
        commands["store"] = Store(canvas, log, config, modes, stats, icons, fore)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       modes)

    if event.keysym == "Escape":
        s.save()
    root.update()


class Maintance:
    def __init__(self):
        pass

    @staticmethod
    def auto_save(save_name: str, game_stats: Dict[str, Any], bubble: Dict[str, Any]):
        """
        Saves the game. (For Auto-Save)
        """
        from . import config as cfg

        import os

        print(os.curdir)

        try:
            cfg.Writer("../../slots/" + save_name + "/game.json", game_stats.copy())
            cfg.Writer("../../slots/" + save_name + "/bubble.json", bubble.copy())
        except FileNotFoundError as e:
            print(e.args)
            print(e.filename)
            print(e.filename2)

    @staticmethod
    def auto_restore(save_name: str):
        """
        Restoring. (For Auto-Restore)
        """
        from . import config as cfg

        game_stats = cfg.Reader("../../slots/" + save_name + "/game.json").get_decoded()

        return game_stats

    @staticmethod
    def reset(save_name: str):
        """
        Resets the game fully
        """

        from . import config as cfg

        stats = cfg.Reader("config/reset.json").get_decoded()
        bubble = cfg.Reader("config/reset-bubble.json").get_decoded()

        cfg.Writer("../../slots/" + save_name + "/game.json", stats.copy())
        cfg.Writer("../../slots/" + save_name + "/bubble.json", bubble.copy())


def start(bubble: Dict[str, Any], save_name: str, stats: Dict[str, Any], config: Dict[str, Any], bub,
          modes: Dict[str, bool], canvas: Canvas):
    bubs = Reader("../../slots/" + save_name + "/bubble.json").get_decoded()
    if len(bubs["bub-id"]) <= 1:
        r_start(bubble, stats, config, bub, canvas, modes)
        return
    print(bubs)
    for i in range(len(bubs["bub-id"])):
        bubble["active2"].append(False)
        # print(i)
    for i in range(len(bubs["bub-id"]) - 1):
        if bubs["bub-special"]:
            create_bubble(stats, config, bub, canvas, bubble, modes, i, bubs["bub-index"][i],
                          bubs["bub-position"][i][0] + config["width"],
                          bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
        elif not bubs["bub-special"]:
            SpecialMode.create_bubble(canvas, config, bubble, stats, bub, modes, bubs["bub-index"][i],
                                      bubs["bub-position"][i][0] + config["width"],
                                      bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])


def r_start(bubble: Dict[str, Any], stats: Dict[str, Any], config: Dict[str, Any], bub, canvas: Canvas,
            modes: Dict[str, bool]):
    for i in range(int((config["width"] - 72) / 10)):
        bubble["active2"].append(False)
        # print(i)

    # print(int((config["width"] - 72) / 10))
    for i in range(int((config["width"] - 73) / 10)):
        # print(i)
        r = randint(int(config["bubble"]["min-radius"]),
                    int(config["bubble"]["max-radius"]))
        x = randint(-r, config["width"] + r)
        y = randint(72 + r, (config["height"] - r))
        # spd = stats["bubspeed"]
        # i = randint(0, 1600)
        create_bubble(stats, config, bub, canvas, bubble, modes, i, x=x, y=y, r=r)


# noinspection PyUnusedLocal
class Game(Canvas):
    def __init__(self, launcher_cfg: Dict[str, Any], start_time=0.0, already_opened=False):
        super().__init__()

        from . import config
        import os
        import yaml
        from . import mod_support as mods

        print("started Game")

        # Load Mods
        self.mod_loader = mods.Loader(launcher_cfg)

        print("started mods")

        # Laucher Config
        self.laucher_cfg = launcher_cfg

        # Laucher Config
        self.launcher_cfg = launcher_cfg

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
        self.canvas = None

        # Icons and texts
        self.icons = dict()
        self.texts = dict()

        # Back- and foreground
        self.back = dict()
        self.fore = dict()

        self.config = config.Reader("config/startup.json").get_decoded()

        fd = os.open("../../lang/" + self.config["game"]["language"] + ".yaml", os.O_RDONLY | os.O_CREAT)
        self.lang = yaml.safe_load(os.read(fd, 4096).decode())
        os.close(fd)

        if self.config["game"]["language"] == "tengwar":
            self.font = "Tengwar Annatar Regular"
            self.f_size = 0
        else:
            self.font = "Helvetica"
            self.f_size = -4

        self.commands = {"store": False, "present": False, "special-mode": False}

        # Player-prites
        self.ship = dict()
        self.tp = dict()

        # Configuration
        self.config = config.Reader("config/startup.json").get_decoded()

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
        if self.config["game"]["fullscreen"]:
            self.root.wm_attributes("-fullscreen", True)

        self.root.update()

        # Config resolution / positions
        self.config["width"] = self.root.winfo_width()
        self.config["height"] = self.root.winfo_height()

        self.config["middle-x"] = self.config["width"] / 2
        self.config["middle-y"] = self.config["height"] / 2

        # Collision class
        self.Coll = Collision()

        if not already_opened:
            self.close = Button(self.root, text="X", fg="white", relief=FLAT, bg="#ff0000",
                                command=lambda: os.kill(os.getpid(), -1))
            self.close.pack(side=TOP, fill=X)

        self.items = list()

        class Background:
            """
            Background for the title menu.
            This is a random animation.
            """

            def __init__(self, root: Tk):
                # Widgets
                self._root = root
                self._canvas = Canvas(root, bg="#00afaf", highlightthickness=0)
                self._canvas.pack(fill=BOTH, expand=TRUE)

                # Bubble-sprites config.
                self.__bubbles = []
                self.__speed = []

            def create_bubble(self):
                r = randint(9, 60)
                x = self._root.winfo_width() + 100
                y = randint(int(r), int(self._canvas.winfo_height() - r))

                spd = randint(7, 10)

                self.__bubbles.append(self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="white"))
                self.__speed.append(spd)

            def cleanup_bubs(self):
                """
                Cleaning up bubbles.
                Deleting bubble if the x coord of the bubble is under -100
                :return:
                """
                from .bubble import get_coords

                for index in range(len(self.__bubbles) - 1, -1, -1):
                    x, y, = get_coords(self._canvas, self.__bubbles[index])
                    if x < -100:
                        self._canvas.delete(self.__bubbles[index])
                        del self.__bubbles[index]
                        del self.__speed[index]

            def move_bubbles(self):
                """
                Move all bubble to the left with the self.__speed with index of the bubble
                :return:
                """
                for index in range(len(self.__bubbles) - 1, -1, -1):
                    self._canvas.move(self.__bubbles[index], -self.__speed[index], 0)

            def destroy(self):
                """
                Destroys this custom widget.
                :return:
                """
                self._canvas.destroy()

        # Defining self.background class.
        self.background = Background(self.root)

        self.start_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.load(),
                                text=self.lang["home.start"],
                                relief=FLAT, font=(self.font, 20+self.f_size))
        self.start_btn.place(x=self.config["width"] / 2, y=self.config["height"] / 2 - 40, width=310, anchor=CENTER)

        self.quit_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.root.destroy(),
                               text=self.lang["home.quit"],
                               relief=FLAT, font=(self.font, 20+self.f_size))
        self.quit_btn.place(x=self.config["width"] / 2 + 80, y=self.config["height"] / 2 + 40, width=150, anchor=CENTER)

        self.options_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4,
                                  text=self.lang["home.options"],
                                  relief=FLAT, font=(self.font, 20+self.f_size))  # , command=lambda: self.options())
        self.options_btn.place(x=self.config["width"] / 2 - 80, y=self.config["height"] / 2 + 40, width=150,
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

        a = os.listdir("../../lang/")
        b = []
        c = []
        self.lang_btn.menu = Menu(self.lang_btn, tearoff=0)
        self.lang_btn["menu"] = self.lang_btn.menu

        for i in a:
            file = open("../../lang/" + i, "r")
            b.append(yaml.unsafe_load(file)["options.name"])
            c.append(i)
            file.close()

        d = 0
        for i in range(len(b)):
            self.lang_btn.menu.add_checkbutton(label=b[i], command=lambda: self.lang_selected.set(c[i]))
            d += 1

    def options_save(self):
        import yaml

        file = open("../../lang/" + self.lang_selected.get(), "r")
        self.lang = yaml.safe_load(file)
        file.close()

        self.options_close()

    def options_close(self):
        self.frame5.destroy()

    def load(self):
        """
        This is the Slots Menu.

        Loading slots-menu.
        :return:
        """
        self.background.destroy()
        self.start_btn.destroy()
        self.quit_btn.destroy()
        self.options_btn.destroy()

        import os

        log.info("Game.load", "Loading...")

        # Removes title-menu items.

        # Getting list of slots.
        path = "../../slots/"
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

        # Add-button and -entry (Input)
        self.add = Button(self.frame2, text=self.lang["slots.add"], relief=FLAT, bg="#7f7f7f", fg="white",
                          command=self.add_save, font=[self.font, 15+self.f_size])
        self.add.pack(side=RIGHT, padx=2, pady=5)
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

        names = os.listdir("../../slots/")

        # Information variables for each slot.
        infos = {"dates": [], "score": [], "level": []}

        import time

        # Prepare info variables
        for i in names:
            mtime = os.path.getmtime("../../slots/" + i + "/bubble.json")
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

            a = Reader("../../slots/" + i + "/game.json").get_decoded()
            infos["score"].append(a["score"])
            infos["level"].append(a["level"])

        self.item_info = names

        # Define the index variable.
        i = 0

        # Startloop
        for name in tuple(dirs):
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
                       font=[self.font, 15+self.f_size]))
            self.buttons.copy()[-1].place(x=675, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", lambda event: self.open(name, event))

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.rename"], bg="#afafaf", width=7,
                       font=[self.font, 15+self.f_size]))
            self.buttons.copy()[-1].place(x=600, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.rename)

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.remove"], bg="#afafaf", width=7,
                       font=[self.font, 15+self.f_size]))
            self.buttons.copy()[-1].place(x=525, y=175, anchor=SE)
            self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.remove)

            self.buttons.append(
                Button(self.frames[-1], relief=FLAT, text=self.lang["slots.reset"], bg="#afafaf", width=7,
                       font=[self.font, 15+self.f_size]))
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
        for i in os.listdir("../../slots/" + src):
            os.remove("../../slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("../../slots/" + src)

        # Disabling the input and the button.
        self.add_input.config(state=DISABLED)
        self.add.config(state=DISABLED)

        # Getting the input text.
        if src in ("aux", "con", ".", ".."):
            return

        # Creating dir for the game.
        os.makedirs("../../slots/" + src, exist_ok=True)

        # Copy the template (resetted save-files)
        self.copy("config/reset.json", "../../slots/" + src + "/game.json")
        self.copy("config/reset-bubble.json", "../../slots/" + src + "/bubble.json")

        # Refreshing slots-menu
        self.delete_all()
        self.load()

    def add_save(self):
        """
        Adding a slot to your game.
        :return:
        """
        import os

        if len(os.listdir("../../slots/")) <= 4000:
            # Disabling the input and the button.
            self.add_input.config(state=DISABLED)
            self.add.config(state=DISABLED)

            # Getting the input text.
            new = self.add_input.get()
            if new in ("aux", "con", ".", ".."):
                return

            # Creating dir for the game.
            os.makedirs("../../slots/" + new, exist_ok=True)

            # Copy the template (resetted save-files)
            self.copy("config/reset.json", "../../slots/" + new + "/game.json")
            self.copy("config/reset-bubble.json", "../../slots/" + new + "/bubble.json")

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
        for i in os.listdir("../../slots/" + src):
            os.remove("../../slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("../../slots/" + src)

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
        os.rename("../../slots/" + src, "../../slots/" + new)

        # Refreshing slots-menu
        self.delete_all()
        self.load()

    def open(self, name, event):
        # Getting row-index
        y = event.widget.master.grid_info()["row"]

        # Getting source dir.
        src = self.item_info[y]

        # Remove slots menu and run the game.
        self.delete_all()
        self.run(name)

    def delete_all(self):
        # Delete all main frames
        self.main_f.destroy()
        self.frame2.destroy()

    def run(self, save_name):
        # Getting save-name and copy this in the self.
        self.save_name = save_name

        # Reload stats with the reader.
        self.stats = Reader("../../slots/" + self.save_name + "/game.json").get_decoded()

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
                if not self.stats["paralis"]:
                    x, y = get_coords(self.canvas, self.ship["id"])
                    if self.stats["speedboost"]:
                        a = 6
                    else:
                        a = 1
                    if self.pressed['Up']:
                        if y > 72 + self.config["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0, (-self.stats["shipspeed"] / (self.move_fps / 2) - a))
                            self.root.update()
                    elif self.pressed['Down']:
                        if y < self.config["height"] - self.config["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], 0, (self.stats["shipspeed"] / (self.move_fps / 2) + a))
                            self.root.update()
                    elif self.pressed['Left']:
                        if x > 0 + self.config["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], (-self.stats["shipspeed"] / 20 - a), 0)
                            self.root.update()
                    elif self.pressed['Right']:
                        if x < self.config["width"] - self.config["game"]["ship-radius"]:
                            self.canvas.move(self.ship["id"], (self.stats["shipspeed"] / 20 + a), 0)
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

    def down_release(self, event):
        self.pressed["Down"] = False

    def left_release(self, event):
        self.pressed["Left"] = False

    def right_release(self, event):
        self.pressed["Right"] = False

    def shot(self, event):
        if (not self.modes["teleport"]) and (not self.modes["store"]) and (not self.modes["window"]):
            if not self.modes["pause"]:
                if not self.stats["paralis"]:
                    if event.keysym == "space":
                        create_shot(self.canvas, self.ammo, self.config, self.ship, self.stats)

    def auto_save(self):
        while not self.returnmain:
            Maintance.auto_save(self.save_name, self.stats, self.bubbles)
            print(self.returnmain)
            sleep(2)

    def update(self):
        if not self.stats["timebreak"]:
            if len(self.bubbles["bub-id"]) < (self.config["width"]) / 10:
                if not self.stats["special-level"]:
                    Thread(None,
                           lambda: create_bubble(self.stats, self.config, self.bub, self.canvas,
                                                 self.bubbles, self.modes,
                                                 len(self.bubbles["bub-id"])),
                           name="CreateBubbleThread").start()
                else:
                    Thread(None, lambda: SpecialMode().create_bubble(self.canvas, self.config,
                                                                     self.bubbles, self.stats,
                                                                     self.bub, self.modes),
                           name="SpecialModeCreateBubbleThread").start()
        if self.commands["present"] is True:
            # noinspection PyTypeChecker
            self.commands["present"] = Present(self.canvas, self.stats, self.temp, self.modes,
                                               self.config, self.icons, self.fore, self.log)
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
                event.on_t_update(self)

    def r_update(self):
        self.update()
        Thread(None, lambda: self.t_update(), "UpdateThread")

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        from threading import Thread

        # Pre-Initialize
        self.mod_loader.pre_initialize(self)

        # Updates canvas.
        self.canvas.update()

        # Reload config resolution.
        self.config["height"] = self.canvas.winfo_height()
        self.config["width"] = self.canvas.winfo_width()

        # Copy self.canvas into c.
        c = self.canvas

        # Reload middle positions.
        mid_x = self.config["width"] / 2
        mid_y = self.config["height"] / 2

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

        # Adding the different resolutions to the bubbles.
        for i in range(9, 61):
            self.bub["Normal"][i] = PhotoImage(file="data/bubbles/Normal/" + str(i) + "px.png")
            self.bub["Triple"][i] = PhotoImage(file="data/bubbles/Triple/" + str(i) + "px.png")
            self.bub["Double"][i] = PhotoImage(file="data/bubbles/Double/" + str(i) + "px.png")
            self.bub["SpeedDown"][i] = PhotoImage(file="data/bubbles/SpeedDown/" + str(i) + "px.png")
            self.bub["SpeedUp"][i] = PhotoImage(file="data/bubbles/SpeedUp/" + str(i) + "px.png")
            self.bub["Up"][i] = PhotoImage(file="data/bubbles/Up/" + str(i) + "px.png")
            self.bub["Ultimate"][i] = PhotoImage(file="data/bubbles/Ultimate/" + str(i) + "px.png")
            self.bub["Kill"][i] = PhotoImage(file="data/bubbles/Kill/" + str(i) + "px.png")
            self.bub["Teleporter"][i] = PhotoImage(file="data/bubbles/Teleporter/" + str(i) + "px.png")
            self.bub["SlowMotion"][i] = PhotoImage(file="data/bubbles/SlowMotion/" + str(i) + "px.png")
            self.bub["DoubleState"][i] = PhotoImage(file="data/bubbles/DoubleState/" + str(i) + "px.png")
            self.bub["Protect"][i] = PhotoImage(file="data/bubbles/Protect/" + str(i) + "px.png")
            self.bub["ShotSpdStat"][i] = PhotoImage(file="data/bubbles/ShotSpdStat/" + str(i) + "px.png")
            self.bub["HyperMode"][i] = PhotoImage(file="data/bubbles/HyperMode/" + str(i) + "px.png")
            self.bub["TimeBreak"][i] = PhotoImage(file="data/bubbles/TimeBreak/" + str(i) + "px.png")
            self.bub["Confusion"][i] = PhotoImage(file="data/bubbles/Confusion/" + str(i) + "px.png")
            self.bub["Paralis"][i] = PhotoImage(file="data/bubbles/Paralis/" + str(i) + "px.png")
            self.bub["StoneBub"][i] = PhotoImage(file="data/bubbles/StoneBub/" + str(i) + "px.png")
            self.bub["NoTouch"][i] = PhotoImage(file="data/bubbles/NoTouch/" + str(i) + "px.png")

        # Adding the static-resolution-bubbles.
        self.bub["Key"][60] = PhotoImage(file="data/bubbles/Key.png")
        self.bub["Diamond"][36] = PhotoImage(file="data/bubbles/Diamond.png")
        self.bub["Present"][40] = PhotoImage(file="data/bubbles/Present.png")
        # noinspection PyTypeChecker
        self.bub["Coin"] = PhotoImage(file="data/CoinBub.png")
        self.bub["SpecialKey"][48] = PhotoImage(file="data/bubbles/SpecialMode.png")

        # Adding ship image.
        self.ship["image"] = PhotoImage(file="data/Ship.png")

        # Reload stats with auto-restore.
        self.stats = Maintance().auto_restore(self.save_name)

        # Getting the normal background.
        self.back["normal"] = PhotoImage(file="data/BackGround.png")

        # Getting the store-icons.
        self.icons["store-pack"] = list()
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Key.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Teleport.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Shield.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/DiamondBuy.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/BuyACake.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/Pop_3_bubs.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/PlusLife.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/SpeedBoost.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/SpecialMode.png"))
        self.icons["store-pack"].append(PhotoImage(file="data/Images/StoreItems/DoubleScore.png"))
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)
        self.icons["store-pack"].append(None)

        # Unknown
        self.back["line"] = PhotoImage(file="data/LineIcon.png")

        # Setting present foreground
        self.fore["present-fg"] = PhotoImage(file="data/EventBackground.png")

        # Setting present icons.
        self.icons["circle"] = PhotoImage(file="data/Circle.png")
        self.icons["present"] = PhotoImage(file="data/Present.png")

        # Setting store foreground
        self.fore["store-fg"] = PhotoImage(file="data/FG2.png")

        # Setting standard store icons.
        self.icons["store-diamond"] = PhotoImage(file="data/Diamond.png")
        self.icons["store-coin"] = PhotoImage(file="data/Coin.png")

        # Setting pause-icon.
        self.icons["pause-id"] = PhotoImage(file="data/Pause.png")

        # Setting slowmotion-icon.
        self.icons["slowmotion"] = PhotoImage(file="data/SlowMotionIcon.png")

        # Setting special background.
        self.back["special"] = PhotoImage(file="data/Images/Backgrounds/GameBG Special2.png")

        # Setting normal background.
        self.back["normal"] = PhotoImage(file="data/Images/Backgrounds/GameBG2.png")

        # Setting background from nothing to normal.
        self.back["id"] = self.canvas.create_image(0, 0, anchor=NW, image=self.back["normal"])

        # Creating shi
        self.ship["id"] = c.create_image(7.5, 7.5, image=self.ship["image"])
        print(self.ship["id"])

        # Moving ship to position
        c.move(self.ship["id"], self.stats["ship-position"][0], self.stats["ship-position"][1])

        # Initializing the panels for the game.
        self.panels["game/top"] = self.canvas.create_rectangle(
            -1, -1, self.config["width"], 69, fill="darkcyan"
        )
        # Create seperating lines.
        self.canvas.create_line(0, 70, self.config["width"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, self.config["width"], 69, fill="white")

        c.create_text(55, 30, text=self.lang["info.score"], fill='orange', font=[self.font, 15+self.f_size])
        c.create_text(110, 30, text=self.lang["info.level"], fill='orange', font=[self.font, 15+self.f_size])
        c.create_text(165, 30, text=self.lang["info.speed"], fill='orange', font=[self.font, 15+self.f_size])
        c.create_text(220, 30, text=self.lang["info.lives"], fill='orange', font=[self.font, 15+self.f_size])
        c.create_text(330, 30, text=self.lang["info.state.score"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(400, 30, text=self.lang["info.state.protect"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(490, 30, text=self.lang["info.state.slowmotion"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(580, 30, text=self.lang["info.state.confusion"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(670, 30, text=self.lang["info.state.timebreak"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(760, 30, text=self.lang["info.state.spdboost"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(850, 30, text=self.lang["info.state.paralis"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(940, 30, text=self.lang["info.state.shotspeed"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(1030, 30, text=self.lang["info.state.notouch"], fill="gold", font=[self.font, 15+self.f_size])
        c.create_text(1120, 30, text=self.lang["info.tps"], fill='gold', font=[self.font, 15+self.f_size])
        c.create_image(1185, 30, image=self.icons["store-diamond"])
        c.create_image(1185, 50, image=self.icons["store-coin"])

        # Game information values.
        self.texts["score"] = c.create_text(55, 50, fill='cyan')
        self.texts["level"] = c.create_text(110, 50, fill='cyan')
        self.texts["speed"] = c.create_text(165, 50, fill='cyan')
        self.texts["lives"] = c.create_text(220, 50, fill='cyan')
        self.texts["scorestate"] = c.create_text(330, 50, fill='cyan')
        self.texts["secure"] = c.create_text(400, 50, fill='cyan')
        self.texts["slowmotion"] = c.create_text(490, 50, fill='cyan')
        self.texts["confusion"] = c.create_text(580, 50, fill='cyan')
        self.texts["timebreak"] = c.create_text(670, 50, fill='cyan')
        self.texts["speedboost"] = c.create_text(760, 50, fill='cyan')
        self.texts["paralis"] = c.create_text(850, 50, fill='cyan')
        self.texts["shotspeed"] = c.create_text(940, 50, fill='cyan')
        self.texts["notouch"] = c.create_text(1030, 50, fill='cyan')
        self.texts["shiptp"] = c.create_text(1120, 50, fill='cyan')
        self.texts["diamond"] = c.create_text(1210, 30, fill='cyan')
        self.texts["coin"] = c.create_text(1210, 50, fill='cyan')
        self.texts["level-view"] = c.create_text(mid_x, mid_y, fill='Orange', font=(self.font, 50+self.f_size))

        self.texts["pause"] = c.create_text(mid_x, mid_y, fill='Orange', font=(self.font, 60+self.f_size, "bold"))
        self.icons["pause"] = c.create_image(mid_x, mid_y, image=self.icons["pause-id"], state=HIDDEN)

        # Threaded Automatic Save (TAS)
        self.t_auto_save = StoppableThread(None, lambda: self.auto_save(), name="AutoSaveThread").start()

        # Binding key-events for control
        c.bind_all('<Key>', lambda event: control(self.modes, self.config, self.root, self.canvas, self.stats, self.bubbles, self.back, self.texts, self.commands, self.temp, self.panels, self.fore, self.ship, self.tp, self.lang, self.return_main, self.icons, self, self.bub, self.font, event))

        c.bind_all("<KeyPress-Up>", lambda event: self.up_press(event))
        c.bind_all("<KeyPress-Down>", lambda event: self.down_press(event))
        c.bind_all("<KeyPress-Left>", lambda event: self.left_press(event))
        c.bind_all("<KeyPress-Right>", lambda event: self.right_press(event))

        c.bind_all("<KeyRelease-Up>", self.up_release)

        Thread(None, lambda: self.movent_change(), "MotionThread").start()

        c.bind_all("<KeyRelease-Down>", lambda event: self.down_release(event))
        c.bind_all("<KeyRelease-Left>", lambda event: self.left_release(event))
        c.bind_all("<KeyRelease-Right>", lambda event: self.right_release(event))
        c.bind_all("<Key-Z>", lambda event: self.r_update())

        # Thread(None, lambda: c.bind("<Motion>", MotionEventHandler)).start()
        # Thread(None, lambda: c.bind("<ButtonPress-1>", Button1PressEventHandler)).start()
        # Thread(None, lambda: c.bind("<ButtonRelease-1>", Button1ReleaseEventHandler)).start()

        # Binding other key-events.
        # c.bind_all('<KeyRelease-Escape>', lambda event: self.return_main())
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

        if stats["scorestate-time"] <= time():
            stats["scorestate"] = 1
            stats["scorestate-time"] = time()
        if stats["secure-time"] <= time():
            stats["secure"] = False
            stats["secure-time"] = time()
        if stats["slowmotion-time"] <= time():
            stats["slowmotion"] = False
            stats["slowmotion-time"] = time()
        if stats["timebreak-time"] <= time():
            stats["timebreak"] = False
            stats["timebreak-time"] = time()
        if stats["confusion-time"] <= time():
            stats["confusion"] = False
            stats["confusion-time"] = time()
        if stats["speedboost-time"] <= time():
            stats["speedboost"] = False
            stats["speedboost-time"] = time()
        if stats["paralis-time"] <= time():
            stats["paralis"] = False
            stats["paralis-time"] = time()
        if stats["shotspeed-time"] <= time():
            stats["shotspeed"] = 0.1
            stats["shotspeed-time"] = time()
        if stats["special-level-time"] <= time():
            stats["special-level"] = False
            stats["special-level-time"] = time()
        else:
            self.canvas.itemconfig(self.back["id"], image=self.back["special"])
            self.canvas.itemconfig(self.panels["game/top"], fill="#3f3f3f")
        if stats["score"] < 0:
            log.error("Game.main", "The 'Score' variable under zero.")
            stats["score"] = 0
        if stats["score"] > stats["hiscore"]:
            stats["hiscore"] = stats["score"]
        if stats["confusion"] and not stats["secure"]:
            shuffling(self.bubbles)

        self.bubbles["active2"] = []
        self.bubbles["active"] = 0

        self.stats = self.cfg.auto_restore(self.save_name)

        start(self.bubbles, self.save_name, self.stats, self.config, self.bub, self.modes, self.canvas)

        global Mainloop
        Mainloop = False

        self.stats = stats

        # Post Initalize mods
        self.mod_loader.post_initialize(self)

        from .base import BaseBarier

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
            b = d - e-20
        if c + e < d or d > c - e:
            c = d - e-40

        bariers = [BaseBarier(self), BaseBarier(self), BaseBarier(self)]
        bariers[0].create(a, height / 2 + 72 / 2)
        bariers[1].create(b, height / 2 + 72 / 2)
        bariers[2].create(c, height / 2 + 72 / 2)

        c = self.canvas

        try:
            # MAIN GAME LOOP
            while True:
                # self.stats = self.cfg.auto_restore(self.save_name)
                t0 = self.canvas.create_rectangle(0, 0, self.config["width"], self.config["height"], fill="#3f3f3f",
                                                  outline="#3f3f3f")
                t1 = self.canvas.create_text(self.config["middle-x"], self.config["middle-y"] - 30,
                                             text="Creating bubbles...",
                                             font=(self.font, 50+self.f_size), fill="#afafaf")
                t2 = self.canvas.create_text(self.config["middle-x"], self.config["middle-y"] + 20,
                                             text="Thread 0 of 0 active",
                                             font=(self.font, 15+self.f_size), fill="#afafaf")
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
                        pass
                    self.root.update()
                    self.root.update_idletasks()
                self.root.update()
                for barier in bariers:
                    barier.destroy()
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
        with open("input.json", "w") as file:
            json_str = self.inputs
            json_inputs = json.encoder.JSONEncoder().encode(json_str)

        with open("output.json", "w") as file:
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
