from typing import *

AXIS_HORIZONTAL = "axis horizontal"
AXIS_VERTICAL = "axis vertical"
AXIS_DIAGONAL_NW = "axis diagonal nw se"
AXIS_DIAGONAL_NE = "axis diagonal ne sw"
AXIS_DIAGONAL_SE = "axis diagonal nw se"
AXIS_DIAGONAL_SW = "axis diagonal ne sw"
FORM_CIRCLE = "form circle"
FORM_SQUARE = "form square"
FORM_NONE = "form none"
NONE = None
TYPE_IMAGE = "type image"
TYPE_CIRCLE = "type circle"
TYPE_OVAL = "type oval"
TYPE_RECTANGLE = "type rectangle"
TYPE_LINE = "type line"
TYPE_TEXT = "type text"
TYPE_INV = "type invisible"
TYPE_INVISIBLE = TYPE_INV


class Sprite(object):
    # Define Sprite ID and Prefix
    sprite_id: str = "bubble"
    sprite_prefix: str = "qplay"

    def __init__(self, parent) -> None:
        """
        Target Damage = attackMP / targetDefenceMP

        Sprite.sprite_id is a string used so the game recognized a Bubble or something else
        Sprite.sprite_prefix is used so the game knows from what Mod it used from

        Sptite.health is a float about HP
        Sprite.attackMultiplier is an integer used for Target Damage
        Sprite.defenceMultiplier is an integer used for decreasing Sprite's damage
        Sprite.speedMultiplier is an integer used for Pixels per Tick
        Sprite.collisionable is a boolean that is used to en- / disable collision
        Sprite.collisionWith is a list with Sprite IDs inside
        Sprite.moveAxis is a Axis string using for direction
        Sprite.returnBorder is a boolean. If True, when the sprite touches the border it's direction will invert
        :type parent: type[Sprite]
        """
        if issubclass(parent, Sprite):
            self._parent = parent
        else:
            raise TypeError("Parent is not a subclass of Sprite.")

        # Define HP
        self.health: float = 0.001

        # Define Multipliers
        self.attackMultiplier: int = 0
        self.defenceMultiplier: int = 0
        self.speedMultiplier: int = 0

        # Define Collisions
        self.collisionable: bool = False
        self.collisionWith: list = []

        # Define Movement
        self.moveAxis: Union[AXIS_HORIZONTAL, AXIS_VERTICAL, AXIS_DIAGONAL_NE, AXIS_DIAGONAL_NW] = AXIS_HORIZONTAL
        self.returnBorder: bool = True

        # Define Look
        self.type = TYPE_IMAGE
        self.form = FORM_NONE
        self.create()

    def create(self, *args: List[int], **kwargs) -> NoReturn:
        """
        create(self, x1, y1, x2, y2, fill="", outline="", anchor="nw"):
        create(self, x, y, image=None, anchor="nw"):
        :param args:
        :param kwargs:
        :return:
        """
        from .utils import get_set
        if self.type == TYPE_IMAGE:
            get_set.get_canvas().create_image(*args, **kwargs)
        elif self.type == TYPE_RECTANGLE:
            get_set.get_canvas().create_rectangle(*args, **kwargs)
        elif self.type == TYPE_CIRCLE:
            if args[0] == args[1]:
                get_set.get_canvas().create_oval(*args, **kwargs)
            else:
                raise ValueError("Arg 1 and arg 2 aren't the same")
        elif self.type == TYPE_OVAL:
            get_set.get_canvas().create_oval(*args, **kwargs)
        else:
            raise TypeError("Unkown Type: %s" % self.type)

    def update(self) -> NoReturn:
        """
        Updating Sprite information
        :return:
        """
        pass

    def on_join(self) -> NoReturn:
        """
        On join event
        :return:
        """
        pass
