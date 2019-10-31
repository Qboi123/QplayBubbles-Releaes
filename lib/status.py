from .player import Player


class Status(object):
    def __init__(self):
        pass

    def on_bubble_popped(self, player: Player, ):
        pass

class SpeedUp(Status):
    def __init__(self):
        Status.__init__(self)
