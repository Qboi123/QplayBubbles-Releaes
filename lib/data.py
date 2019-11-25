from typing import NoReturn

from lib.sprites import Bubble

BUBBLES_CLASS = []
BUBBLES_ID = []


def GetBubbleClassByID(_id: int) -> Bubble:
    index = BUBBLES_ID.index(_id)
    return BUBBLES_CLASS[index]


def GetBubbleIDByClass(_class: Bubble) -> int:
    index = BUBBLES_CLASS.index(_class)
    return BUBBLES_ID[index]


def GetBubbleIDByIndex(index: int) -> int:
    return BUBBLES_ID[index]


def GetBubbleClassByIndex(index: int) -> Bubble:
    return BUBBLES_CLASS[index]


def GetBubbleIndexByID(_id: int) -> int:
    index = BUBBLES_ID.index(_id)
    return index


def GetBubbleIndexByClass(_class: Bubble) -> int:
    index = BUBBLES_CLASS.index(_class)
    return index


def AddBubble(_id: int, _class: Bubble) -> NoReturn:
    BUBBLES_CLASS.append(_class)
    BUBBLES_ID.append(_id)


def DestroyBubbleByID(_id: int):
    from .utils.get_set import get_canvas

    # index = GetBubbleIndexByID(_id)
    canvas = get_canvas()
    canvas.delete(_id)


def DestroyBubbleByClass(_class: Bubble):
    _id = GetBubbleIDByClass(_class)
    DestroyBubbleByID(_id)
