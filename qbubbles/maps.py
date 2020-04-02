import os
from random import Random
from tkinter import Canvas
from typing import Dict, Tuple, Optional

from qbubbles.nzt import NZTFile

from qbubbles.gui import CPanel, CEffectBarArea
from qbubbles.utils import Font
from qbubbles.bubbles import Bubble, BubbleObject
from qbubbles.gameIO import printerr
from qbubbles.bubbleSystem import BubbleSystem
from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, \
    MapInitializeEvent, FirstLoadEvent, SaveEvent
from qbubbles.registry import Registry


class GameMap(object):
    def __init__(self):
        self.__bubbles = property(self.get_bubbles)
        self.seedRandom = None
        self.randoms: Dict[str, Tuple[Random, int]] = None
        self._uname = None
        
        MapInitializeEvent.bind(self.on_mapinit)

    @staticmethod
    def get_bubbles():
        return Registry.saveData["Sprites"]["qbubbles:bubble"]["Bubbles"]

    def create(self, seed, randoms=None):
        self.seedRandom = seed
        self.randoms: Dict[str, Tuple[Random, int]] = {}
        if randoms is not None:
            for random in randoms:
                randomState = random["State"]
                offset = random["offset"]
                id_ = random["id"]
                self.randoms[id_] = (Random(self.seedRandom << offset).setstate(randomState), offset)
        else:
            self.init_defaults()
        self._uname = None

    def add_random(self, id_, offset):
        if id_.count(":") != 1:
            printerr(f"Randomizer id must contain a single COLON, id: {id_}")
        self.randoms[id_] = self.format_random(offset)

    def init_defaults(self):
        self.add_random("qbubbles:bubble_system", 4096)

    def on_mapinit(self, evt: MapInitializeEvent):
        pass

    def on_firstload(self, evt: FirstLoadEvent):
        pass

    def format_random(self, offset):
        if offset % 4 == 0:
            return Random(self.seedRandom << offset), offset
        else:
            raise ValueError("Offset must be multiple of 4")

    def __setattr__(self, key, value):
        if key == "format_random":
            if value != self.format_random:
                raise PermissionError("Cannot set format_random")
        self.__dict__[key] = value

    def set_uname(self, uname):
        self._uname = uname

    def get_uname(self):
        return self._uname

    def get_save_data(self):
        randoms = []
        for id, data in self.randoms.items():
            sdata = {}
            random: Random = data[0]
            sdata["State"] = random.getstate()
            sdata["offset"] = data[1]
            sdata["id"] = id
            randoms.append(sdata)

    def create_random_bubble(self, x=None, y=None):
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble_x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble_y"][0].randint(0 - radius, h + radius)
        bubbleObject.create(
            x=x, y=y, radius=radius, speed=speed, health=bubbleObject.health % (bubbleObject.maxHealth + 1))
        self.__bubbles.append(bubbleObject)

    def get_random_bubble(self) -> Tuple[BubbleObject, float, float]:
        bubble: Bubble = BubbleSystem.random(self.randoms["qbubbles:bubble_system"][0])
        radius = self.randoms["qbubbles:bubble_radius"][0].randint(bubble.minRadius, bubble.maxRadius)
        speed = self.randoms["qbubbles:bubble_speed"][0].randint(bubble.minSpeed, bubble.maxSpeed)

        max_health = 1
        if hasattr(bubble, "maxHealth"):
            max_health = bubble.maxHealth

        return BubbleObject(bubble, max_health), radius, speed

    def create_bubble(self, x: int, y: int, bubble_object: BubbleObject, radius: float, speed: float, health: float):
        bubble_object.create(x=x, y=y, radius=radius, speed=speed, health=health)
        self.__bubbles.append(bubble_object)

    def delete_bubble(self, bubble_object: BubbleObject):
        self.__bubbles.remove(bubble_object)
        bubble_object.delete()

    def on_update(self, evt: UpdateEvent):
        pass

    # def on_playermotion(self, evt: PlayerMotionEvent):
    #     pass

    def on_collision(self, evt: CollisionEvent):
        pass

    def on_keypress(self, evt: KeyPressEvent):
        pass

    def on_keyrelease(self, evt: KeyReleaseEvent):
        pass

    def on_xinput(self, evt: XInputEvent):
        pass

    def __repr__(self):
        return f"GameMap<{self.get_uname()}>"


class ClassicMap(GameMap):
    def __init__(self):
        super(ClassicMap, self).__init__()

        self.set_uname("qbubbles:classic_map")
        self.maxBubbles = 100
        self.texts = {}
        self.panelTop: Optional[CPanel] = None
        self.tSpecialColor = "#ffffff"
        self.tNormalColor = "#3fffff"

    def init_defaults(self):
        self.add_random("qbubbles:bubble_system", 4)
        self.add_random("qbubbles:bubble_system.start_x", 8)
        self.add_random("qbubbles:bubble_system.start_y", 12)
        
    def on_firstload(self, evt: FirstLoadEvent):
        print("Create bubbles because the save is loaded for first time")

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]
        for i in range(self.maxBubbles):
            self.randoms["qbubbles:bubble_system.start_x"][0].randint(-100, w + 100)
            self.randoms["qbubbles:bubble_system.start_y"][0].randint(-100, h + 100)
            self.create_random_bubble()
        Registry.saveData["Game"]["GameMap"]["initialized"] = True

    def on_mapinit(self, evt: MapInitializeEvent):
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        canvas: Canvas = evt.canvas

        t1 = evt.t1
        t2 = evt.t2

        # noinspection PyUnusedLocal
        self.panelTop = CPanel(canvas, 0, 0, width="extend", height=69, fill="darkcyan", outline="darkcyan")
        # print(f"Panel Top created: {self.panelTop}")
        panelTopFont = Font("Helvetica", 12)

        # # Initializing the panels for the game.
        # self.panels["game/top"] = canvas.create_rectangle(
        #     -1, -1, Registry.gameData["WindowWidth"], 69, fill="darkcyan"
        # )

        # Create seperating lines.
        canvas.create_line(0, 70, Registry.gameData["WindowWidth"], 70, fill="lightblue")
        canvas.create_line(0, 69, Registry.gameData["WindowWidth"], 69, fill="lightblue")

        canvas.create_text(
            55, 30, text=Registry.get_lname("info", "score"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Score")
        canvas.create_text(
            110, 30, text=Registry.get_lname("info", "level"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Level")
        canvas.create_text(
            165, 30, text=Registry.get_lname("info", "speed"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Speed")
        canvas.create_text(
            220, 30, text=Registry.get_lname("info", "lives"),
            fill=self.tSpecialColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Lives")

        CEffectBarArea(canvas, gamemap=self)

        canvas.create_text(1120, 30, text=Registry.gameData["language"]["info.tps"],
                           fill=self.tNormalColor, font=panelTopFont.get_tuple())
        canvas.itemconfig(t2, text="Teleports")

        # Coin / Diamond icons
        canvas.create_image(1185, 30, image=Registry.get_icon("StoreDiamond"))
        canvas.itemconfig(t2, text="Diamonds")
        canvas.create_image(1185, 50, image=Registry.get_icon("StoreCoin"))
        canvas.itemconfig(t2, text="Coins")

        canvas.itemconfig(t1, text="Creating Stats Data")
        canvas.itemconfig(t2, text="")

        # Game information values.
        self.texts["score"] = canvas.create_text(55, 50, fill="cyan")
        canvas.itemconfig(t2, text="Score")
        self.texts["level"] = canvas.create_text(110, 50, fill="cyan")
        canvas.itemconfig(t2, text="Level")
        self.texts["speed"] = canvas.create_text(165, 50, fill="cyan")
        canvas.itemconfig(t2, text="Speed")
        self.texts["lives"] = canvas.create_text(220, 50, fill="cyan")
        canvas.itemconfig(t2, text="Lives")



        self.texts["shiptp"] = canvas.create_text(w-20, 10, fill="cyan")
        canvas.itemconfig(t2, text="Teleports")
        self.texts["diamond"] = canvas.create_text(w-20, 30, fill="cyan")
        canvas.itemconfig(t2, text="Diamonds")
        self.texts["coin"] = canvas.create_text(w-20, 50, fill="cyan")
        canvas.itemconfig(t2, text="Coins")
        self.texts["level-view"] = canvas.create_text(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"],
                                                      fill='Orange',
                                                      font=Font("Helvetica", 46).get_tuple())
        canvas.itemconfig(t2, text="Level View")

    def on_save(self, evt: SaveEvent):
        game_data = Registry.saveData["Game"].copy()
        game_data["GameMap"]["Randoms"] = self.randoms
        sprites_data = Registry.saveData["Sprites"].copy()
        sprite_info_data = Registry.saveData["SpriteInfo"].copy()

        save_path = f"{Registry.gameData['launcherConfig']['gameDir']}saves/{evt.saveName}"

        game_data_file = NZTFile(f"{save_path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{save_path}/spriteinfo.nzt", "w")
        sprite_info_file.data = sprite_info_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{save_path}/sprites/")

        for sprite in sprites_data.keys():
            path = '/'.join(sprite.split(":")[:-1])
            os.makedirs(f"{save_path}/sprites/{path}")
            sprite_data_file = NZTFile(f"{save_path}/sprites/{sprite.replace(':', '/')}.nzt", "w")
            sprite_data_file.data = sprites_data[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

