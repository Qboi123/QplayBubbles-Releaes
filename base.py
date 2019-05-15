from .components import Store
from .fake_main import Game


# noinspection PyMissingConstructor
class StoreItem(Store):
    def __init__(self, parent: Game):
        self.parent = parent

    def on_buy(self, parent: Game):
        pass

    def on_select(self, parent: Game):
        pass


class EventCatcher:
    def __init__(self, parent: Game):
        self.parent = parent

    def on_update(self, parent: Game):
        pass

    def on_t_update(self, parent: Game):
        pass
