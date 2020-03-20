from random import randint

from advUtils.advBuiltins import AdvBoolean

from bubble import Bubble
from registry import Registry


class BubbleSpec(object):
    def __init__(self, bubble, speed, radius):
        self.speed = speed
        self.radius = radius
        self.bubble = bubble


class NormalBubble(Bubble):
    def __init__(self, **kw):
        Bubble.__init__(self, **kw)
        self.priority = 5_000_000

        self.speedNoise = 5
        self.speedBase = 10

        self.radiusNoise = 30
        self.radiusBase = 40

        self.xSpeed = randint(int(kw["stats"]["bubspeed"]) - 3, int(kw["stats"]["bubspeed"]))
        self.radius = randint(int(kw["config"]["bubble"]["minRadius"]), int(kw["config"]["bubble"]["maxRadius"]))

    def on_create(self, rand) -> BubbleSpec:
        x_speed = rand.randint(self.speedBase - self.speedNoise, self.speedBase + self.speedNoise)
        x_radius = rand.randint(int(kw["config"]["bubble"]["minRadius"]), int(kw["config"]["bubble"]["maxRadius"]))
        return BubbleSpec(self, x_speed, x_radius)

    def on_update(self, bubbleobject, **kw) -> AdvBoolean:
        bubbleobject.on_move()

        return AdvBoolean(True)
