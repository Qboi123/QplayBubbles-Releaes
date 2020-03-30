from random import randint, Random
from tkinter import Canvas
from typing import Dict, Any, List

from bubble import create_bubble
from bubbles import Bubble
from components import SpecialMode
from config import Reader


class BubbleSystem(object):
    def __init__(self, bubbles: List[Bubble]):
        self.bubblePriorities = []
        self.maxPriority = 0

        for bubble in bubbles:
            self.bubblePriorities.append((bubble, self.maxPriority))
            self.maxPriority += bubble.priority

    def random(self, rand: Random):
        integer = rand.randint(0, self.maxPriority)
        for priority in self.bubblePriorities:
            pass


def start(bubble: Dict[str, Any], save_name: str, stats: Dict[str, Any], config: Dict[str, Any], bub,
          modes: Dict[str, bool], canvas: Canvas):
    bubs = Reader("saves/" + save_name + "/bubble.nzt").get_decoded()
    if len(bubs["bub-id"]) <= 1:
        r_start(bubble, stats, config, bub, canvas)
        return
    print(bubs)
    for i in range(len(bubs["bub-id"])):
        bubble["active2"].append(False)
        # print(i)
    for i in range(len(bubs["bub-id"]) - 1):
        if bubs["bub-special"]:
            create_bubble(stats, config, bub, canvas, bubble, bubs["bub-index"][i],
                          bubs["bub-position"][i][0],
                          bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])
        elif not bubs["bub-special"]:
            SpecialMode.create_bubble(canvas, config, bubble, stats, bub, bubs["bub-index"][i],
                                      bubs["bub-position"][i][0],
                                      bubs["bub-position"][i][1], bubs["bub-radius"][i], bubs["bub-speed"][i])


def r_start(bubble: Dict[str, Any], stats: Dict[str, Any], config: Dict[str, Any], bub, canvas: Canvas):
    for i in range(int((config["width"] - 72) / 10)):
        bubble["active2"].append(False)
        # print(i)

    # print(int((config["width"] - 72) / 10))
    for i in range(int((config["width"] - 73) / 10)):
        # print(i)
        r = randint(int(config["Bubble"]["min-radius"]),
                    int(config["Bubble"]["max-radius"]))
        x = randint(-r, config["width"] + r)
        y = randint(72 + r, (config["height"] - r))
        # spd = stats["bubspeed"]
        # i = randint(0, 1600)
        create_bubble(stats, config, bub, canvas, bubble, x=x, y=y, r=r)
