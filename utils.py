import os
import os
import sys
import tempfile
from time import time, sleep
from typing import Tuple, Callable

import pyglet
from PIL import Image, ImageDraw
from threadsafe_tkinter import Button, Frame, HIDDEN, Canvas, FLAT, Y, X, Tk

from advBuiltins import *
from bubble import place_bubble
from components import Store
from extras import get_coords
from special import ScrolledWindow
from teleport import teleport, tp_mode


def randint_lookup(value_in, min_, max_):
    # value_in2 = (value_in / 2) + 0.5
    sys.stderr.write(str(value_in) + " ")
    value_in2 = value_in
    return int(round(value_in2 * (max_ - min_) + min_))


def version2name(version: Tuple[str, int, int, int]):  # releasetype: str, a: int, b: int, c: int=0):
    rt: str = version[0]
    rt = rt.title()
    a_: int = version[1]
    b_: int = version[2]
    c_: int = version[3]
    return "%s %s.%s.%s" % (rt, a_, b_, c_)


def draw_ellipse(image, bounds, width=1.0, outline='white', antialias=4):
    """Improved ellipse drawing function, based on PIL.ImageDraw."""

    # Use a single channel image (mode='L') as mask.
    # The size of the mask can be increased relative to the imput image
    # to get smoother looking results.
    mask = Image.new(
        size=[int(dim * antialias) for dim in image.size],
        mode='L', color='black')
    draw = ImageDraw.Draw(mask)

    # draw outer shape in white (color) and inner shape in black (transparent)
    for offset, fill in (width / -1.5, '#ffffffff'), (width / 1.5, '#000000ff'):  # Note: Was first white, black
        left, top = [(value + offset) * antialias for value in bounds[:2]]
        right, bottom = [(value - offset) * antialias for value in bounds[2:]]
        draw.ellipse([left, top, right, bottom], fill=fill)

    # downsample the mask using PIL.Image.LANCZOS
    # (a high-quality downsampling filter).
    mask = mask.resize(image.size, Image.LANCZOS)
    # paste outline color to input image through the mask
    image.paste(outline, mask=mask)


def _new(mode, size, color):
    return Image.new(mode, size, color)


def _open(fp, mode: str = "r"):
    return Image.open(fp, mode)


def createbackground(size, color):
    return _new("RGBA", size, color)


def createcolorfield(size, color):
    return createbackground(size, color)


def createellipse(size, bg, fill=None, outline=None, width: int = 0):
    im = _new('RGBA', size, bg)
    draw = ImageDraw.Draw(im, 'RGBA')
    draw.ellipse((0, 0, *size), fill, outline, width)


def createbubble_image(size, inner=None, *colors):
    im = _new('RGBA', size, '#ffffff00')
    # im.putalpha(0)
    if inner is not None:
        inner_im: Optional[Image.Image] = _open(inner)
    else:
        inner_im: Optional[Image.Image] = None
    # draw = ImageDraw.Draw(im, "RGBA")
    i = 2

    # Drawung ellipses for Bubble.
    width = 0.75
    ex_w = width / 2
    w = width
    if len(colors) == 1:
        draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[0], width=w, antialias=4)
        i += width + ex_w
        # print("Single circle")
    else:
        for index in range(0, len(colors)):

            if len(colors) - 1 > index > 0:  # .OOO.
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w + ex_w,
                             antialias=4)
            elif index == len(colors) - 1:  # ....O
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w, antialias=4)
            else:  # First:  O....
                draw_ellipse(im, (0 + i, 0 + i, size[0] - i, size[0] - i), outline=colors[index], width=w + ex_w,
                             antialias=4)
            i += width + (ex_w * 2)

    i += 10

    if inner is not None:
        png2 = _new('RGBA', size, (0, 0, 0, 0))
        # noinspection PyUnboundLocalVariable
        if size[0] - int(i) < png2.width:
            inner_im = inner_im.resize((size[0] - int(i), size[1] - int(i)))
        png2.paste(inner_im, (int(i / 2), int(i / 2)))
        im = Image.alpha_composite(png2, im)

    return pillow2pyglet(im=im)


def pillow2pyglet(im: Image.Image):
    if not os.path.exists("assets/temp"):
        os.makedirs("assets/temp")

    # _imaging.

    temp_file = tempfile.TemporaryFile("w+", suffix=".png", dir=os.path.abspath("assets/temp"), delete=False)
    temp_file.close()

    pyglet.resource.reindex()
    im.save(temp_file.name)
    # temp_file.name

    # image: pyglet.image.ImageData = pyglet.image.ImageData(im.width, im.height, 'RGBA', raw_image, pitch=-im.width * 4)
    image = pyglet.resource.image(os.path.join("temp", os.path.split(temp_file.name)[-1]).replace("\\", "/"))
    # pyglet.image.TextureRegion()
    os.remove(temp_file.name)
    return image


def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return AdvFloat((point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2).sqrt()


# fast math algorithms
class FastRandom(object):
    def __init__(self, seed):
        self.seed = seed

    def randint(self):
        self.seed = (214013 * self.seed + 2531011)
        return (self.seed >> 16) & 0x7FFF


# rand.randint()


class Seed(object):
    def __init__(self, seed):
        self._seed = seed

    def randint(self, x, y):
        h: int = self._seed + x * 374761393 + y * 668265263
        h = (h ** (h >> 16)) * 1274126177
        return h ** (h >> 16)


def control(input_modes: dict, config: dict, root: Tk, canvas: Canvas, stats: dict, bubbles: dict, back: object, texts: dict,
            commands: dict, temp: dict, panels: dict, fore: dict, ship: dict, tp: dict, lang: dict, return_main: Callable,
            icons: dict, bub: dict, font: tuple, event, c_ammo: Callable, laucher_cfg: dict, log,
            save_system: object):
    """
    Ship-motion event
    :param save_system:
    :param log:
    :param laucher_cfg:
    :param c_ammo:
    :param font:
    :param bub:
    :param icons:
    :param ship:
    :param tp:
    :param lang:
    :param return_main:
    :param commands:
    :param fore:
    :param panels:
    :param temp:
    :param input_modes:
    :param config:
    :param root:
    :param canvas:
    :param stats:
    :param bubbles:
    :param back:
    :param texts:
    :param event:
    """

    if input_modes["store"] and commands["store"] is not None:
        if event.keysym == "Up":
            commands["store"].set_selected(canvas, -1)
        if event.keysym == "Down":
            commands["store"].set_selected(canvas, 1)
        if event.keysym == "Left":
            commands["store"].set_selected(canvas, int(-((config["height"] - 215) / 140 + 1)))
        if event.keysym == "Right":
            commands["store"].set_selected(canvas, int((config["height"] - 215) / 140 + 1))
        if event.keysym == "space":
            commands["store"].buy_selected(config, input_modes, log, root, canvas, stats, bubbles, back,
                                           texts,
                                           commands, temp, panels)
        if event.keysym == "BackSpace":
            commands["store"].exit(canvas, log, input_modes, stats, temp, commands)
            commands["store"] = None
        if event.keysym == "Escape":
            sleep(1)
            commands["store"].exit(canvas, log, input_modes, stats, temp, commands)
            commands["store"] = None
    if input_modes["present"]:
        if event.keysym == "space":
            if False != commands["present"] != True:
                commands["present"].exit(canvas)
                input_modes["pause"] = False
                input_modes["present"] = False
                stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
                stats["Effects"]["secure-time"] = temp["secure-save"] + time()
                stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
                stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
                stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
                stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
                stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
                stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()
    if input_modes["teleport"]:
        x, y = get_coords(canvas, tp["id1"])
        if event.keysym == 'Up':
            if y > 72 + 5:
                canvas.move(tp["id1"], 0, -5)
                canvas.move(tp["id2"], 0, -5)
                canvas.move(tp["id3"], 0, -5)
                canvas.move(tp["id4"], 0, -5)
        if event.keysym == "Down":
            if y < config["height"] - 105 - 5:
                canvas.move(tp["id1"], 0, 5)
                canvas.move(tp["id2"], 0, 5)
                canvas.move(tp["id3"], 0, 5)
                canvas.move(tp["id4"], 0, 5)
        if event.keysym == "Left":
            if x > 0 + 5:
                canvas.move(tp["id1"], -5, 0)
                canvas.move(tp["id2"], -5, 0)
                canvas.move(tp["id3"], -5, 0)
                canvas.move(tp["id4"], -5, 0)
        if event.keysym == "Right":
            if x < config["width"] - 5:
                canvas.move(tp["id1"], 5, 0)
                canvas.move(tp["id2"], 5, 0)
                canvas.move(tp["id3"], 5, 0)
                canvas.move(tp["id4"], 5, 0)
        if event.keysym == "BackSpace":
            input_modes["pause"] = False

            stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure-time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
            stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()
        if event.keysym == "Escape":
            input_modes["pause"] = False

            stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure-time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
            stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()
            sleep(1)
        if event.keysym == "Return":
            input_modes["pause"] = False

            stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure-time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
            stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, input_modes, ship, tp, tp["id1"])
        if event.keysym.lower() == "space":
            input_modes["pause"] = False

            stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
            stats["Effects"]["secure-time"] = temp["secure-save"] + time()
            stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
            stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
            stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
            stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
            stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
            stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()

            stats["teleports"] -= 1
            teleport(canvas, root, stats, input_modes, ship, tp, tp["id1"])
    elif event.keysym.lower() == "space":
        ammo_object = c_ammo()
        ammo_object.create(None, None)
    if event.keysym == "Escape" and (not input_modes["pause"]) and (not input_modes["store"]) and (not input_modes["teleport"]) and \
            (not input_modes["window"]) and (not input_modes["present"]) and (not input_modes["cheater"]):
        input_modes["pause"] = True

        canvas.delete(icons["pause"])
        if stats["Effects"]["special-level"]:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="#3f3f3f",
                                                       outline="#3f3f3f")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#afafaf")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#afafaf")

            temp['pause/menu_frame'] = Frame(root, bg="#3f3f3f")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=20, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief=FLAT, bg="#1f1f1f", fg="#afafaf", font=font)
            back = "#1f1f1f"
            fore = "yellow"
        else:
            temp['pause/bg'] = canvas.create_rectangle(0, 69,
                                                       config["width"],
                                                       config[
                                                           "height"],
                                                       fill="darkcyan",
                                                       outline="darkcyan")
            temp['pause/toline'] = canvas.create_line(0, 69, config["width"], 69,
                                                      fill="#7fffff")
            # temp['pause/bottom.line'] = canvas.create_line(0, config["height"] - 102, config["width"],
            #                                                config["height"] - 102,
            #                                                fill="#7fffff")

            temp['pause/menu_frame'] = Frame(root, bg="darkcyan")
            temp['pause/menu'] = canvas.create_window(config["middle-x"], config["middle-y"] / 2 + 130,
                                                      window=temp['pause/menu_frame'], anchor='n',
                                                      height=500, width=300)

            temp["pause/back-to-menu"] = Button(temp["pause/menu_frame"], text=lang["pause.back-to-home"],
                                                command=lambda: return_main(),
                                                relief=FLAT, bg="#005f5f", fg="#7fffff", font=[font])

            back = "#005f5f"
            fore = "#7fffff"

        temp["s_frame"] = Frame(root, bg=back)
        temp["s_frame"].place(x=config["middle-x"], y=config["middle-y"] / 2 + 250, anchor='n', width=1000)

        temp["sw"] = ScrolledWindow(temp["s_frame"], 1020, 321, height=321, width=1000)

        temp["canv"] = temp["sw"].canv
        temp["canv"].config(bg=back)
        temp["sw"].scrollwindow.config(bg=back)

        temp["frame"] = temp["sw"].scrollwindow

        class_names = ("Normal", "Double", "Kill", "Triple", "SpeedUp", "SpeedDown", "Up", "Ultimate", "DoubleState",
                       "Protect", "SlowMotion", "TimeBreak", "Confusion", "HyperMode", "Teleporter",
                       "Coin", "NoTouch", "Paralis", "Diamond", "StoneBub", "Present", "SpecialKey", "LevelKey")

        id_names = (
            "bubble.normal", "bubble.double", "bubble.kill", "bubble.triple", "bubble.speedup", "bubble.speeddown",
            "bubble.up", "bubble.state.ultimate", "bubble.state.double", "bubble.state.protect",
            "bubble.state.slowmotion",
            "bubble.state.timebreak", "bubble.state.confusion", "bubble.state.hypermode", "bubble.teleporter",
            "bubble.coin", "bubble.state.notouch", "bubble.state.paralis", "bubble.diamond", "bubble.stonebubble",
            "bubble.present", "bubble.state.specialkey", "bubble.levelkey"
        )

        canvass = Canvas(temp["frame"], bg=back, highlightthickness=0)
        x = 50
        y = 50
        temp["pause/bubble.iconss"] = []
        for i in range(len(class_names)):
            # print(class_names[i], b[i])
            place_bubble(canvass, bub, x, y, 25, class_names[i])
            canvass.create_text(x, y + 40, text=lang[id_names[i]], fill=fore, font=[font, 10])
            if x > 900:
                x = 50
                y += 100
            else:
                x += 100

        canvass.config(height=y + 70, width=1000)
        canvass.pack(fill=Y)

        temp["pause/back-to-menu"].pack(fill=X)

        icons["pause"] = canvas.create_image(config["middle-x"], config["middle-y"] / 2,
                                             image=icons["pause-id"])

        canvas.itemconfig(texts["pause"], text="")
        root.update()

        temp["scorestate-save"] = stats["Effects"]["scorestate-time"] - time()
        temp["secure-save"] = stats["Effects"]["secure-time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak-time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion-time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion-time"] - time()
        temp["paralis-save"] = stats["Effects"]["paralyse-time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed-time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch-time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level-time"] - time()
    elif event.keysym == "Escape" and input_modes["pause"] and (not input_modes["store"]) and (not input_modes["teleport"]) and \
            (not input_modes["window"]) and (not input_modes["present"]) and (not input_modes["cheater"]):
        input_modes["pause"] = False

        canvas.itemconfig(icons["pause"], state=HIDDEN)
        canvas.itemconfig(texts["pause"], text="")

        temp["pause/back-to-menu"].destroy()
        temp['pause/menu_frame'].destroy()
        temp["s_frame"].destroy()

        canvas.delete(temp['pause/toline'])
        # canvas.delete(temp['pause/bottom.line'])
        canvas.delete(temp['pause/menu'])
        canvas.delete(temp['pause/bg'])

        root.update()

        stats["Effects"]["scorestate-time"] = temp["scorestate-save"] + time()
        stats["Effects"]["secure-time"] = temp["secure-save"] + time()
        stats["Effects"]["timebreak-time"] = temp["timebreak-save"] + time()
        stats["Effects"]["confusion-time"] = temp["confusion-save"] + time()
        stats["Effects"]["slowmotion-time"] = temp["slowmotion-save"] + time()
        stats["Effects"]["paralyse-time"] = temp["paralis-save"] + time()
        stats["Effects"]["shotspeed-time"] = temp["shotspeed-save"] + time()
        stats["Effects"]["notouch-time"] = temp["notouch-save"] + time()
    if event.keysym == "t" and stats["teleports"] > 0 and (not input_modes["teleport"]):
        input_modes["pause"] = True

        temp["scorestate-save"] = stats["Effects"]["scorestate-time"] - time()
        temp["secure-save"] = stats["Effects"]["secure-time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak-time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion-time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion-time"] - time()
        temp["paralis-save"] = stats["Effects"]["paralyse-time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed-time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch-time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level-time"] - time()

        input_modes["teleport"] = True

        tp_mode(canvas, config, stats, input_modes, tp)
    if event.keysym.lower() == "e" and (not input_modes["store"]):
        input_modes["pause"] = True
        temp["scorestate-save"] = stats["Effects"]["scorestate-time"] - time()
        temp["secure-save"] = stats["Effects"]["secure-time"] - time()
        temp["timebreak-save"] = stats["Effects"]["timebreak-time"] - time()
        temp["confusion-save"] = stats["Effects"]["confusion-time"] - time()
        temp["slowmotion-save"] = stats["Effects"]["slowmotion-time"] - time()
        temp["paralis-save"] = stats["Effects"]["paralyse-time"] - time()
        temp["shotspeed-save"] = stats["Effects"]["shotspeed-time"] - time()
        temp["notouch-save"] = stats["Effects"]["notouch-time"] - time()
        temp["special-level-save"] = stats["Effects"]["special-level-time"] - time()
        input_modes["store"] = True
        log.debug("bub_move", "Creating Store() to input mode \"store\"")
        log.debug("bub_move", "storemode=" + str(input_modes["store"]))
        commands["store"] = Store(canvas, log, config, input_modes, stats, icons, fore, font, laucher_cfg)
    # if event.char == "/":
    #     CheatEngine().event_handler(canvas, input_modes, stats, config, temp, log, backgrounds, bubble, event, bub)
    # if input_modes["cheater"]:
    #     CheatEngine().input_event_handler(canvas, log, stats, backgrounds, bubble, event, config, bub, temp,
    #                                       input_modes)

    if event.keysym == "Escape":
        save_system.save()
    root.update()
