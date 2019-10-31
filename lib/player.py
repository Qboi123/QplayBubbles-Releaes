from .base import Sprite
from .sprites import Bubble
from .status import *
from typing import *


class Player(Sprite):
    def __init__(self, stats):
        Sprite.__init__(self)

        self.collisionable = False
        self.collisionWith = []

        self.score = stats["score"]
        self.status: List[Type[Status]] = []

    def on_join(self):
        pass
