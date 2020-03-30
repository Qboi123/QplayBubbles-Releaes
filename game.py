import sys

from background import Background
from bubbleSystem import start
from bubbles import Bubble
from events import SavedataReadedEvent, KeyReleaseEvent, UpdateEvent, KeyPressEvent, XInputEvent, CollisionEvent
from modemanager import ModeManager
from sprites import Player
from utils import control, Maintance, Font
from globals import MAX_BUBBLES

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

import config
from ammo import *
from base import Ammo, Panel, Sprite
from bubble import Collision, create_bubble, place_bubble
from components import *
from extras import Logging, refresh, shuffling
from special import ScrolledWindow
from teleport import *
from scenemanager import CanvasScene

import sys

default_launchercfg = {"version": "v1.5.0-pre1",
                       "versionDir": "v1_5_0_pre1",
                       "debug": False}

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
            # noinspection PyDeepBugsBinOperator
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

            temp["pause/back-to-menu"] = Button(temp["qbubbles:pause.menu_frame"], text=lang["pause.back-to-home"],
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

            temp["pause/back-to-menu"] = Button(temp["qbubbles:pause.menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief="flat", bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        temp["qbubbles:pause.s_frame"] = Frame(root, bg=back)
        temp["qbubbles:pause.s_frame"].place(x=config["middle-x"], y=config["middle-y"] / 2 + 250, anchor='n',
                                             width=1000)

        temp["qbubbles:pause.sw"] = ScrolledWindow(temp["qbubbles:pause.s_frame"], 1020, 321, height=321, width=1000)

        temp["qbubbles:pause.canv"] = temp["qbubbles:pause.sw"].canv
        temp["qbubbles:pause.canv"].config(bg=back)
        temp["qbubbles:pause.sw"].scrollwindow.config(bg=back)

        temp["qbubbles:pause.frame"] = temp["qbubbles:pause.sw"].scrollwindow

        a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
             "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
             "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        canvas = (
            "bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
            "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
            "bubble.state.slowmotion",
            "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
            "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
            "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

        canvass = Canvas(temp["qbubbles:pause.frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(a)):
            # print(a[i], b[i])
            place_bubble(canvass, bub, x, y, 25, a[i])
            canvass.create_text(x, y + 40, text=lang[canvas[i]], fill=fore, font=[font, 10])
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
        temp["qbubbles:pause.s_frame"].destroy()

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
        # # TODO: Change to Store-scene instead of creating a Store instance
        # commands["store"] = Store(canvas, log, config, modes, stats, icons, fore, font, laucher_cfg)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       modes)

    if event.keysym == "Escape":
        s.save()
    root.update()


# noinspection PyUnusedLocal,PyArgumentList,PyCallByClass,PyAttributeOutsideInit
class Game(CanvasScene):
    def __init__(self):
        super().__init__(Registry.get_window("default"))

        # Start variables for the game
        self.texts = {}
        self.pauseIcon: Optional[PhotoImage] = None
        self.modeManager = ModeManager()
        self.log = log
        self.returnmain = False

        # Startup
        self.root: Tk = Registry.get_window("default")
        self.time1: float = Registry.gameData["startTime"]
        self.maintance: Maintance = Maintance()
        self.saveName: Optional[str] = None

        # Stats
        Registry.saveData = dict()
        self.xControl = dict()

        # Standard Temporaray variables
        self.temp: Dict[str, Any] = dict()
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

        # XInput pressed dpad buttons
        self.pressed = {"Up": False,
                        "Down": False,
                        "Left": False,
                        "Right": False,
                        }

        self._pauseMode = False

        self.player: Optional[Player] = None

    # noinspection PyAttributeOutsideInit
    def show_scene(self, save_name):  # , save_data: Dict[str, Union[List, Dict[Any, Any], str, int, bool, float]]):
        super(Game, self).show_scene()

        print("started Game")

        # Initialize save-data
        self.saveName = save_name

        # noinspection PyDictCreation
        self.commands = {"store": False, "present": False, "special-mode": False}
        self.commands["store"]: Union[bool, Store] = False
        self.commands["present"]: Union[bool, Present] = False
        self.commands["special-mode"]: Union[bool, SpecialMode] = False

        self.player = Player()

        # self.tp = TPSprite()  # TODO: Make support for TPSprite(...) object in './sprites.py'. When done, uncomment.

        # # TODO: Replace Ammo id-dict with classes loaded in ./load.py using ./ammoTypes.py, ./ammo.py, ./sprites.py
        # # Ammo id-dictionary
        # self.ammo = {"ammo-id": list(), "ammo-radius": 5, "ammo-speed": list(), "ammo-position": list(),
        #              "ammo-damage": list(), "retime": Registry.gameData["startTime"]}

        self.run(save_name)

        # # Saved game data event, and regiser save-data
        # Registry.saveData = save_data
        # SavedataReadedEvent(Registry.saveData)

    def options(self):
        pass

    def run(self, save_name):
        # Getting save-name and copy this in the self.
        self.saveName = save_name

        # Reload stats with the reader.
        Registry.saveData = Reader("saves/" + self.saveName + "/game.nzt").get_decoded()

        # Create canvas.
        # self.canvas = Canvas(self.root, height=Registry.gameData["WindowHeight"],
        #                      width=Registry.gameData["WindowWidth"], highlightthickness=0)
        # self.canvas.pack(expand=True)

        # Run the main method (function).
        self.main()

    @staticmethod
    def on_resize(event):
        if "--travis" in sys.argv:
            return
        return

    def return_main(self):
        """
        Return to title screen
        :return:
        """
        # Returning to title menu.
        Maintance().auto_save(self.saveName, Registry.saveData)
        self.returnmain = True
        self.scenemanager.change_scene("TitleScreen")
        self.__init__()

    def on_keyrelease(self, evt: KeyReleaseEvent):
        """
        TODO: Rename method to on_keyrelease
        Key-release event, called when user stops pressing a key on the keyboard
        :param evt:
        :return:
        """
        if evt.char.lower() == "e":
            pass  # TODO: Change here to the inventory scene (when created)
        if evt.keySym.lower() == "esc" or evt.keySym.lower() == "escape":
            if self._pauseMode is False:
                self.pause()  # FIXME: Create pause-menu
            elif self._pauseMode is True:
                self.unpause()  # FIXME: Destroy pause-menu
            else:
                raise ValueError("Pause mode must be True or False")

    def pause(self):
        # TODO: Create pause menu here, set game to pause and call PauseEvent(...)
        self._pauseMode = True

        root = Registry.get_window("default")

        font = Font("Helvetica", 10)

        if self.pauseIcon is not None:
            self.canvas.delete(self.pauseIcon)  # Registry.get_icon("pause"))
        if self.modeManager.currentModeName == "specialLevel":
            self.temp["qbubbles:pause.bg"] = self.canvas.create_rectangle(
                0, 69, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
                fill="#3f3f3f", outline="#3f3f3f")
            self.temp["qbubbles:pause.to_line"] = self.canvas.create_line(
                0, 69, Registry.gameData["WindowWidth"], 69, fill="#afafaf")
            self.temp["qbubbles:pause.menu_frame"] = Frame(
                root, bg="#3f3f3f")
            self.temp['qbubbles:pause.menu'] = self.canvas.create_window(
                Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 130,
                window=self.temp['pause/menu_frame'], anchor='n', height=20, width=300)
            self.temp["qbubbles:pause.back_to_menu"] = Button(
                self.temp["qbubbles:pause.menu_frame"], text=Registry.gameData["language"]["pause.back-to-home"],
                command=lambda: self.return_main(), relief="flat", bg="#1f1f1f", fg="#afafaf", font=font)
            back = "#1f1f1f"
            fore = "yellow"
        else:
            self.temp["qbubbles:pause.bg"] = self.canvas.create_rectangle(
                0, 69, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
                fill="darkcyan", outline="darkcyan")
            self.temp["qbubbles:pause.to_line"] = self.canvas.create_line(
                0, 69, Registry.gameData["WindowWidth"], 69, fill="#7fffff")
            # self.temp['pause/bottom.line'] = self.canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            self.temp["qbubbles:pause.menu_frame"] = Frame(root, bg="darkcyan")
            self.temp["qbubbles:pause.menu"] = self.canvas.create_window(
                Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2 + 130,
                window=self.temp['pause/menu_frame'], anchor='n', height=500, width=300)

            self.temp["qbubbles:pause.back_to_menu"] = Button(
                self.temp["qbubbles:pause.menu_frame"], text=Registry.gameData["language"]["pause.back-to-home"],
                command=lambda: self.return_main(), relief="flat", bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        self.temp["qbubbles:pause.s_frame"] = Frame(root, bg=back)
        self.temp["qbubbles:pause.s_frame"].place(
            x=Registry.gameData["MiddleX"], y=Registry.gameData["MiddleY"] / 2 + 250, anchor='n', width=1000)
        self.temp["qbubbles:pause.sw"] = ScrolledWindow(
            self.temp["qbubbles:pause.s_frame"], 1020, 321, height=321, width=1000)

        self.temp["qbubbles:pause.canv"] = self.temp["qbubbles:pause.sw"].canv
        self.temp["qbubbles:pause.canv"].config(bg=back)
        self.temp["qbubbles:pause.sw"].scrollwindow.config(bg=back)

        self.temp["qbubbles:pause.frame"] = self.temp["qbubbles:pause.sw"].scrollwindow

        a = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
             "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
             "Coin", "NoTouch", "Paralyse", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        c = ("bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
             "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
             "bubble.state.slowmotion",
             "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
             "bubble.coin", "bubble.state.notouch", "bubble.state.paralyse", "bubble.diamond", "bubble.stonebubble",
             "bubble.present", "bubble.state.specialkey", "bubble.levelkey")

        canvass = Canvas(self.temp["qbubbles:pause.frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        self.temp["qbubbles:pause.bubble.icons"] = []
        bubbles: List[Bubble] = Registry.get_bubbles()
        for i in range(len(bubbles)):
            # print(a[i], b[i])
            uname = bubbles[i].get_uname()
            bubble_icon = Registry.get_bubresource(uname, "images")[50]
            self.temp["qbubbles:pause.bubble.icons"].append(
                canvass.create_image(
                    x, y, bubbles[i].get_uname()
                )
            )
            self.temp["qbubbles:pause.bubble.texts"].append(
                canvass.create_text(
                    x, y + 40, text=Registry.get_lname("bubble", Registry.get_bubbles(), "name"), fill=fore, font=font
                )
            )
            # place_bubble(canvass, bub, x, y, 25, a[i])

            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill="y")

        self.temp["qbubbles:pause.canvass"] = canvass
        self.temp["qbubbles:pause.back_to_menu"].pack(fill="x")

        self.temp["qbubbles:pause.icon_id"] = self.canvas.create_image(
            Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] / 2, image=Registry.get_icon("pauseIcon"))

        self.canvas.itemconfig(self.texts["pause"], text="")  # TODO: Remove the use of pause-text
        root.update()

        # # TODO: Remove this unused s###
        # self.self.temp["scorestate-save"] = stats["scorestate_time"] - time()
        # self.self.temp["secure-save"] = stats["secure_time"] - time()
        # self.self.temp["timebreak-save"] = stats["timebreak_time"] - time()
        # self.self.temp["confusion-save"] = stats["confusion_time"] - time()
        # self.self.temp["slowmotion-save"] = stats["slowmotion_time"] - time()
        # self.self.temp["paralyse-save"] = stats["paralyse_time"] - time()
        # self.self.temp["shotspeed-save"] = stats["shotspeed_time"] - time()
        # self.self.temp["notouch-save"] = stats["notouch_time"] - time()
        # self.self.temp["special-level-save"] = stats["special-level_time"] - time()

    def unpause(self):
        # TODO: Destroy pause menu here, set game to unpause and call UnpauseEvent(...)
        self._pauseMode = False

    def on_keypress(self, event):
        """
        TODO: Add custom key-events using Registry.get_keybindings("press", ...)
        TODO: Change name to on_keypress
        TODO: Make auto-update events
        :return:
        """

        KeyPressEvent(self, event)

    # noinspection PyAttributeOutsideInit
    def movent_change(self):
        """
        TODO: Remove Game.movement_change(...)
        Movement change thread
        :return:
        """

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
            Thread(None, lambda: self.on_keypress()).start()
            sleep(0.01)

    def _xbox_input(self):
        """
        TODO: Use Registry.get_xboxbinding(...) to check if the event is used
        TODO: Call the XInputEvent(...) here (to update and call event handlers)
        xinput handlers
        :return:
        """

        XInputEvent(self)

        # # TODO: Remove this unused s###
        # time2 = time()
        # while not self.returnmain:
        #     self.xbox.update()
        #     a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        #     b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        #     self.xControl["LeftJoystick"] = a
        #     self.xControl["RightJoystick"] = b
        #     self.xControl["A"] = bool(self.xbox.A)
        #     self.xControl["B"] = bool(self.xbox.B)
        #     self.xControl["X"] = bool(self.xbox.X)
        #     self.xControl["Y"] = bool(self.xbox.Y)
        #     self.xControl["Start"] = bool(self.xbox.Start)
        #     self.xControl["Back"] = bool(self.xbox.Back)
        #     self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        #     self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        #     self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        #     self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)

    def xboxDeamon(self):
        """
        TODO: Use events for xinput (xbox) events
        TODO: Remove Game.xboxDeamon(...)
        XInput update thread
        :return:
        """

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
        """
        FIXME: Use XInputEvent(...) instead of Game.xMovent(...)
        TODO: Use XInputEvent(...) in the sprite class, or gui class

        Movement for xinput
        :return:
        """

        if self.modeManager.currentModeName == "present":  # self.modes["present"]:
            if self.xControl["A"]:
                # noinspection PyDeepBugsBinOperator,PyDeepBugsBinOperand
                if False != self.commands["present"] != True:
                    self.commands["present"].exit(self.canvas)
                    self._pauseMode = False
                    self.modes["present"] = False
                    Registry.saveData["Effects"]["scorestate_time"] = self.temp["scorestate-save"] + time()
                    Registry.saveData["Effects"]["secure_time"] = self.temp["secure-save"] + time()
                    Registry.saveData["Effects"]["timebreak_time"] = self.temp["timebreak-save"] + time()
                    Registry.saveData["Effects"]["confusion_time"] = self.temp["confusion-save"] + time()
                    Registry.saveData["Effects"]["slowmotion_time"] = self.temp["slowmotion-save"] + time()
                    Registry.saveData["Effects"]["paralyse_time"] = self.temp["paralyse-save"] + time()
                    Registry.saveData["Effects"]["shotspeed_time"] = self.temp["shotspeed-save"] + time()
                    Registry.saveData["Effects"]["notouch_time"] = self.temp["notouch-save"] + time()

        if (self.modeManager.currentModeName != "teleport") and (self.modeManager.currentModeName != "store") and (
                self.modeManager.currentModeName != "window"):
            if not self._pauseMode:
                if not Registry.saveData["Effects"]["paralyse"]:
                    x, y = get_coords(self.canvas, self.player.id)
                    if Registry.saveData["Effects"]["speedboost"]:
                        a = 6
                    else:
                        a = 1

                    self.canvas.move(self.player.id,
                                     (Registry.saveData["shipspeed"] / (self.move_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][0] / 7,
                                     -((Registry.saveData["shipspeed"] / (self.move_fps / 4) + a) * self.xControl[
                                         "LeftJoystick"][1] / 7))

    def shot(self, event):
        # TODO: Remove Game.shot(...) and use on_keyrelease- or on_keypress-events
        # TODO: Use Ammo(...) subclasses for ammo shooting
        if (not self.modeManager.currentMode == "teleport") and (not self.modes["store"]) and (
                not self.modes["window"]):
            if not self._pauseMode:
                if not Registry.saveData["Effects"]["paralyse"]:
                    if event.keysym == "space":
                        # noinspection PyTypeChecker
                        create_shot(self.canvas, self.ammo, self.config, self.ship, Registry.saveData)

    def on_autosave(self):
        # TODO: Use events for Game.on_autosave like AutoSaveEvent(...)
        while not self.returnmain:
            Maintance.auto_save(self.saveName, Registry.saveData)
            print(self.returnmain)
            sleep(2)



    def update(self):
        # TODO: Make this completely using events like CollisionEvent(...), or UpdateEvent
        self.canvas.tag_raise(self.player.id)
        if len(self.bubbles) < MAX_BUBBLES:
            if SpecialLevelEffect in self.player.appliedEffectTypes:
                Thread(None,
                       lambda: create_bubble(Registry.saveData, self.config, self.bub, self.canvas,
                                             self.bubbles),
                       name="CreateBubbleThread").start()
            else:
                Thread(None, lambda: SpecialMode().create_bubble(self.canvas, self.config,
                                                                 self.bubbles, Registry.saveData,
                                                                 self.bub),
                       name="SpecialModeCreateBubbleThread").start()
        # if self.commands["present"] is True:
        #     # noinspection PyTypeChecker
        #     self.commands["present"] = Present(self.canvas, Registry.saveData, self.temp, self.modes,
        #                                        self.config, self.icons, self.fore, self.log, self.font)
        # if self.commands["special-mode"] is True:
        #     State.set_state(self.canvas, log, Registry.saveData, "SpecialLevel", self.back)
        #     self.commands["special-mode"] = False
        # Collision().check_collision(self.root, self.commands, self.bubbles, self.config,
        #                             Registry.saveData,
        #                             self.ammo,
        #                             self.ship, self.canvas, log, self.back,
        #                             self.texts, self.panels)
        for object1 in range(len(self.gameObjects)):
            for object2 in range(object1, len(self.gameObjects)):
                gameObj1: Sprite = self.gameObjects[object1]
                gameObj2: Sprite = self.gameObjects[object2]
                CollisionEvent(self, gameObj1, gameObj2)
        UpdateEvent(self, 0, self.canvas)
        # Thread(None, lambda: refresh(Registry.saveData, self.config, self.bubbles, self.bub, self.canvas,
        #                              self.back, self.texts, self.modes, self.panels),
        #        name="RefreshThread").start()

    # noinspection PyTypeChecker,PyShadowingNames
    def main(self):
        from threading import Thread
        from lib import xbox

        loadDescFont = Font("Helvetica", 13)
        loadTitleFont = Font("Helvetica", 46, "bold")
        t0 = self.canvas.create_rectangle(0, 0, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"],
                                          fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 30,
                                     text="Loading...",
                                     font=loadTitleFont.get_tuple(), fill="#afafaf")
        t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 20,
                                     text="Loading Mods",
                                     font=loadDescFont.get_tuple(), fill="#afafaf")
        self.canvas.update()

        # Setting background from nothing to normal.
        # Registry.get_background("id"] = self.canvas.create_image(0, 0, anchor=NW, image=self.back["normal"])

        # # Creating player id  # TODO: Remove this s###
        # self.player.id = self.canvas.create_image(7.5, 7.5, image=self.ship["image"])
        self.player.create(7.5, 7.5)
        # print(self.player.id)

        shipPosition = Registry.saveData["Player"]["ShipStats"]["ShipPosition"]

        self.player.teleport(shipPosition[0], shipPosition[1])

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        panelTop = Panel(self.canvas, 0, 0, width="extend", height=69)
        panelTopFont = Font("Helvetica", 12)

        # # Initializing the panels for the game.
        # self.panels["game/top"] = self.canvas.create_rectangle(
        #     -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        # )

        # Create seperating lines.
        self.canvas.create_line(0, 70, Registry.gameData["WindowWidth"], 70, fill="lightblue")
        self.canvas.create_line(0, 69, Registry.gameData["WindowWidth"], 69, fill="white")

        self.canvas.create_text(
            55, 30, text=Registry.gameData["language"]["info.score"],
            fill='orange', font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Score")
        self.canvas.create_text(
            110, 30, text=Registry.gameData["language"]["info.level"],
            fill='orange', font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Level")
        self.canvas.create_text(
            165, 30, text=Registry.gameData["language"]["info.speed"],
            fill='orange', font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Speed")
        self.canvas.create_text(
            220, 30, text=Registry.gameData["language"]["info.lives"],
            fill='orange', font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Lives")
        self.canvas.create_text(
            330, 30, text=Registry.gameData["language"]["info.state.score"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Score State")
        self.canvas.create_text(
            400, 30, text=Registry.gameData["language"]["info.state.protect"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Protect")
        self.canvas.create_text(
            490, 30, text=Registry.gameData["language"]["info.state.slowmotion"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Slow Motion")
        self.canvas.create_text(
            580, 30, text=Registry.gameData["language"]["info.state.confusion"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Confusion")
        self.canvas.create_text(
            670, 30, text=Registry.gameData["language"]["info.state.timebreak"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Time Break")
        self.canvas.create_text(
            760, 30, text=Registry.gameData["language"]["info.state.spdboost"],
            fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        self.canvas.create_text(850, 30, text=Registry.gameData["language"]["info.state.paralyse"],
                                fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Paralize")
        self.canvas.create_text(940, 30, text=Registry.gameData["language"]["info.state.shotspeed"],
                                fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        self.canvas.create_text(1030, 30, text=Registry.gameData["language"]["info.state.notouch"],
                                fill="gold", font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        self.canvas.create_text(1120, 30, text=Registry.gameData["language"]["info.tps"],
                                fill='gold', font=panelTopFont.get_tuple())
        self.canvas.itemconfig(t2, text="Teleports")

        # Coin / Diamond icons
        self.canvas.create_image(1185, 30, image=Registry.get_icon("StoreDiamond"))
        self.canvas.itemconfig(t2, text="Diamonds")
        self.canvas.create_image(1185, 50, image=Registry.get_icon("StoreCoin"))
        self.canvas.itemconfig(t2, text="Coins")

        self.canvas.itemconfig(t1, text="Creating Stats Data")
        self.canvas.itemconfig(t2, text="")

        # Game information values.
        self.texts["score"] = self.canvas.create_text(55, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Score")
        self.texts["level"] = self.canvas.create_text(110, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Level")
        self.texts["speed"] = self.canvas.create_text(165, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Speed")
        self.texts["lives"] = self.canvas.create_text(220, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Lives")
        self.texts["scorestate"] = self.canvas.create_text(330, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Score")
        self.texts["secure"] = self.canvas.create_text(400, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Protection")
        self.texts["slowmotion"] = self.canvas.create_text(490, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Slowmotion")
        self.texts["confusion"] = self.canvas.create_text(580, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Confusion")
        self.texts["timebreak"] = self.canvas.create_text(670, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Time Break")
        self.texts["speedboost"] = self.canvas.create_text(760, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State SpeedBoost")
        self.texts["paralyse"] = self.canvas.create_text(850, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Paralyse")
        self.texts["shotspeed"] = self.canvas.create_text(940, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Ammo Speed")
        self.texts["notouch"] = self.canvas.create_text(1030, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="State Ghost Mode")
        self.texts["shiptp"] = self.canvas.create_text(1120, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = self.canvas.create_text(1210, 30, fill='cyan')
        self.canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = self.canvas.create_text(1210, 50, fill='cyan')
        self.canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                           fill='Orange',
                                                           font=Font("Helvetica", 46).get_tuple())
        self.canvas.itemconfig(t2, text="Level View")

        self.texts["pause"] = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 56, "bold").get_tuple())
        self.canvas.itemconfig(t2, text="Pauze")
        self.canvas.itemconfig(t2, text="Pauze")

        # Threaded Automatic Save (TAS)
        # self.t_auto_save = StoppableThread(None, lambda: self.on_autosave(), name="AutoSaveThread").start()

        # Binding key-events for control
        self.canvas.itemconfig(t1, text="Binding Objects")
        self.canvas.itemconfig(t2, text="Main Binding")

        self.canvas.bind_all("<KeyPress>", lambda event: self.on_keypress(event))
        self.canvas.bind_all("<KeyRelease>", lambda event: self.on_keyrelease(event))

        self.canvas.itemconfig(t2, text="Player Motion")
        self.player.activate_events()

        # # Binding other events.  # TODO: Remove unnecessary binding
        # self.canvas.bind_all('Configure', lambda event: self.resize)

        log.info("Game.main", "Key-bindings binded to 'move_ship'")

        stats = Registry.saveData

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
        if stats["Effects"]["special_level_time"] <= time():
            stats["Effects"]["special_level"] = False
            stats["Effects"]["special_level_time"] = time()
        else:
            self.canvas.itemconfig(Registry.get_background("id"), image=Registry.get_background("special"))
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

        Registry.saveData = self.maintance.auto_restore(self.saveName)

        start(self.bubbles, self.saveName, Registry.saveData, self.config, self.bub, self.modes, self.canvas)

        Maintance.auto_save(self.saveName, Registry.saveData)

        global Mainloop
        Mainloop = False

        Registry.saveData = stats

        # Post Initalize mods

        self.canvas.itemconfig(t1, text="Post Initialize Mods")
        self.canvas.itemconfig(t2, text="")
        self.mod_loader.post_initialize(self)

        height = Registry.gameData["WindowHeight"]
        width = Registry.gameData["WindowWidth"]

        a = randint(0, width)
        b = randint(0, width)
        self.canvas = randint(0, width)

        d = stats["ship-position"][0]

        e = 40

        if a + e < d or d > a - e:
            a = d - e
        if b + e < d or d > b - e:
            b = d - e - 20
        if self.canvas + e < d or d > self.canvas - e:
            self.canvas = d - e - 40

        # bariers = [BaseBarier(self), BaseBarier(self), BaseBarier(self)]
        # bariers[0].create(a, height / 2 + 72 / 2)
        # bariers[1].create(b, height / 2 + 72 / 2)
        # bariers[2].create(self.canvas, height / 2 + 72 / 2)

        self.canvas = self.canvas

        print("[XboxController]:", "Starting Daemons")

        Thread(None, lambda: self._xbox_input(), daemon=True).start()
        Thread(None, lambda: self.xboxDeamon(), daemon=True).start()
        Thread(None, lambda: self.movent_change(), "MotionThread").start()

        try:
            # MAIN GAME LOOP
            while True:
                # Registry.saveData = self.cfg.auto_restore(self.save_name)
                while self.bubbles["active"] <= len(self.bubbles["bub-index"]) - 1:
                    self.canvas.itemconfig(t2, text="Created " + str(self.bubbles["active"]) + " of " + str(
                        len(self.bubbles["bub-index"]) - 1) + " active...")
                    self.canvas.update()
                    self.root.update()
                    sleep(0.1)

                self.canvas.delete(t0)
                self.canvas.delete(t1)
                self.canvas.delete(t2)

                while Registry.saveData["lives"] > 0:
                    if self._pauseMode:
                        pass
                    UpdateEvent(self, 0, self.canvas)
                    self.root.update()
                    self.root.update_idletasks()
                self.root.update()
                # for barier in bariers:
                #     barier.destroy()
                g1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                             text='GAME OVER', fill='Red', font=('Helvetica', 60, "bold"))
                g2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 60,
                                             text='Score: ' + str(Registry.saveData["Player"]["score"]), fill='white',
                                             font=('Helvetica', 30))
                g3 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 90,
                                             text='Level: ' + str(Registry.saveData["level"]),
                                             fill='white',
                                             font=('Helvetica', 30))
                log.info("Game.main", "Game Over!")
                self.root.update()
                sleep(4)
                self.canvas.delete(g1)
                self.canvas.delete(g2)
                self.canvas.delete(g3)
                del g1, g2, g3
                Maintance().reset(self.saveName)
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
