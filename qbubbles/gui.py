from tkinter import Canvas, PhotoImage
from typing import Optional, Tuple, Union, Callable
from zipimport import zipimporter

from PIL import ImageTk, Image
from overload import overload
from qbubbles.registry import Registry

from qbubbles.resources import Resources

from qbubbles.events import ResizeEvent


class CRectangle(object):
    def __init__(self, canvas: Canvas, x1, y1, x2, y2, *, fill="", outline="", anchor="center", tags=tuple()):
        self._id = canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=outline)  # , anchor=anchor)
        self._canvas = canvas
        # print("CRectangle created")

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


class CImage(object):
    def __init__(self, canvas: Canvas, x, y, *, image, anchor="center", tags=tuple()):
        self._id = canvas.create_image(x, y, image=image, anchor=anchor, tags=tags)  # , anchor=anchor)
        self._canvas: Canvas = canvas
        self._image: Union[ImageTk.PhotoImage, PhotoImage] = image
        self._anchor = anchor
        self._tags = tags

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> Optional[Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, *, image=None, anchor=None, tags=None):
        if image is None:
            image=self._image
        if anchor is None:
            anchor=self._anchor
        if tags is None:
            tags=self._tags
        return self._canvas.itemconfigure(self._id, image=image, anchor=anchor, tags=tags)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CText(object):
    def __init__(self, canvas: Canvas, x, y, *, text, anchor="center", fill="", tags=tuple(), font=("Helvetica", 10)):
        self._id = canvas.create_text(x, y, text=text, anchor=anchor, tags=tags, fill=fill, font=font)
        self._canvas: Canvas = canvas
        self._text: str = text
        self._anchor = anchor
        self._tags = tags
        self._fill = fill
        self._font = font

    def get_id(self):
        return self._id

    def move(self, x=None, y=None):
        return self._canvas.move(self._id, x, y)

    @overload
    def coords(self, x1, y1) -> None:
        self._canvas.coords(self._id, x1, y1)

    @coords.add
    def coords(self) -> Optional[Tuple[float, float]]:
        return self._canvas.coords(self._id)

    def bind(self, sequence=None, func=None, add=None) -> Union[str, int]:
        return self._canvas.tag_bind(self._id, sequence, func, add)

    def unbind(self, sequence, funcid=None):
        return self._canvas.tag_unbind(self._id, sequence, funcid)

    def configure(self, *, text=None, anchor=None, tags=None, fill=None, font=None):
        if text is None:
            text = self._text
        if anchor is None:
            anchor = self._anchor
        if tags is None:
            tags = self._tags
        if fill is None:
            fill = self._fill
        if font is None:
            font = self._font
        return self._canvas.itemconfigure(self._id, text=text, anchor=anchor, tags=tags, fill=fill, font=font)

    def cget(self, option) -> Union[str, int, float, bool, list, dict, Callable]:
        return self._canvas.itemcget(self._id, option)

    def lower(self, *args):
        return self._canvas.tag_lower(self._id, *args)

    def raise_(self, *args):
        return self._canvas.tag_raise(self._id, *args)

    config = configure


class CPanel(CRectangle):
    def __init__(self, canvas: Canvas, x, y, width, height, fill="", outline=""):
        self._width = width
        self._height = height
        if width == "extend":
            width = canvas.winfo_width()
        if height == "expand":
            height = canvas.winfo_height()
        self.x = x
        self.y = y
        super(CPanel, self).__init__(canvas, x, y, width, height, fill=fill, outline=outline, anchor="nw")

    def on_resize(self, event: ResizeEvent):
        # noinspection PyDeepBugsBinOperand
        if self._width == "extend":
            width = self._canvas.winfo_width() - self.x
        if self._height == "expand":
            height = self._canvas.winfo_height() - self.y
        self.coords(self.x, self.y, self._width, self._height)


class CEffectBarArea(object):
    def __init__(self, canvas, *, gamemap):
        self.effectbars = CEffectBar

    def add_effect(self, applied_effect):
        pass


class CEffectBar(object):
    def __init__(self, canvas, x, y, *, gamemap, effect):
        barimage = Registry.get_texture("qbubbles:gui", "qbubbles:effect_bar", gamemap=gamemap)
        effectimage = Registry.get_texture("qbubbles:effect", effect.get_uname(), gamemap=gamemap)

        self.cBarimage = CImage(canvas, x, y, image=barimage, anchor="nw")
        self.cEffectimage = CImage(canvas, x+2, y+2, image=effectimage, anchor="nw")
        self._effect = effect

    def get_effect(self):
        return self._effect
