from events import UpdateEvent, CollisionEvent, KeyPressEvent, KeyReleaseEvent, XInputEvent
from registry import Registry


class GameMap(object):
    def __init__(self, *args, **kwargs):
        pass

    def create_random_bubbe(self, x: None, y: None):
        bubble = BubbleSystem.get_random()

        if x is None:
            x = Registry.gameData["WindowWidth"] + radius

    def on_update(self, evt: UpdateEvent):


    def on_playermotion(self, evt: PlayerMotionEvent):
        pass

    def on_collision(self, evt: CollisionEvent):
        pass

    def on_keypress(self, evt: KeyPressEvent):
        pass

    def on_keyrelease(self, evt: KeyReleaseEvent):
        pass

    def on_xinput(self, evt: XInputEvent):
        pass
