import string
from tkinter import Canvas
from typing import Optional, List, NoReturn

from qbubbles.sprites import Sprite, SpriteData
from qbubbles.exceptions import UnlocalizedNameError
from qbubbles.registry import Registry
from qbubbles.sprites import Player


class Bubble(object):
    def __init__(self):
        self.priority = 0

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 10
        self.hardness: int = 1
        self.damage: int = 1
        self._uName: Optional[str] = None

    def set_uname(self, name) -> NoReturn:
        for symbol in name:
            if symbol not in string.ascii_letters + string.digits + "_" + ":":
                raise UnlocalizedNameError(f"Invalid character '{symbol}' for unlocalized name '{name}'")
        if name[0] not in string.ascii_letters:
            raise UnlocalizedNameError(f"Invalid start character '{name[0]}' for unlocalized name '{name}'")
        if name[-1] not in string.ascii_letters + string.digits:
            raise UnlocalizedNameError(f"Invalid start character '{name[-1]}' for unlocalized name '{name}'")

        self._uName = name

    def get_uname(self) -> str:
        return self._uName

    def get_uname_registry(self) -> List[str]:
        return Registry.get_id_bubble(self)

    def __repr__(self) -> str:
        return f"Bubble<{self.get_uname()}>"


class BubbleObject(Sprite):
    def __init__(self, base_class: Bubble = None, max_health=5):
        super(BubbleObject, self).__init__()

        self._spriteName = "qbubbles:bubble"
        self._spriteData = SpriteData({"Bubbles": [], "speed_multiplier": 0.5, "id": self.get_sname()})

        self.baseSpeed: Optional[int] = None
        self.baseClass: Bubble = base_class
        self.maxHealth = max_health
        self.imageList = {}
        self.id: Optional[int] = None

        if base_class is not None:
            self.imageList = Registry.get_bubresource(self.baseClass.get_uname(), "images")

    def create(self, x, y, radius=5, speed=5, health=5):
        if self.baseClass is None:
            raise UnlocalizedNameError(f"BubbleObject is used for Sprite information, use the base_class argument with "
                                       f"a Bubble-instance instead of NoneType to fix this problem")
        if self.id is not None:
            raise OverflowError(f"BubbleObject is already created")
        canvas: Canvas = Registry.get_scene("Game").canvas
        self.baseSpeed = speed
        self.health = health
        self.id = canvas.create_image(x, y, image=Registry.get_texture("qbubbles:bubble", self.baseClass.get_uname()))


class NormalBubble(Bubble):
    def __init__(self):
        super(NormalBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12
        self.scoreMultiplier: float = 1
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:normal_bubble")


class DoubleBubble(Bubble):
    def __init__(self):
        super(DoubleBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12
        self.scoreMultiplier: float = 2
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:double_value")


class TripleBubble(Bubble):
    def __init__(self):
        super(TripleBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12
        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:triple_value")


class DoubleStateBubble(Bubble):
    def __init__(self):
        super(DoubleStateBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12

        self.scoreMultiplier: float = 2
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:double_state")


class TripleStateBubble(Bubble):
    def __init__(self):
        super(TripleStateBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12

        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:triple_state")


class DamageBubble(Bubble):
    def __init__(self):
        super(DamageBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 21
        self.maxRadius: int = 80
        self.minSpeed: int = 5
        self.maxSpeed: int = 12

        self.scoreMultiplier: float = 0.5
        self.attackMultiplier: float = 1

        self.set_uname("qbubbles:damage_bubble")


class SpeedupBubble(Bubble):
    def __init__(self):
        super(SpeedupBubble, self).__init__()

        self.priority = 1500000

        self.minRadius: int = 5
        self.maxRadius: int = 50
        self.minSpeed: int = 29
        self.maxSpeed: int = 57

        self.scoreMultiplier: float = 3
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:speedup")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Sprite):
        if other_object.get_sname() == "player":
            other_object: Player
            if other_object.baseSpeed < 20:
                other_object.baseSpeed += int((bubbleobject.radius / 5) + 5)


class TeleportBubble(Bubble):
    def __init__(self):
        super(TeleportBubble, self).__init__()

        self.priority = 10

        self.minRadius: int = 5
        self.maxRadius: int = 30
        self.minSpeed: int = 34
        self.maxSpeed: int = 51

        self.scoreMultiplier: float = 1
        self.attackMultiplier: float = 0

        self.set_uname("qbubbles:teleport_bubble")

    def on_collision(self, bubbleobject: BubbleObject, other_object: Player):
        if other_object.get_sname() == "player":
            other_object.get_ability("qbubbles:teleport")["value"] = \
                bubbleobject.baseSpeed / bubbleobject.baseClass.maxSpeed * 2
