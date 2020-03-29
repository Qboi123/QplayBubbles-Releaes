from tkinter import Canvas, Frame
from typing import Optional, Union, Callable, Type, List, Tuple

from events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, MouseEnterEvent, \
    MouseLeaveEvent, ResizeEvent
from globals import CANVAS
from registry import Registry
from sprite.abilities import Ability

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

TYPE_DANGEROUS = "dangerous"
TYPE_NEUTRAL = "neutral"

FORM_CIRCLE = "circle"
FORM_RECT = "rectangle/line"
FORM_LINE = "rectangle/line"

BUB_NOSTATE = "nostate"
BUB_WITHSTATE = "withstate"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

TRUE = True
FALSE = False

COLOR_RED = "red"

RED = COLOR_RED

ANY_BUBBLE = "any.bubble"
SHIP = "ship"

OBJ_SHIP = SHIP
OBJ_ANY_BUBBLE = ANY_BUBBLE
OBJ_BARIER = "barier"


# noinspection PyMissingConstructor
class StoreItem:
    def __init__(self, parent):
        self.parent = parent
        self.coins = 0
        self.diamonds = 0

    def __repr__(self):
        return f"StoreItem<{self.__class__.__name__}>"

    def on_buy(self, parent):
        pass

    def on_select(self, parent):
        pass


class Event:
    def __init__(self):
        pass

    def on_update(self, parent):
        pass

    def on_t_update(self, parent):
        pass


DirectionWaring = Warning


# noinspection PyUnusedLocal,PyStatementEffect,PyTypeChecker
class Sprite:
    requires = ("sprites", "config", "canvas", "stats", "log", "ship", "bubbles")

    def __init__(self, **kw):
        name = "EmptySprite"

        self._kw = kw

        self.abilities: List[Ability] =[]

        # Axis
        self.axis = (HORIZONTAL, VERTICAL)

        # Has- variables
        self.hasSkin = True
        self.hasMovetag = True

        # Type
        self.type = TYPE_NEUTRAL
        self.shoots = FALSE
        self.form = FORM_CIRCLE

        # Info
        self.radius = int()
        self.height = int()
        self.width = int()

        # Direction movement
        self.returnBorder = True
        self.direction = LEFT

        # HP System
        self.health = 1
        self.maxHealth = 1
        self.regenValue = 1
        self.attackValue = 0
        self.defenceValue = 1
        self.regenMultiplier = 0
        self.attackMultiplier = 1
        self.defenceMultiplier = 1

        # x and y, move and speed variables
        self.xMove = -3
        self.xSpeed = 3
        self.yMove = 0
        self.ySpeed = 0

        self.collisionWith = (SHIP, ANY_BUBBLE)

        self.lifeCost = 1

        self.id = int()

        self._spriteName: str = None

        self.coordsLen = 2

        self.__active = False

    def create(self, x, y):
        pass

    def get_sname(self):
        return self._spriteName

    @staticmethod
    def _c_create_image(x, y, image, anchor="nw"):
        return Registry.get_scene("Game").canvas.create_image(x, y, image=image, anchor=anchor)

    def move(self, x, y):
        Registry.get_scene("Game").canvas.move(self.id, x, y)

    def teleport(self, x, y):
        Registry.get_scene("Game").canvas.coords(self.id, x, y)

    def get_coords(self):
        return Registry.get_scene("Game").canvas.coords(self.id)

    def attack(self, other: object):
        if type(other) != Sprite:
            raise TypeError("argument 'other' must be a Sprite-object")
        other: Sprite
        other.damage(self.attackValue * self.attackMultiplier)

    def damage(self, value: float):
        self.health -= value / self.defenceValue

    def on_collision(self, evt: CollisionEvent):
        pass

    def on_keypress(self, evt: KeyPressEvent):
        pass

    def on_keyrelease(self, evt: KeyReleaseEvent):
        pass

    def on_xboxcontrol(self, evt: XInputEvent):
        pass

    def on_mouseenter(self, evt: MouseEnterEvent):
        pass

    def on_mouseleave(self, evt: MouseLeaveEvent):
        pass

    def on_update(self, evt: UpdateEvent):
        pass


# noinspection PyRedundantParentheses
class BaseBarier(Sprite):
    def __init__(self, **kw):
        from random import randint, choice
        self._kw = kw
        super().__init__(**kw)
        self.direction = choice([UP, DOWN])
        self.has_skin = True
        self.has_movetag = True
        self.axis = [VERTICAL]
        self.type = TYPE_DANGEROUS
        self.form = FORM_RECT
        self.direction = UP
        self.__speed = randint(80, 104)
        self.x_speed = 0
        self.y_speed = self.__speed
        self.x_move = 0
        self.y_move = self.__speed
        self.height = 100
        self.width = 10
        self.collision_with = [SHIP]

    def create(self, x, y):
        self.id = self._kw["canvas"].create_rectangle(x, y + 72, x + 10, y + 222, fill=RED, outline=RED)
        # print(self.parent.canvas.coords(self.id))
        super().create(x, 72 + y)


# noinspection PyMethodOverriding
class Bubble(Sprite):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = ""
        self.min = 9
        self.max = 60
        self.bubtype = BUB_NOSTATE
        self.hardness = 1
        self.images = dict()
        self.collision_with = []
        self.life_cost = 0
        self.form = FORM_CIRCLE
        self.coords_len = 2

    def pre_initialize(self):
        pass

    def create(self, x: int, y: int, r: int, s: int, **kw):
        r = max(min(r, self.min), self.max)
        self.ids = [self._kw["bubbles"]["canvas"].create_image(x, y, image=self.images[r * 2])]
        self.speed = s
        self._kw["bubbles"]["bubbles"]["bub-special"].append(False)
        self._kw["bubbles"]["bubbles"]["bub-index"].append(self)
        self._kw["bubbles"]["bubbles"]["bub-position"].append([x, y])
        self._kw["bubbles"]["bubbles"]["bub-hardness"].append(self.hardness)
        self._kw["bubbles"]["bubbles"]["bub-action"].append(self.name)
        self._kw["bubbles"]["bubbles"]["bub-id"].append(self.ids)
        self._kw["bubbles"]["bubbles"]["bub-radius"].append(r)
        self._kw["bubbles"]["bubbles"]["bub-speed"].append(s)
        self.index = self._kw["bubbles"]["bubbles"]["bub-id"].index(self.ids, 0, len(self._kw["bubbles"]["bubbles"]["bub-id"]))

    def on_move(self, parent):
        pass

    def on_collision(self, parent):
        from bubble import del_bubble
        del_bubble(self.index, self._kw["bubbles"], self._kw["canvas"])

    def pop(self):
        pass


ActionIsNoneWarning = Warning


class StatusBubble(Bubble): 
    requires = tuple(list(Bubble.requires) + ["back"])

    def __init__(self, **kw):
        super().__init__(**kw)
        self._kw = kw
        self.name = None

    def on_collfunc(self):
        from state import State
        if self.name is None:
            raise ActionIsNoneWarning("The name on status-bubble '%s' is None" % __name__)
        State.set_state(self._kw["canvas"], self._kw["log"], self._kw["stats"], self._kw["name"], self._kw["back"])


class Ammo(Sprite):
    requires = tuple(list(Sprite.requires) + ["ship", "ammo"])

    def __init__(self, **kw):
        super().__init__(**kw)
        self._kw = kw
        self.form = FORM_LINE
        self.return_border = FALSE
        self.direction = LEFT
        self.axis = [VERTICAL]
        self.x_speed = 60
        self.x_move = 60
        self.y_speed = 0
        self.y_move = 0
        self.height = 1
        self.width = 5

    def destroy(self):
        try:
            self.thread4.stop()
        except AttributeError:
            pass
        super().destroy()

    def on_collide_bubble(self, index):
        from tkinter import TclError
        from components import StoppableThread
        from bubble import del_bubble
        from extras import replace_list, distance
        from ammo import del_ammo

        log = self._kw["log"]
        ammo = self._kw["ammo"]
        root = self._kw["root"]
        texts = self._kw["texts"]
        stats = self._kw["stats"]
        canvas = self._kw["canvas"]
        panels = self._kw["panels"]
        bubble = self._kw["bubbles"]
        commands = self._kw["commands"]
        coll_func = self._kw["Coll"].coll_func
        ammo_index = self.id
        backgrounds = self._kw["back"]

        index_bub = index
        try:
            if distance(canvas, log, ammo["ammo-id"][ammo_index], bubble["bub-id"][index_bub][0]) < (
                    1 + bubble["bub-radius"][index_bub]):
                if bubble["bub-hardness"][index_bub] == 1:
                    try:
                        self.thread4 = StoppableThread(
                            None,
                            lambda: coll_func(index_bub, canvas, commands, root, log,
                                              stats,
                                              (bubble["bub-radius"][index_bub] +
                                               bubble["bub-speed"][index_bub]),
                                              bubble["bub-action"][index_bub], bubble,
                                              backgrounds,
                                              texts, panels, False),
                            __name__ + ".CollisionFunction").start()
                    except IndexError:
                        pass
                    del_bubble(index_bub, bubble, canvas)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                    # Thread(None, PlaySound("versions/"+self.launcher_config["versionDir"]+"/assets/bubpop.wav", 1)).start()
                elif bubble["bub-hardness"][index_bub] > 1:
                    replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                root.update()
        except TypeError:
            pass
        except IndexError:
            pass
        except AttributeError:
            self.destroy()
        except TclError:
            self.destroy()

    def create(self, x, y):
        id = self._kw["ship"]["id"]
        x, y = self._kw["canvas"].coords(id)

        self.id = self._kw["canvas"].create_line(x+7, y, x+12, y, fill="gold")
        self._kw["ammo"]["ammo-id"][self.id] = self.id
        self._kw["ammo"]["ammo-speed"][self.id] = 5
        self._kw["ammo"]["ammo-damage"][self.id] = 0
        super().create(x, y)


class Player(Sprite):
    def __init__(self):
        super().__init__()
        UpdateEvent.bind(self.on_update)

    def move(self, x=0, y=0):
        CANVAS.move(self.id, x, y)

    def move_joy(self, x=0, y=0):
        CANVAS.move(self.id, x, y)

    def on_update(self, evt: UpdateEvent):
        pass


class CRectangle(object):
    def __init__(self, canvas: Canvas, x1, y1, x2, y2, fill="", outline="", anchor="center", tags=tuple()):
        self._id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline, anchor=anchor)
        self._canvas = canvas

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    def coords(self, x1, y1, x2, y2) -> Optional[Tuple[float, float, float, float]]:
        return self._canvas.coords(self._id, x1, y1, x2, y2)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, fill=None, outline=None, anchor=None, tags=None):
        return self._canvas.itemconfigure(self._id, fill=fill, outline=outline, anchor=anchor, tags=tags)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class Panel(CRectangle):
    def __init__(self, canvas, x, y, width, height, fill="", outline=""):
        self._width = width
        self._height = height
        if width == "extend":
            width = canvas.winfo_width() - x
        if height == "expand":
            height = canvas.winfo_height() - y
        self.x = x
        self.y = y
        super(Panel, self).__init__(canvas, x, y, width, height, fill=fill, outline=outline, anchor="nw")

    def on_resize(self, event: ResizeEvent):
        # noinspection PyDeepBugsBinOperand
        if self._width == "extend":
            width = self._canvas.winfo_width() - self.x
        if self._height == "expand":
            height = self._canvas.winfo_height() - self.y
        self.coords(self.x, self.y, self._width, self._height)
