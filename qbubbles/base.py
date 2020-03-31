from tkinter import Canvas
from typing import Optional, Union, Callable, List, Tuple

from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent, MouseEnterEvent, \
    MouseLeaveEvent, ResizeEvent
from qbubbles.registry import Registry
from qbubbles.sprite.abilities import Ability

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


ActionIsNoneWarning = Warning


class CRectangle(object):
    def __init__(self, canvas: Canvas, x1, y1, x2, y2, fill="", outline="", anchor="center", tags=tuple()):
        self._id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)  # , anchor=anchor)
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
