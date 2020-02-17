from base import Bubble, StatusBubble


class NormalBubble(Bubble):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Normal"
        self.radius = int()

    def on_collision(self, parent):
        parent.stats["score"] += self.r


class InfitraBubble(StatusBubble)
