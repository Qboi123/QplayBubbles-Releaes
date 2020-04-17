import math
from math import sqrt
from typing import Iterable, Optional, Mapping, Sequence, Any, Union, Callable, ValuesView, TypeVar, Type, NoReturn, \
    List, ItemsView, KeysView, Tuple
from tkinter import Canvas

from overload import overload

from qbubbles.base import HORIZONTAL, VERTICAL, TYPE_NEUTRAL, FALSE, FORM_CIRCLE, LEFT, TYPE_DANGEROUS, FORM_RECT, UP, \
    DOWN, SHIP, RED, FORM_LINE
from qbubbles.effects import BaseEffect, AppliedEffect
from qbubbles.events import KeyPressEvent, KeyReleaseEvent, UpdateEvent, SavedataReadedEvent, ExperienceEvent, \
    CollisionEvent, XInputEvent, MouseEnterEvent, MouseLeaveEvent, SpriteDamageEvent
from qbubbles.registry import Registry
from qbubbles.sprite.abilities import GhostAbility, Ability, InvulnerableAbility

# noinspection PyShadowingBuiltins
_KT = TypeVar('_KT')
# noinspection PyShadowingBuiltins
_VT = TypeVar('_VT')
# noinspection PyShadowingBuiltins
_T = TypeVar('_T')
# noinspection PyShadowingBuiltins
_S = TypeVar('_S')


# noinspection PyShadowingBuiltins
class SpriteData(object):
    def __init__(self, default):
        if type(default) == dict:
            self._type: Type[dict] = dict
        else:
            raise TypeError(f"The default value is not a dict or list")
        self.default = default.copy()
        self._value = default.copy()

    def __iter__(self):
        if self._type == list:
            return self._value
        else:
            return []

    def __getitem__(self, item):
        return self._value[item]

    def __setitem__(self, item, value):
        self._value[item] = value

    def __delitem__(self, item):
        del self._value[item]

    def __setslice__(self, i, j, sequence: Sequence):
        if type(self._value) == list:
            self._value: list
            self._value[i:j] = sequence

    def __getslice__(self, i, j):
        if type(self._value) == list:
            self._value: list
            return self._value[i:j]

    def __delslice__(self, i, j):
        if type(self._value) == list:
            self._value: list
            del self._value[i:j]

    @overload
    def get(self, k: _KT) -> _VT:
        if self._type == dict:
            self._value: dict
            return self._value.get(k)

    @get.add
    def get(self, k: _KT, default: Union[_VT, _T] = None) -> Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.get(k, default)

    @overload
    def pop(self, k: _KT, default: Union[_VT, _T] = None) -> Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.pop(k, default)

    def keys(self) -> KeysView:
        if self._type == dict:
            self._value: dict
            return self._value.keys()

    def values(self) -> ValuesView:
        if self._type == dict:
            self._value: dict
            return self._value.values()

    def items(self) -> ItemsView:
        if self._type == dict:
            self._value: dict
            return self._value.items()

    @overload
    def update(self, __m: Mapping[_KT, _VT], **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(__m, **kwargs)

    @update.add
    def update(self, __m: Iterable[Tuple[_KT, _VT]], **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(__m, **kwargs)

    @update.add
    def update(self, **kwargs) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.update(**kwargs)

    @overload
    def fromkeys(self, seq: Iterable[_T]) -> dict:
        if self._type == dict:
            self._value: dict
            return self._value.fromkeys(seq)

    @fromkeys.add
    def fromkeys(self, seq: Iterable[_T], value: _T) -> dict:
        if self._type == dict:
            self._value: dict
            return self._value.fromkeys(seq, value)

    def popitem(self) -> Tuple[_KT, _VT]:
        if self._type == dict:
            self._value: dict
            return self._value.popitem()

    def setdefault(self, k: _KT, default: _VT) -> int:
        if self._type == dict:
            self._value: dict
            return self._value.setdefault(k, default)

    @pop.add
    def pop(self, k: Union[_KT, int]) -> Union[_VT, _T]:
        if self._type == dict:
            self._value: dict
            return self._value.pop(k)
        if self._type == list:
            self._value: list
            return self._value.pop(k)

    def clear(self) -> None:
        if self._type == dict:
            self._value: dict
            return self._value.clear()
        if self._type == list:
            self._value: list
            return self._value.clear()

    def copy(self) -> Union[list, dict]:
        if self._type == dict:
            self._value: dict
            return self._value.copy()
        if self._type == list:
            self._value: list
            return self._value.copy()

    def remove(self, o: _T) -> None:
        if self._type == list:
            self._value: list
            return self._value.remove(o)

    def extend(self, iterable: Iterable[_T]) -> None:
        if self._type == list:
            self._value: list
            return self._value.extend(iterable)
        self._value: list

    def count(self, object: _T) -> int:
        if self._type == list:
            self._value: list
            return self._value.count(object)

    def index(self, object: _T, start: int = None, stop: int = None) -> int:
        if self._type == list:
            self._value: list
            return self._value.index(object, start, stop)

    def reverse(self) -> None:
        if self._type == list:
            self._value: list
            return self._value.reverse()

    def insert(self, index: int, object: _T) -> None:
        if self._type == list:
            self._value: list
            return self._value.insert(index, object)

    def sort(self, *, key: Callable[[_T], Any] = None, reverse: bool) -> None:
        if self._type == list:
            self._value: list
            return self._value.sort(key=key, reverse=reverse)

    # noinspection PyShadowingBuiltins
    def append(self, object: _T):
        if self._type == list:
            self._value: list
            self._value.append(object)


# noinspection PyUnusedLocal,PyStatementEffect,PyTypeChecker
class Sprite:
    requires = ("sprites", "config", "canvas", "stats", "log", "ship", "bubbles")

    def __init__(self, **kw):
        name = "EmptySprite"

        self._kw = kw

        self.abilities: List[Ability] = []

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

        # self.collisionWith = (SHIP, ANY_BUBBLE)
        self.collisionWith: Optional[List] = None

        self.lifeCost = 1

        self.id = int()

        self._spriteName: str = None

        self.coordsLen = 2

        self._spriteData = SpriteData({})
        self._objectData = SpriteData({"Position": (None, None)})
        self.dead = False

    def __repr__(self):
        a = "<"+(", ".join(f"{repr(key)}={repr(value)}" for key, value in dict(self._objectData).items()))+">"
        return f"Sprite({repr(self.get_sname())}, data="+a+")"

    def delete(self) -> NoReturn:
        canvas: Canvas = Registry.get_scene("Game").canvas
        canvas.delete(self.id)

    def get_spritedata(self) -> SpriteData:
        return self._spriteData

    def create(self, x, y):
        Registry.get_scene("Game").gameObjects.append(self)

    def get_sname(self):
        return self._spriteName

    @staticmethod
    def _c_create_image(x, y, image, anchor="nw"):
        return Registry.get_scene("Game").canvas.create_image(x, y, image=image, anchor=anchor)

    def move(self, x, y):
        Registry.get_scene("Game").canvas.move(self.id, x, y)
        self._objectData["Position"] = self.get_coords()

    def teleport(self, x, y):
        Registry.get_scene("Game").canvas.coords(self.id, x, y)
        self._objectData["Position"] = self.get_coords()

    def get_coords(self):
        return Registry.get_scene("Game").canvas.coords(self.id)

    def attack(self, other: object):
        if not issubclass(type(other), Sprite):
            raise TypeError("argument 'other' must be a Sprite-object")
        other: Sprite
        # print(f"{self.__class__.__name__} is attacking {other.__class__.__name__}")
        if other.defenceMultiplier != 0:
            other.damage(self.attackMultiplier / other.defenceMultiplier)
        else:
            other.instant_death()

    def damage(self, value: float):
        scene = Registry.get_scene("Game")
        if not SpriteDamageEvent(scene, self).cancel:
            self.health -= value / self.defenceValue
            if self.health <= 0:
                self.dead = True

    def distance(self, to):
        canvas = Registry.get_scene("Game").canvas
        try:
            # try:
            x1, y1 = self.get_coords()
            # except ValueError:
            #     self.instant_death()
            # try:
            x2, y2 = to.get_coords()
            # except ValueError:
            #     to.instant_death()
            # print(f"POINT_1: {x1, y1}")
            # print(f"POINT_2: {x2, y2}")
            # noinspection PyUnboundLocalVariable
            return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        except ValueError:
            return math.inf
        except UnboundLocalError:
            return math.inf

    def instant_death(self):
        self.health = 0
        self.dead = True

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

    def get_objectdata(self):
        return dict(self._objectData).copy()


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()

        self.rotation = 0
        self.appliedEffects = []
        self.appliedEffectTypes = []

        self.score = 0
        self.health = 10
        self.maxHealth = 10
        self._exp = 0

        self.radius = 12.5
        self.speed = 0
        self.baseSpeed = 0

        self.keysPressed = ""
        self._spriteName = "qbubbles:player"
        self._spriteData = SpriteData({"objects": [{
                "Money": {
                    "diamonds": 0,
                    "coins": 0
                },
                "Abilities": {
                    **dict(((key, value) for key, value in Registry.get_abilities()))
                },
                "Effects": [],
                "Position": [],
                "speed": 10,
                "lives": 7,
                "score": 0,
                "high_score": 0,
                "teleports": 0,
                "level": 1
            }]})
        self._objectData = SpriteData(
            {
                "Money": {
                    "diamonds": 0,
                    "coins": 0
                },
                "Abilities": {
                    **dict(((key, value) for key, value in Registry.get_abilities()))
                },
                "Effects": [],
                "Position": [10, 10],
                "speed": 10,
                "lives": 7,
                "score": 0,
                "high_score": 0,
                "teleports": 0,
                "level": 1
            }
        )
        self.events_activated = False

        self.up = False
        self.down = False
        self.right = False
        self.left = False

    def add_effect(self, effect):
        self.appliedEffects.append(effect)
        self.appliedEffectTypes.append(type(effect))

    def activate_events(self):
        if self.events_activated:
            print("Events already activated")
            return
        print("Activating events...")
        self.events_activated = True
        KeyPressEvent.bind(self.on_key_press)
        KeyReleaseEvent.bind(self.on_key_release)
        UpdateEvent.bind(self.on_update)
        CollisionEvent.bind(self.on_collision)
        SavedataReadedEvent.bind(self.on_savedata_readed)

    def deactivate_events(self):
        if not self.events_activated:
            print("Events already deactivated")
            return
        print("Deactivating events...")
        self.events_activated = False
        KeyPressEvent.unbind(self.on_key_press)
        KeyReleaseEvent.unbind(self.on_key_release)
        UpdateEvent.unbind(self.on_update)
        CollisionEvent.unbind(self.on_collision)
        SavedataReadedEvent.unbind(self.on_savedata_readed)

    def on_collision(self, evt: CollisionEvent):
        # print(evt.collidedObj.get_sname())
        # print(evt.eventObject.get_sname())
        if evt.collidedObj.get_sname() != "qbubbles:bubble":
            evt.collidedObj.attack(evt.eventObject)  # evt.collidedObj.attackMultiplier / self.defenceMultiplier)
            evt.eventObject.attack(evt.collidedObj)
            if evt.collidedObj.get_sname() == "qbubbles:player":
                evt.collidedObj.score += int(self.radius * (self.baseSpeed / 8) / 8)
        elif evt.eventObject.get_sname() != "qbubbles:bubble":
            evt.collidedObj.attack(evt.eventObject)  # evt.collidedObj.attackMultiplier / self.defenceMultiplier)
            evt.eventObject.attack(evt.collidedObj)
            if evt.eventObject.get_sname() == "qbubbles:player":
                evt.eventObject.score += int(self.radius * (self.baseSpeed / 8) / 8)

    def add_experience(self, experience):
        ExperienceEvent(self, experience)

    def on_savedata_readed(self, data):
        self.score = data["Player"]["score"]

        for effect in data["Player"]["Effects"]:
            effect_class: BaseEffect = Registry.get_effect(effect["id"])
            time_length: float = effect["timeRemaining"]
            strength: float = effect["strength"]
            self.start_effect(effect_class, Registry.get_scene("Game"), time_length, strength)

    def start_effect(self, effect_class, scene, time_length, strength) -> NoReturn:
        self.appliedEffects.append(AppliedEffect(effect_class, scene, time_length, strength))

    def move(self, x=0, y=0):
        Registry.get_scene("Game").canvas.move(self.id, x, y)

    def move_joy(self, x=0, y=0):
        Registry.get_scene("Game").canvas.move(self.id, x, y)

    def on_update(self, evt: UpdateEvent):
        x = 0
        y = 0
        # if self.up:
        #     y -= self.baseSpeed * evt.dt
        # if self.left:
        #     x -= self.baseSpeed * evt.dt
        # if self.down:
        #     y += self.baseSpeed * evt.dt
        # if self.right:
        #     x += self.baseSpeed * evt.dt

        pixels = 0

        if self.up:
            pixels = self.baseSpeed
        if self.down:
            pixels = -self.baseSpeed
        if self.left:
            self.rotate(+(evt.dt * 160))
        if self.right:
            self.rotate(-(evt.dt * 160))

        import math

        d = -(evt.dt * pixels)  # distance covered this tick.
        angle_radians = math.radians(self.rotation)
        dx = -math.cos(angle_radians)
        dy = math.sin(angle_radians)

        dx, dy = dx * d, dy * d

        x, y = dx, dy

        # print(self.up, self.left, self.down, self.right)
        # print(x, y)
        self.move(x, y)

    def create(self, x, y):
        image = Registry.get_texture("sprite", "player", rotation=0)
        self.id = self._c_create_image(x, y, image, anchor="center")
        # self.id = Registry.get_scene("Game").canvas.create_image(x, y, image=Registry.get_texture("sprite", "player",
        #                                                                                           rotation=0))
        self.baseSpeed = 80
        self.speed = self.baseSpeed

    def _update_rot_tex(self):
        """
        Updates the rotation texture

        :return:
        """
        image = Registry.get_texture("sprite", "player", rotation=int(self.rotation - (self.rotation % 1)))
        c = Registry.get_scene("Game").canvas
        c.itemconfig(self.id, image=image)

    def rotate(self, r_rot):
        """
        Rotates the player

        :param r_rot: Rotation in degrees
        :return:
        """

        self.rotation += r_rot
        self.rotation = self.rotation % 360
        self._update_rot_tex()

    def on_key_press(self, evt: KeyPressEvent):
        """
        Key-press event handler

        :param evt:
        :return:
        """

        # print(f"PRESS1: {evt.char} | {evt.keySym}")
        if (evt.char.lower() == "w") and not self.up:
            self.up = True
        elif (evt.keySym.lower() == "up") and not self.up:
            self.up = True
        elif (evt.char.lower() == "a") and not self.left:
            self.left = True
        elif (evt.keySym.lower() == "left") and not self.left:
            self.left = True
        elif (evt.char.lower() == "s") and not self.down:
            self.down = True
        elif (evt.keySym.lower() == "down") and not self.down:
            self.down = True
        elif (evt.char.lower() == "d") and not self.right:
            self.right = True
        elif (evt.keySym.lower() == "right") and not self.right:
            self.right = True
        # TODO: Implement teleport ability for player, using key-events
        # print(self.up, self.left, self.down, self.right)

    def on_key_release(self, evt: KeyReleaseEvent):
        """
        Key-release event handler

        :param evt:
        :return:
        """

        a = list(self.keysPressed)
        # print(f"RELEASE1: {evt.char}")
        if (evt.char.lower() == "w") and self.up:
            self.up = False
        elif (evt.keySym.lower() == "up") and self.up:
            self.up = False
        elif (evt.char.lower() == "a") and self.left:
            self.left = False
        elif (evt.keySym.lower() == "left") and self.left:
            self.left = False
        elif (evt.char.lower() == "s") and self.down:
            self.down = False
        elif (evt.keySym.lower() == "down") and self.down:
            self.down = False
        elif (evt.char.lower() == "d") and self.right:
            self.right = False
        elif (evt.keySym.lower() == "right") and self.right:
            self.right = False
        # TODO: Implement teleport ability for player, using key-events

    def get_ability(self, uname):
        """
        Get ability instance from uname

        :param uname:
        :return:
        """

        if uname in self.get_spritedata()["Abilities"].keys():
            return self.get_spritedata()["Abilities"][uname]
        return None


class TeleportCrosshair(Sprite):
    def __init__(self):
        """
        Deprecated, will use ability and key-events instead.
        TODO: Remove this, and use ability and key-events instead.
        """

        super(TeleportCrosshair, self).__init__()

        self.abilities.append(GhostAbility(self))
        self.abilities.append(InvulnerableAbility(self))

    def create(self, x, y):
        super(x, y)

    def on_key_release(self, evt: KeyReleaseEvent):
        if evt.keySym.lower() == "return":
            Registry.get_mode("teleport").execute("done", x=self.get_coords()[0], y=self.get_coords()[1])


# noinspection PyAttributeOutsideInit
class Ammo(Sprite):
    requires = tuple(list(Sprite.requires) + ["ship", "ammo"])

    def __init__(self, **kw):
        """
        WORK IN PROGRESS
        TODO: Use Ammo(Sprite) class for shooting, and improve performance of the Ammo Sprite.

        :param kw:
        """
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

    def on_collide_bubble(self, index):
        """
        FIXME: Rename method to allow compatibility with base sprite

        :param index:
        :return:
        """

        from qbubbles.components import StoppableThread
        from qbubbles.bubble import del_bubble
        from qbubbles.extras import replace_list, distance
        from qbubbles.ammo import del_ammo

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
                    # # TODO: Replace with something like pygame's mixer'
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

    def create(self, x, y):
        id_ = self._kw["ship"]["id"]
        x, y = self._kw["canvas"].coords(id_)

        self.id = self._kw["canvas"].create_line(x + 7, y, x + 12, y, fill="gold")
        self._kw["ammo"]["ammo-id"][self.id] = self.id
        self._kw["ammo"]["ammo-speed"][self.id] = 5
        self._kw["ammo"]["ammo-damage"][self.id] = 0
        super().create(x, y)


# noinspection PyRedundantParentheses
class BaseBarier(Sprite):
    def __init__(self, **kw):
        """
        WORK IN PROGRESS

        :param kw:
        """
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
        """
        TODO: Use Images instead (Pillow / Tkinter.PhotoImage).

        :param x:
        :param y:
        :return:
        """

        self.id = self._kw["canvas"].create_rectangle(x, y + 72, x + 10, y + 222, fill=RED, outline=RED)
        # print(self.parent.canvas.coords(self.id))
        super().create(x, 72 + y)
