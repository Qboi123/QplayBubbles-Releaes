from PIL.ImageTk import PhotoImage
from shapely.geometry import Point

from .base import *
from .player import Player
from lib import globals as g
from .stats import get_stats
from .utils import seedint


class Bubble(object):
    def __init__(self):
        self.rarity: int = 100

        # Define HP
        self.health: float = 0.5

        # Define Multipliers
        self.scoreMultiplier: int = 1
        self.attackMultiplier: int = 0
        self.defenceMultiplier: int = 1
        self.speedMultiplier: int = 1

        # Define Collisions
        self.collisionable: bool = True
        self.collisionWith: list = ["player"]

        # Define Movement
        self.moveAxis = AXIS_HORIZONTAL
        self.returnBorder = False

        # Define Look
        self.type = TYPE_IMAGE
        self.form = FORM_CIRCLE

        # Image
        self._image: Union[PhotoImage, None] = None

    def set_unlocalized_name(self, name):
        if name in g.NAME2BUBBLE.keys():
            raise ValueError(f"Name already used: '{name}'")
        if name in g.BUBBLE2NAME.values():
            raise ValueError(f"Name already used: '{name}'")
        if self in g.NAME2BUBBLE.values():
            raise ValueError(f"Unlocalized name already set")
        if self in g.BUBBLE2NAME.keys():
            raise ValueError(f"Unlocalized name already set")
        g.NAME2BUBBLE[name] = self
        g.BUBBLE2NAME[self] = name

    def get_unlocalized_name(self):
        if self not in g.BUBBLE2NAME.keys():
            raise ValueError(f"Unlocalized name not set yet: '{self.__module__}.{self.__class__.__name__}'")
        return g.BUBBLE2NAME[self]

    def on_create(self):
        pass

    def pre_initialize(self):
        pass

    def initialize(self):
        pass

    def post_initialize(self):
        pass

    def on_update(self):
        pass


class BubbleObject(Sprite):
    # Define Sprite ID and Prefix
    sprite_id: str = "bubble"
    sprite_prefix: str = "qplay"

    def __init__(self, base_class: Bubble, x: int, y: int, radius: int, xupd):
        super(BubbleObject, self).__init__()

        self.health = base_class.health
        self.speedMultiplier = base_class.speedMultiplier
        self.attackMultiplier = base_class.attackMultiplier
        self.defenceMultiplier = base_class.defenceMultiplier

        self.collisionable = base_class.collisionable
        self.collisionWith = base_class.collisionWith

        self.type = base_class.type
        self.form = base_class.form

        if self.form == FORM_CIRCLE:
            self.geometry: Point = Point(x, y).buffer(radius)
        else:
            raise TypeError("Bubble must have the form 'circle' (FORM_CIRCLE)")

        self.radius = radius
        self.diameter = radius * 2

        self._image = reg
        self._id = get_canvas().create_image(x, y, seedint(get_stats("game")["seed"], xupd, 2, 15, 30))


Player = Player
