from PIL.ImageTk import PhotoImage

from .base import *


class Bubble(Sprite):
    # Define Sprite ID and Prefix
    sprite_id: str = "bubble"
    sprite_prefix: str = "qplay"

    # Define Bubble ID and Prefix
    bubble_id: str = "base"
    bubble_prefix: str = "qplay"

    def __init__(self, parent):
        
        Sprite.__init__(self, Bubble)

        if issubclass(parent, Sprite):
            self._bubbleParent = parent
        else:
            raise TypeError("{name} is not a subclass of Bubble.".format(name=parent.__name__))

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

    def on_create(self):
        Sprite.create(self)

    def pre_initialize(self):
        pass

    def initialize(self):
        pass
        # from . import bubbles
        # _bubbles = dir(bubbles)

    def post_initialize(self):
        pass
