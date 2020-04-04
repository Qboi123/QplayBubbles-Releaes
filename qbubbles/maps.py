import os
from random import Random
from tkinter import Canvas
from typing import Dict, Tuple, Optional, List

from qbubbles.bubbleSystem import BubbleSystem
from qbubbles.bubbles import Bubble, BubbleObject
from qbubbles.config import Reader
from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, \
    MapInitializeEvent, FirstLoadEvent, SaveEvent, LoadCompleteEvent, GameExitEvent
from qbubbles.gameIO import printerr
from qbubbles.gui import CPanel, CEffectBarArea
from qbubbles.nzt import NZTFile
from qbubbles.registry import Registry
from qbubbles.sprites import Sprite, Player
from qbubbles.utils import Font


class GameMap(object):
    def __init__(self):
        self._bubbles = []
        self._gameobjects = []
        self.player: Optional[Player] = None
        self.seedRandom = None
        self.randoms: Dict[str, Tuple[Random, int]] = {}
        self._uname = None
        
        MapInitializeEvent.bind(self.on_mapinit)
        FirstLoadEvent.bind(self.on_firstload)
        LoadCompleteEvent.bind(self.on_loadcomplete)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        pass

    def get_gameobjects(self) -> List[Sprite]:
        return self._gameobjects

    @staticmethod
    def get_bubbles():
        return Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"]

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
        self.add_random("qbubbles:bubble_radius", 32)
        self.add_random("qbubbles:bubble_speed", 64)
        self.add_random("qbubbles:bubble_x", 128)
        self.add_random("qbubbles:bubble_y", 256)

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

    def create_random_bubble(self, *, x=None, y=None):
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble_x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble_y"][0].randint(0 - radius, h + radius)
        self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)

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
        self._bubbles.append(bubble_object)
        self._gameobjects.append(bubble_object)

    def delete_bubble(self, bubble_object: BubbleObject):
        self._bubbles.remove(bubble_object)
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

    def load_savedata(self, path):
        raise RuntimeError("Default Game Map does not support loading savedata")

    def save_savedata(self, path):
        raise RuntimeError("Default Game Map does not support saving savedata")

    def create_savedata(self, path, seed):
        raise RuntimeError("Default Game Map does not support creating savedata")


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
        self.add_random("qbubbles:bubble_radius", 32)
        self.add_random("qbubbles:bubble_speed", 64)
        self.add_random("qbubbles:bubble_x", 128)
        self.add_random("qbubbles:bubble_y", 256)
        
    def on_firstload(self, evt: FirstLoadEvent):
        print("Create bubbles because the save is loaded for first time")

        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]
        for i in range(self.maxBubbles):
            self.create_random_bubble()
        Registry.saveData["Game"]["GameMap"]["initialized"] = True
        self.player.teleport(Registry.gameData["MiddleX"], Registry.gameData["MiddleY"])

    def on_mapinit(self, evt: MapInitializeEvent):
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        self.seedRandom = Registry.saveData["Game"]["GameMap"]["seed"]
        self.init_defaults()

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

        self.background = CPanel(canvas, 0, 71, "extend", "expand", fill="#00a7a7", outline="#00a7a7")

        LoadCompleteEvent.bind(self.on_loadcomplete)

        bubbles = Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"].copy()
        Registry.saveData["Sprites"]["qbubbles:bubble"]["objects"] = []
        for bubble in bubbles:
            bub = Registry.get_bubble(bubble["id"])
            pos = bubble["pos"]
            x = pos[0]
            y = pos[1]
            rad = bubble["radius"]
            spd = bubble["speed"]
            hlt = bubble["health"]
            self.create_bubble(x, y, bub, rad, spd, hlt)

        self.player = Player()
        self.player.create(*Registry.saveData["Sprites"]["qbubbles:player"]["objects"][0]["Position"])
        self._gameobjects.append(self.player)
        self.canvas = canvas

    def on_update(self, evt: UpdateEvent):
        if len(self._bubbles) < self.maxBubbles:
            bubbleObject, radius, speed = self.get_random_bubble()
            w = Registry.gameData["WindowWidth"]
            h = Registry.gameData["WindowHeight"]

            x = w + radius
            y = self.randoms["qbubbles:bubble_y"][0].randint(71 + radius, h - radius)
            self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
        self.canvas.itemconfig(self.texts["level"], text=f"{self.player.get_objectdata()['level']}")
        self.canvas.itemconfig(self.texts["lives"], text=f"{round(self.player.health, 1)}")
        self.canvas.itemconfig(self.texts["score"], text=f"{self.player.score}")
        # self.texts["score"] = self.player.score
        for bubble in self._bubbles.copy():
            bubble: BubbleObject
            if not bubble.dead:
                # print((-bubble.radius))
                if bubble.get_coords()[0] < -bubble.radius:
                    bubble.instant_death()
            else:
                self._gameobjects.remove(bubble)
                self._bubbles.remove(bubble)

    def create_random_bubble(self, *, x=None, y=None):
        bubbleObject, radius, speed = self.get_random_bubble()
        w = Registry.gameData["WindowWidth"]
        h = Registry.gameData["WindowHeight"]

        if x is None:
            x = self.randoms["qbubbles:bubble_x"][0].randint(0 - radius, w + radius)
        if y is None:
            y = self.randoms["qbubbles:bubble_y"][0].randint(71 + radius, h - radius)
        self.create_bubble(x, y, bubbleObject, radius, speed, bubbleObject.maxHealth)

    def on_loadcomplete(self, evt: LoadCompleteEvent):
        UpdateEvent.bind(self.on_update)
        # CleanUpEvent.bind(self.on_cleanup)
        GameExitEvent.bind(self.on_gameexit)
        LoadCompleteEvent.unbind(self.on_loadcomplete)

        self.player.activate_events()

    def on_gameexit(self, evt: GameExitEvent):
        print("Exiting Game - Game Map")
        UpdateEvent.unbind(self.on_update)
        # CleanUpEvent.unbind(self.on_cleanup)
        GameExitEvent.unbind(self.on_gameexit)

        self.player.deactivate_events()

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

    def load_savedata(self, path):
        Registry.saveData["SpriteInfo"] = Reader(f"{path}/spriteinfo.nzt").get_decoded()
        Registry.saveData["Sprites"] = {}

        # Get Sprite data
        for sprite_id in Registry.saveData["SpriteInfo"]["Sprites"]:
            sprite_path = sprite_id.replace(":", "/")
            data = Reader(f"{path}/sprites/{sprite_path}.nzt").get_decoded()
            Registry.saveData["Sprites"][sprite_id] = data

    def save_savedata(self, path):
        for sprite in self.get_gameobjects():
            Registry.saveData["Sprites"][sprite.get_sname()]["objects"] = sprite.get_objectdata()

        game_data = Registry.saveData["Game"]
        sprite_info_data = Registry.saveData["SpriteInfo"]
        sprite_data = Registry.saveData["Sprites"]

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = sprite_info_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{path}/sprites/")

        for sprite in sprite_data.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = sprite_data[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

    def create_savedata(self, path, seed):
        game_data = {
            "GameInfo": {
                "seed": seed
            },
            "GameMap": {
                "id": self.get_uname(),
                "seed": seed,
                "initialized": False,
                "Randoms": []
            }
        }

        spriteinfo_data = {
            "qbubbles:bubble": {
                "speedMultiplier": 5
            },
            "Sprites": [
                sprite.get_sname() for sprite in Registry.get_sprites()
            ]
        }

        spriteData = dict()
        for sprite in Registry.get_sprites():
            spriteData[sprite.get_sname()] = sprite.get_spritedata().default

        Registry.saveData = {"GameData": game_data, "SpriteInfo": spriteinfo_data, "SpriteData": spriteData}

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile(f"{path}/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        sprite_info_file = NZTFile(f"{path}/spriteinfo.nzt", "w")
        sprite_info_file.data = spriteinfo_data
        sprite_info_file.save()
        sprite_info_file.close()

        os.makedirs(f"{path}/sprites/", exist_ok=True)

        for sprite in spriteData.keys():
            sprite_path = '/'.join(sprite.split(":")[:-1])
            if not os.path.exists(f"{path}/sprites/{sprite_path}"):
                os.makedirs(f"{path}/sprites/{sprite_path}", exist_ok=True)
            sprite_data_file = NZTFile(
                f"{path}/sprites/"
                f"{sprite.replace(':', '/')}.nzt",
                "w")
            sprite_data_file.data = spriteData[sprite]
            sprite_data_file.save()
            sprite_data_file.close()

        game_data_file = NZTFile(f"{path}/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()

