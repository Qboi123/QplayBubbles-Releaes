from typing import List, Dict, Union, NoReturn

from lib.utils import get_rgblist_from_hex, to_rgb
from lib.utils.get_set import get_canvas

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


class Size(object):
    def __init__(self, height: int, width: int):
        self.height: int = height
        self.width: int = width

    def __add__(self, other):
        if type(other) == type(self):
            return self.__init__(self.height + other.height, self.width + other.width)
        elif type(other) == List:
            return self.__init__(self.height + other[0], self.width + other[1])
        elif type(other) == Dict:
            return self.__init__(self.height + other["height"], self.width + other["width"])
        else:
            raise TypeError("Can't add %s to %s" % (type(other), type(self)))

    def __sub__(self, other):
        if type(other) == type(self):
            return self.__init__(self.height - other.height, self.width - other.width)
        elif type(other) == List:
            return self.__init__(self.height - other[0], self.width - other[1])
        elif type(other) == Dict:
            return self.__init__(self.height - other["height"], self.width - other["width"])
        else:
            raise TypeError("Can't add %s to %s" % (type(other), type(self)))

    def __eq__(self, other):
        if type(other) == type(self):
            return (self.height == other.height) and (self.width == other.width)
        elif type(other) == List:
            return self.__init__(self.height + other[0], self.width + other[1])
        elif type(other) == Dict:
            return self.__init__(self.height + other["height"], self.width + other["width"])

    def __int__(self):
        return self.height * self.width

    def __setitem__(self, key: str, value: int):
        if key == "height":
            self.height = value
        elif key == "width":
            self.width = value
        else:
            raise KeyError("Key \"%s\" isn't compatible with %s" % (key, type(self)))

    def __getitem__(self, item: str):
        if item == "height":
            return self.height
        elif item == "width":
            return self.width
        else:
            raise KeyError("Key \"%s\" isn't compatible with %s" % (item, type(self)))

    def __delitem__(self, key):
        raise PermissionError("Key \"%s\" is read-write only (not deletable)" % key)

    def __delattr__(self, item):
        raise PermissionError("Attribute \"%s\" is read-write only (not deletable)" % item)


class Point2D(object):
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def __str__(self):
        return "Point2D(x=%s, y=%s)" % (self.x, self.y)

    def __add__(self, other):
        if type(other) == type(self):
            return Point2D(self.x + other.x, self.y + other.y)
        elif type(other) == List:
            return Point2D(self.x + other[0], self.y + other[1])
        elif type(other) == Dict:
            return Point2D(self.x + other["x"], self.y + other["y"])
        else:
            raise TypeError("Can't add %s to %s" % (type(other), type(self)))

    def __sub__(self, other):
        if type(other) == type(self):
            return Point2D(self.x - other.height, self.y - other.width)
        elif type(other) == List:
            return Point2D(self.x - other[0], self.y - other[1])
        elif type(other) == Dict:
            return Point2D(self.x - other["x"], self.y - other["y"])
        else:
            raise TypeError("Can't add %s to %s" % (type(other), type(self)))

    def __eq__(self, other):
        if type(other) == type(self):
            return (self.x == other.x) and (self.y == other.y)
        elif type(other) == List:
            return (self.x == other[0]) and (self.y == other[1])
        elif type(other) == Dict:
            return (self.x == other["x"]) and (self.y == other["y"])

    def __int__(self):
        return self.x * self.y

    def __setitem__(self, key: str, value: int):
        if key == "x":
            self.x = value
        elif key == "y":
            self.y = value
        else:
            raise KeyError("Key \"%s\" isn't compatible with %s" % (key, type(self)))

    def __getitem__(self, item: str):
        if item == "x":
            return self.x
        elif item == "y":
            return self.y
        else:
            raise KeyError("Key \"%s\" isn't compatible with %s" % (item, type(self)))

    def __delitem__(self, key):
        raise PermissionError("Key \"%s\" is read-write only (not deletable)" % key)

    def __delattr__(self, item):
        raise PermissionError("Attribute \"%s\" is read-write only (not deletable)" % item)


class ColorRGB(object):
    def __init__(self, color=Union[List[int], str, int]):
        if type(color) == List[int]:
            self.r = color[0]
            self.g = color[1]
            self.b = color[2]
        elif type(color) == str:
            _rgb = to_rgb(color)

            self.r = _rgb[0]
            self.g = _rgb[1]
            self.b = _rgb[2]
        elif type(color) == int:
            _hex = hex(color)
            _rgb = get_rgblist_from_hex()


class Accent(object):
    def __init__(self, color):
        self.__color = color
        self._color = property(self.getColor())

    def getColor(self):
        return self.__color




class Sprite(object):
    # Define Sprite ID and Prefix
    sprite_id: str = "bubble"
    sprite_prefix: str = "qplay"

    def __init__(self)-> None:
        """
        Target Damage = attackMP / targetDefenceMP

        Sprite.sprite_id is a string used so the game recognized a Bubble or something else
        Sprite.sprite_prefix is used so the game knows from what Mod it used from

        Sptite.health is a float about HP
        Sprite.attackMultiplier is an integer used for target damage
        Sprite.defenceMultiplier is an integer used for decreasing Sprite's damage
        Sprite.speedMultiplier is an integer used for pixels per tick
        Sprite.collisionable is a boolean that is used to en- / disable collision
        Sprite.collisionWith is a list with Sprite IDs inside
        Sprite.moveAxis is a axis string used for direction
        Sprite.returnBorder is a boolean. If True, when the sprite touches the border it's direction will invert
        :type parent: type[Sprite]
        """
        # if issubclass(parent, Sprite):
        #     self._parent = parent
        # else:
        #     raise TypeError("Parent is not a subclass of Sprite.")

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
