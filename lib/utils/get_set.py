# noinspection PyProtectedMember
from tkinter import _default_root as tkd
from typing import Union, NoReturn

import threadsafe_tkinter as tk
from threadsafe_tkinter import *

tk._default_root = tkd


# noinspection PyUnresolvedReferences,PyProtectedMember
def get_root() -> Tk:
    return tk._default_root


# noinspection PyUnresolvedReferences,PyProtectedMember
def get_game():
    if hasattr(tk._default_root, "game"):
        return tk._default_root.game
    else:
        return None


# noinspection PyUnresolvedReferences,PyProtectedMember
def get_canvas() -> Union[Canvas, None]:
    if hasattr(tk._default_root, "canvas"):
        return tk._default_root.canvas
    else:
        return None


# noinspection PyUnresolvedReferences,PyProtectedMember
def set_canvas(obj: object) -> Canvas:
    tk._default_root.canvas = obj
    return get_canvas()


# noinspection PyUnresolvedReferences,PyProtectedMember
def del_canvas() -> NoReturn:
    del tk._default_root.canvas
