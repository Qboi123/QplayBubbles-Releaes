from typing import Callable


class Status(object):
    def __init__(self):
        pass

    def on_bubble_popped(self, player: Callable, ):
        pass

class SpeedUp(Status):
    def __init__(self):
        Status.__init__(self)
