import string
from time import time
from typing import Callable, Union
from qbubbles import globals as g
from qbubbles.exceptions import UnlocalizedNameError


class BaseEffect(object):
    def __init__(self):
        self.callWhen: Callable = lambda game, time, strength: None

    def __call__(self, game, time, strength):
        if not self.callWhen(game, time, strength):
            return

        active_effects =[applied_effect.baseEffectClass for applied_effect in game.player.appliedEffects]
        for applied_effect in self.incompatibles:
            if applied_effect in active_effects:
                return

        return AppliedEffect(self, game, time, strength)

    def set_unlocalized_name(self, name):
        for symbol in name:
            if symbol not in string.ascii_letters+string.digits+"_":
                raise UnlocalizedNameError(f"Invalid character '{symbol}' for unlocalized name '{name}'")
        if name[0] not in string.ascii_letters:
            raise UnlocalizedNameError(f"Invalid start character '{name[0]}' for unlocalized name '{name}'")
        if name[-1] not in string.ascii_letters+string.digits:
            raise UnlocalizedNameError(f"Invalid start character '{name[-1]}' for unlocalized name '{name}'")

        if self in g.EFFECT2NAME.keys():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has already an unlocalized name")
        if self in g.NAME2EFFECT.values():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has already an unlocalized name")
        if name in g.EFFECT2NAME.values():
            raise ValueError(f"Name '{name}' already defined for effect '{self.__class__.__module__}.{self.__class__.__name__}'")
        if name in g.NAME2EFFECT.keys():
            raise ValueError(f"Name '{name}' already defined for effect '{self.__class__.__module__}.{self.__class__.__name__}'")

        g.EFFECT2NAME[self] = name
        g.NAME2EFFECT[name] = self

        return self.get_unlocalized_name()

    def __repr__(self):
        return f"Effect(<{self.get_unlocalized_name()}>)"

    def get_unlocalized_name(self):
        if self not in g.EFFECT2NAME.keys():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has no unlocalized name")

        return g.EFFECT2NAME[self]


class AppliedEffect(object):
    def __init__(self, base_class: BaseEffect, game, time_length: float, strength: Union[float, int]):
        self.baseEffectClass: BaseEffect = base_class
        self.baseEffectId: str = base_class.get_unlocalized_name()

        self._endTime = time() + time_length

    def get_end_time(self):
        return self._endTime

    def get_data(self):
        return {"id": self.baseEffectId, "time": self.get_remaining_time()}

    def get_unlocalized_name(self):
        self.baseEffectClass.get_unlocalized_name()

    def get_remaining_time(self):
        return self._endTime - time()

    def set_remaining_time(self, time_length: int):
        self._endTime = time() + time_length
