from .base import Bubble, StatusBubble
from .fake_main import Game


class NormalBubble(Bubble):
    def __init__(self, parent: Game):
        super().__init__(parent)
        self.name = "Normal"
        self.radius = int()

    def on_collision(self, parent: Game):
        parent.stats["score"] += self.r


class InfitraBubble(StatusBubble)
