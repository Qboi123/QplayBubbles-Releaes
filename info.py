from time import sleep, time
from tkinter import TclError, Canvas
from typing import *


def show_score(canvas: Canvas, texts: Dict[str, int], score: Union[int, str]):
    """
    Shows Score
    :param texts:
    :param canvas:
    :param score:
    :return:
    """
    canvas.itemconfig(texts["score"], text=str(score))


def show_level(canvas: Canvas, texts: Dict[str, int], level: Union[int, str]):
    """
    Shows Level
    :param canvas:
    :param texts:
    :param level:
    :return:
    """
    canvas.itemconfig(texts["level"], text=str(level))


def show_speed(canvas: Canvas, texts: Dict[str, int], speed: int):
    """
    Shows Speed
    :param texts:
    :param canvas:
    :param speed:
    :return:
    """
    canvas.itemconfig(texts["speed"], text=str(speed))


def show_lives(canvas: Canvas, texts: Dict[str, int], lives: int):
    """
    Shows Lives
    :param canvas:
    :param texts:
    :param lives:
    :return:
    """
    canvas.itemconfig(texts["lives"], text=str(lives))


def show_score_point(canvas: Canvas, texts: Dict[str, int], data):
    """
    Shows score status value
    :param texts:
    :param canvas:
    :param data:
    :return:
    """
    canvas.itemconfig(texts["scorestate"], text=data)


def show_protection(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows security-state
    :param canvas:
    :param texts:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["secure"], text=on_off)


def show_slowmotion(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows slow motion state
    :param texts:
    :param canvas:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["slowmotion"], text=on_off)


def show_confusion(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows confusion state
    :param canvas:
    :param texts:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["confusion"], text=on_off)


def show_timebreak(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows timebreak state
    :param texts:
    :param canvas:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["timebreak"], text=on_off)


def show_spdboost(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows speedboost state
    :param texts:
    :param canvas:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["speedboost"], text=on_off)


def show_paralis(canvas: Canvas, texts: Dict[str, int], on_off: str):
    """
    shows paralis state
    :param texts:
    :param canvas:
    :param on_off:
    :return:
    """
    canvas.itemconfig(texts["paralis"], text=on_off)


def show_shotspeed(canvas: Canvas, texts: Dict[str, int], integer: Union[str, int]):
    """
    Shows Shot-speed state
    :param canvas:
    :param texts:
    :param integer:
    :return:
    """
    canvas.itemconfig(texts["shotspeed"], text=integer)


def show_tps(canvas: Canvas, texts: Dict[str, int], integer: Union[str, int]):
    """
    Shows Teleports
    :param canvas:
    :param texts:
    :param integer:
    :return:
    """
    canvas.itemconfig(texts["shiptp"], text=str(integer))


def show_notouch(canvas: Canvas, texts: Dict[str, int], integer: Union[str, int]):
    """
    Shows Teleports
    :param canvas:
    :param texts:
    :param integer:
    :return:
    """
    canvas.itemconfig(texts["notouch"], text=str(integer))


def show_diamond(canvas: Canvas, texts: Dict[str, int], integer: Union[str, int]):
    """
    Shows Diamonds
    :param canvas:
    :param texts:
    :param integer:
    :return:
    """
    canvas.itemconfig(texts["diamond"], text=str(integer))


def show_coin(canvas: Canvas, texts: Dict[str, int], integer: Union[str, int]):
    """
    Shows Coins
    :param texts:
    :param canvas:
    :rtype: object

    :param integer:
    """
    canvas.itemconfig(texts["coin"], text=str(integer))


def view_level(canvas: Canvas, root, texts: Dict[str, int], level: Union[str, int]):
    """
    Viewes level
    """
    canvas.itemconfig(texts["level-view"], text="Level " + str(level))
    root.update()
    sleep(2)
    canvas.itemconfig(texts["level-view"], text="")
    root.update()


def show_info(canvas: Canvas, texts: Dict[str, int], stats):
    """
    Shows all information:
    Score, Level, status-time etc.
    :return:
    """
    try:
        show_score(canvas, texts, stats["score"])
        show_level(canvas, texts, stats["level"])
        show_speed(canvas, texts, stats["shipspeed"])
        show_lives(canvas, texts, stats["lives"])
        show_score_point(canvas, texts, str(int(stats["scorestate-time"] - time())))
        show_protection(canvas, texts, str(int(stats["secure-time"] - time())))
        show_slowmotion(canvas, texts, str(int(stats["slowmotion-time"] - time())))
        show_confusion(canvas, texts, str(int(stats["confusion-time"] - time())))
        show_timebreak(canvas, texts, str(int(stats["timebreak-time"] - time())))
        show_spdboost(canvas, texts, str(int(stats["speedboost-time"] - time())))
        show_paralis(canvas, texts, str(int(stats["paralis-time"] - time())))
        show_shotspeed(canvas, texts, str(int(stats["shotspeed-time"] - time())))
        show_notouch(canvas, texts, str(int(stats["notouch-time"] - time())))
        show_tps(canvas, texts, stats["teleports"])
        show_diamond(canvas, texts, stats["diamonds"])
        show_coin(canvas, texts, stats["coins"])
    except AttributeError:
        exit(0)
    except TclError:
        exit(0)
