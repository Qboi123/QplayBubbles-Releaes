from random import Random
from typing import Dict, Tuple

from qbubbles.bubbleSystem import BubbleSystem
from qbubbles.events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent
from qbubbles.registry import Registry


class GameMap(object):
    def __init__(self, seed, randoms=None, *args, **kwargs):
        self.seedRandom = seed
        self.randoms: Dict[str, Tuple[Random, int]] = {}
        if randoms is not None:
            for random in randoms:
                randomState = random["State"]
                offset = random["offset"]
                id = random["id"]
                self.randoms[id] = (Random(self.seedRandom << offset).setstate(randomState), offset)
        else:
            self.randoms["qbubbles:bubble_system"] = self.format_random(4096)
        self._uname = None
        self._uname = None

    def format_random(self, offset):
        if offset % 4 == 0:
            return Random(self.seedRandom << offset), offset
        else:
            raise ValueError("Offset must be multiple of 4")

    def __setattr__(self, key, value):
        if key == "format_random":
            if value != self.format_random:
                raise PermissionError("Cannot set format_random")
        self.__dict__[key] = value

    def set_uname(self, uname):
        self._uname = uname

    def get_uname(self):
        return self._uname

    def get_save_data(self):
        randoms = []
        for id, data in self.randoms.items():
            sdata = {}
            random: Random = data[0]
            sdata["State"] = random.getstate()
            sdata["offset"] = data[1]
            sdata["id"] = id
            randoms.append(sdata)

    def create_random_bubbe(self, x: None, y: None):
        bubble = BubbleSystem.random(self.randoms["qbubbles:bubble_system"][0])
        radius = 0

        if x is None:
            x = Registry.gameData["WindowWidth"] + radius

    def on_update(self, evt: UpdateEvent):
        pass

    # def on_playermotion(self, evt: PlayerMotionEvent):
    #     pass

    def on_collision(self, evt: CollisionEvent):
        pass

    def on_keypress(self, evt: KeyPressEvent):
        pass

    def on_keyrelease(self, evt: KeyReleaseEvent):
        pass

    def on_xinput(self, evt: XInputEvent):
        pass

    def __repr__(self):
        return f"GameMap<{self.get_uname()}>"


class ClassicMap(GameMap):
    def __init__(self):  # , seed, *args, **kwargs):
        super(GameMap, self).__init__()

        randoms=None
        self.seedRandom = 4096
        print(dir(self))

        self.randoms: Dict[str, Tuple[Random, int]] = {}
        if randoms is not None:
            for random in randoms:
                randomState = random["State"]
                offset = random["offset"]
                id = random["id"]
                self.randoms[id] = (Random(self.seedRandom << offset).setstate(randomState), offset)
        else:
            self.randoms["qbubbles:bubble_system"] = self.format_random(4096)
        self._uname = None
        self._uname = None

        self.set_uname("qbubbles:classic_map")
