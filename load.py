import os
from time import time
from tkinter import PhotoImage

import yaml

import config
from game import Game
from menus.titleMenu import TitleMenu
from scenemanager import CanvasScene
from components import Store
from registry import Registry
from scenes import SavesMenu
from utils import Font, Maintance


class Load(CanvasScene):
    def __init__(self, root):
        super(Load, self).__init__(root)

    def __repr__(self):
        return super(CanvasScene, self).__repr__()

    def pre_initialize(self):
        pass

    def show_scene(self, *args, **kwargs):
        super(Load, self).show_scene(*args, **kwargs)
        self.initialize()

    def initialize(self):
        config_ = config.Reader(
            "config/startup.nzt").get_decoded()

        with open("lang/" + config_["Game"]["language"] + ".yaml", "r") as file:
            lang_ = yaml.safe_load(file.read())

        Registry.gameData["config"] = config_
        Registry.gameData["language"] = lang_

        # Config resolution / positions
        Registry.gameData["WindowWidth"] = Registry.get_root().winfo_screenwidth()
        Registry.gameData["WindowHeight"] = Registry.get_root().winfo_screenheight()
        Registry.gameData["MiddleX"] = Registry.gameData["WindowWidth"] / 2
        Registry.gameData["MiddleY"] = Registry.gameData["WindowHeight"] / 2

        root = Registry.get_root()
        game = Game(Registry.gameData["launcherConfig"], time())

        # Register Xbox-Bindings
        # Registry.register_xboxbinding("A", game.close_present)
        # print("[Game]:", "Starting XboxController")
        # self.xbox = xbox.XboxController()
        # print("[Game]:", "Started XboxController")
        #
        # self.xControl = dict()
        #
        # a = [int(self.xbox.LeftJoystickX * 7), int(self.xbox.LeftJoystickY * 7)]
        # b = [int(self.xbox.RightJoystickX * 7), int(self.xbox.RightJoystickY * 7)]
        # self.xControl["LeftJoystick"] = a
        # self.xControl["RightJoystick"] = b
        # self.xControl["A"] = bool(self.xbox.A)
        # self.xControl["B"] = bool(self.xbox.B)
        # self.xControl["x"] = bool(self.xbox."x")
        # self.xControl[""y""] = bool(self.xbox."y")
        # self.xControl["Start"] = bool(self.xbox.Start)
        # self.xControl["Back"] = bool(self.xbox.Back)
        # self.xControl["LeftBumper"] = bool(self.xbox.LeftBumper)
        # self.xControl["RightBumper"] = bool(self.xbox.RightBumper)
        # self.xControl["LeftTrigger"] = int((self.xbox.LeftBumper + 1) / 2 * 7)
        # self.xControl["RightTrigger"] = int((self.xbox.RightBumper + 1) / 2 * 7)

        title_font = Font("Helvetica", 50, "bold")
        descr_font = Font("Helvetica", 15)

        t0 = self.canvas.create_rectangle(0, 0, Registry.gameData["WindowWidth"], Registry.gameData["WindowHeight"], fill="#3f3f3f",
                                          outline="#3f3f3f")
        t1 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] - 30,
                                     text="Loading...",
                                     font=title_font.get_tuple(), fill="#afafaf")
        t2 = self.canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"] + 20,
                                     text="Loading Mods",
                                     font=descr_font.get_tuple(), fill="#afafaf")
        self.canvas.update()

        # # Pre-Initialize
        # self.mod_loader.pre_initialize(self)

        self.canvas.itemconfig(t1, text="Loading...")
        self.canvas.itemconfig(t2, text="Loading Config")
        self.canvas.update()

        # Reload config resolution.
        Registry.gameData["WindowHeight"] = self.canvas.winfo_height()
        Registry.gameData["WindowWidth"] = self.canvas.winfo_width()

        self.canvas.itemconfig(t1, text="Loading Bubbles")
        self.canvas.itemconfig(t2, text="Creating Dicts")
        self.canvas.update()

        # Adding the dictionaries for the bubbles. With different res.
        Registry.gameData["BubbleImage"] = dict()
        Registry.gameData["BubbleImage"]["Normal"] = dict()
        Registry.gameData["BubbleImage"]["Triple"] = dict()
        Registry.gameData["BubbleImage"]["Double"] = dict()
        Registry.gameData["BubbleImage"]["Kill"] = dict()
        Registry.gameData["BubbleImage"]["SpeedUp"] = dict()
        Registry.gameData["BubbleImage"]["SpeedDown"] = dict()
        Registry.gameData["BubbleImage"]["Ultimate"] = dict()
        Registry.gameData["BubbleImage"]["Up"] = dict()
        Registry.gameData["BubbleImage"]["Teleporter"] = dict()
        Registry.gameData["BubbleImage"]["SlowMotion"] = dict()
        Registry.gameData["BubbleImage"]["DoubleState"] = dict()
        Registry.gameData["BubbleImage"]["Protect"] = dict()
        Registry.gameData["BubbleImage"]["ShotSpdStat"] = dict()
        Registry.gameData["BubbleImage"]["HyperMode"] = dict()
        Registry.gameData["BubbleImage"]["TimeBreak"] = dict()
        Registry.gameData["BubbleImage"]["Confusion"] = dict()
        Registry.gameData["BubbleImage"]["Paralyse"] = dict()
        Registry.gameData["BubbleImage"]["StoneBub"] = dict()
        Registry.gameData["BubbleImage"]["NoTouch"] = dict()
        Registry.gameData["BubbleImage"]["Key"] = dict()
        Registry.gameData["BubbleImage"]["Diamond"] = dict()
        Registry.gameData["BubbleImage"]["Present"] = dict()
        Registry.gameData["BubbleImage"]["SpecialKey"] = dict()
        from lib import utils

        _min = 21
        _max = 80

        # Adding the different resolutions to the bubbles.
        for i in range(_min, _max + 1):
            Registry.gameData["BubbleImage"]["Normal"][i] = utils.createbubble_image((i, i), None, "white")
            Registry.gameData["BubbleImage"]["Double"][i] = utils.createbubble_image((i, i), None, "gold")
            Registry.gameData["BubbleImage"]["Triple"][i] = utils.createbubble_image((i, i), None, "blue", "#007fff", "#00ffff", "white")
            Registry.gameData["BubbleImage"]["SpeedDown"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#a7a7a7", "#7f7f7f", "#373737")
            Registry.gameData["BubbleImage"]["SpeedUp"][i] = utils.createbubble_image((i, i), None, "#ffffff", "#7fff7f", "#00ff00", "#007f00")
            Registry.gameData["BubbleImage"]["Up"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#00ff00", "#00000000", "#00ff00")
            Registry.gameData["BubbleImage"]["Ultimate"][i] = utils.createbubble_image((i, i), None, "gold", "gold", "orange", "gold")
            Registry.gameData["BubbleImage"]["Kill"][i] = utils.createbubble_image((i, i), None, "#7f0000", "#7f007f", "#7f0000",)
            Registry.gameData["BubbleImage"]["Teleporter"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#ff1020", "#373737")
            Registry.gameData["BubbleImage"]["SlowMotion"][i] = utils.createbubble_image((i, i), None, "#ffffffff", "#00000000", "#000000ff")
            Registry.gameData["BubbleImage"]["DoubleState"][i] = utils.createbubble_image((i, i), None, "gold", "#00000000", "gold", "gold")
            Registry.gameData["BubbleImage"]["Protect"][i] = utils.createbubble_image((i, i), None, "#00ff00", "#3fff3f", "#7fff7f", "#9fff9f")
            Registry.gameData["BubbleImage"]["ShotSpdStat"][i] = utils.createbubble_image((i, i), None, "#ff7f00", "#ff7f00", "gold")
            Registry.gameData["BubbleImage"]["HyperMode"][i] = utils.createbubble_image((i, i), None, "black", "black", "white", "black")
            Registry.gameData["BubbleImage"]["TimeBreak"][i] = utils.createbubble_image((i, i), None, "red", "orange", "yellow", "white")
            Registry.gameData["BubbleImage"]["Confusion"][i] = utils.createbubble_image((i, i), None, "black", "purple", "magenta", "white")
            Registry.gameData["BubbleImage"]["Paralyse"][i] = utils.createbubble_image((i, i), None, "#ffff00", "#ffff00", "#ffff7f", "#ffffff")
            Registry.gameData["BubbleImage"]["StoneBub"][i] = utils.createbubble_image((i, i), None, "black", "orange", "yellow")
            Registry.gameData["BubbleImage"]["NoTouch"][i] = utils.createbubble_image((i, i), None, "#7f7f7f", "#7f7f7f", "#7f7f7f", "#373737")

            self.canvas.itemconfig(t1, text="Loading Bubbles Sizes")
            self.canvas.itemconfig(t2, text="Loading %s of %s" % (i - _min, _max - 1 - _min))
            self.canvas.update()

        # Adding the static-resolution-bubbles.
        Registry.gameData["BubbleImage"]["Key"][60] = PhotoImage(file="assets/bubbles/Key.png")
        Registry.gameData["BubbleImage"]["Diamond"][36] = PhotoImage(
            file="assets/bubbles/Diamond.png")
        Registry.gameData["BubbleImage"]["Present"][40] = PhotoImage(
            file="assets/bubbles/Present.png")
        # noinspection PyTypeChecker
        Registry.gameData["BubbleImage"]["Coin"] = PhotoImage(file="assets/CoinBub.png")
        Registry.gameData["BubbleImage"]["SpecialKey"][48] = PhotoImage(
            file="assets/bubbles/SpecialMode.png")

        for i in Registry.gameData["BubbleImage"].keys():
            print("%s: %s" % (i, repr(Registry.gameData["BubbleImage"][i])))

        # Adding ship image.
        Registry.register_image("ShipImage", PhotoImage(file="assets/Ship.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="")
        self.canvas.update()

        # Getting the store-icons.
        Registry.register_storeitem("Key", PhotoImage(file="assets/Images/StoreItems/Key.png"))
        self.canvas.itemconfig(t2, text="Store Item: Key")
        self.canvas.update()
        Registry.register_storeitem("Teleport", PhotoImage(file="assets/Images/StoreItems/Teleport.png"))
        self.canvas.itemconfig(t2, text="Store Item: Teleport")
        self.canvas.update()
        Registry.register_storeitem("Shield", PhotoImage(file="assets/Images/StoreItems/Shield.png"))
        self.canvas.itemconfig(t2, text="Store Item: Shield")
        self.canvas.update()
        Registry.register_storeitem("Diamond", PhotoImage(file="assets/Images/StoreItems/DiamondBuy.png"))
        self.canvas.itemconfig(t2, text="Store Item: Diamond")
        self.canvas.update()
        Registry.register_storeitem("BuyACake", PhotoImage(file="assets/Images/StoreItems/BuyACake.png"))
        self.canvas.itemconfig(t2, text="Store Item: Buy A Cake")
        self.canvas.update()
        Registry.register_storeitem("Pop3Bubbles", PhotoImage(file="assets/Images/StoreItems/Pop_3_bubs.png"))
        self.canvas.itemconfig(t2, text="Store Item: Pop 3 Bubbles")
        self.canvas.update()
        Registry.register_storeitem("PlusLife", PhotoImage(file="assets/Images/StoreItems/PlusLife.png"))
        self.canvas.itemconfig(t2, text="Store Item: PlusLife")
        self.canvas.update()
        Registry.register_storeitem("Speedboost", PhotoImage(file="assets/Images/StoreItems/SpeedBoost.png"))
        self.canvas.itemconfig(t2, text="Store Item: Speedboost")
        self.canvas.update()
        Registry.register_storeitem("SpecialMode", PhotoImage(file="assets/Images/StoreItems/SpecialMode.png"))
        self.canvas.itemconfig(t2, text="Store Item: Special Mode")
        self.canvas.update()
        Registry.register_storeitem("DoubleScore", PhotoImage(file="assets/Images/StoreItems/DoubleScore.png"))
        self.canvas.itemconfig(t2, text="Double Score")
        self.canvas.update()

        # Loading backgrounds
        self.canvas.itemconfig(t1, text="Loading Backgrounds")
        self.canvas.itemconfig(t2, text="Line")
        self.canvas.update()
        Registry.register_background("Line", PhotoImage(file="assets/LineIcon.png"))

        self.canvas.itemconfig(t1, text="Loading Backgrounds")
        self.canvas.itemconfig(t2, text="Normal")
        self.canvas.update()
        Registry.register_background("Normal", PhotoImage(file="assets/Images/Backgrounds/GameBG2.png"))

        self.canvas.itemconfig(t1, text="Loading Backgrounds")
        self.canvas.itemconfig(t2, text="Special Mode")
        self.canvas.update()
        Registry.register_background("Special", PhotoImage(file="assets/Images/Backgrounds/GameBG Special2.png"))

        # Loading foregrounds
        self.canvas.itemconfig(t1, text="Loading Foregrounds")
        self.canvas.itemconfig(t2, text="For Bubble Gift")
        self.canvas.update()
        Registry.register_foreground("BubbleGift", PhotoImage(file="assets/EventBackground.png"))

        self.canvas.itemconfig(t1, text="Loading Foregrounds")
        self.canvas.itemconfig(t2, text="Store FG")
        self.canvas.update()
        Registry.register_foreground("StoreFG", PhotoImage(file="assets/FG2.png"))

        # Loading Icons
        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Present Circle")
        self.canvas.update()
        Registry.register_icon("PresentCircle", PhotoImage(file="assets/Circle.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Present Chest")
        self.canvas.update()
        Registry.register_icon("PresentChest", PhotoImage(file="assets/Present.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Store: Diamond & Coin")
        self.canvas.update()
        Registry.register_icon("StoreDiamond", PhotoImage(file="assets/Diamond.png"))
        Registry.register_icon("StoreCoin", PhotoImage(file="assets/Coin.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="Pause")
        self.canvas.update()
        Registry.register_icon("Pause", PhotoImage(file="assets/Pause.png"))

        self.canvas.itemconfig(t1, text="Loading Icons")
        self.canvas.itemconfig(t2, text="SlowMotion")
        self.canvas.update()
        Registry.register_icon("EffectSlowmotion", PhotoImage(file="assets/SlowMotionIcon.png"))

        # Loading fonts
        Registry.gameData["fonts"] = {}

        self.canvas.itemconfig(t1, text="Loading Fonts")
        self.canvas.itemconfig(t2, text="Title Fonts")
        self.canvas.update()
        Registry.gameData["fonts"]["titleButtonFont"] = Font("Helvetica", 15)

        self.canvas.itemconfig(t1, text="Loading Fonts")
        self.canvas.itemconfig(t2, text="Slots Menu Fonts")
        self.canvas.update()
        Registry.gameData["fonts"]["slotsButtonFont"] = Font("Helvetica", 12)

        # Register Scenes
        Registry.register_scene("TitleScreen", TitleMenu())
        Registry.register_scene("SaveMenu", SavesMenu())
        Registry.register_scene("Store", Store())

        self.scenemanager.change_scene("TitleScreen")
        return

        # Setting background from nothing to normal.
        self.back["id"] = self.canvas.create_image(0, 0, anchor="nw", image=self.back["normal"])

        # Creating shi
        self.ship["id"] = self.canvas.create_image(7.5, 7.5, image=self.ship["image"])
        print(self.ship["id"])

        # Moving ship to position
        self.canvas.move(self.ship["id"], self.stats["Player"]["ShipStats"]["ShipPosition"][0], self.stats["Player"]["ShipStats"]["ShipPosition"][1])

        self.canvas.itemconfig(t1, text="Creating Stats objects")
        self.canvas.itemconfig(t2, text="")

        # Initializing the panels for the game.
        self.panels["game/top"] = self.canvas.create_rectangle(
            -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        )
