from .components import Store
from .fake_main import Game


# noinspection PyMissingConstructor
class StoreItem(Store):
    def __init__(self, parent: Game):
        self.parent = parent

    def on_buy(self, parent: Game):
        pass
