from random import randint
from versions.v1_5_0_pre5.lib.bubble import Bubble


class NormalBubble(Bubble):
    def __init__(self, **kw):
        Bubble.__init__(self, **kw)
        self.chance = 7/1600
        self.xSpeed = randint(int(kw["stats"]["bubspeed"]) - 3, int(kw["stats"]["bubspeed"]))
        self.radius = randint(int(kw["config"]["bubble"]["minRadius"]), int(kw["config"]["bubble"]["maxRadius"]))

    def onUpdate(self, event, **kw):
        self.xSpeed = randint(int(kw["stats"]["bubspeed"]) - 3, int(kw["stats"]["bubspeed"]))
        self._onMove()
