import threadsafe_tkinter as tk
from tkinter import _default_root as tkd
from threadsafe_tkinter import *
from typing import *
tk._default_root = tkd


def get_root() -> Tk:
    return tk._default_root


def get_canvas() -> Union[Canvas, None]:
    if hasattr(tk._default_root, "canvas"):
        return tk._default_root.canvas
    else:
        return None


def set_canvas(obj: Canvas):
    tk._default_root.canvas = obj
    return get_canvas()


def del_canvas():
    del tk._default_root.canvas
