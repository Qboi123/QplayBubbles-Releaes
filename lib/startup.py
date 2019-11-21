from tkinter import Canvas
from typing import Dict, Any

from lib.utils.config import Reader


def start(bubble: Dict[str, Any], save_name: str, stats: Dict[str, Any], config: Dict[str, Any], bub,
          modes: Dict[str, bool], canvas: Canvas):
    bubs = Reader("slots/" + save_name + "/bubble.data").get_decoded()
    if len(bubs["bub-id"]) <= 1:
        r_start(bubble, stats, config, bub, canvas, modes)
        return
    print(bubs)
    for i in range(len(bubs["bub-id"])):
        bubble["active2"].append(False)
        # print(i)
    for i in range(len(bubs["bub-id"]) - 1):
        if bubs["bub-special"]:
            pass
            # set_bubble(stats, config, bub, canvas, bubble, bubs["bub-index"][i],
            #            bubs["bub-position"][i][0],
            #            bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
        elif not bubs["bub-special"]:
            pass
            # SpecialMode.create_bubble(canvas, config, bubble, stats, bub, bubs["bub-index"][i],
            #                           bubs["bub-position"][i][0],
            #                           bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])


def r_start(bubble: Dict[str, Any], stats: Dict[str, Any], config: Dict[str, Any], bub, canvas: Canvas,
            modes: Dict[str, bool]):
    for i in range(int((config["width"] - 72) / 10)):
        bubble["active2"].append(False)
        # print(i)

    # print(int((config["width"] - 72) / 10))
    for i in range(int((config["width"] - 73) / 10)):
        pass
        # print(i)
        # spd = stats["bubspeed"]
        # i = randint(0, 1600)
    for stats["xupd"] in range(-10, config["width"] + 100):
        pass
        # create_bubble(stats, config, bub, canvas, bubble, stats["xupd"])
