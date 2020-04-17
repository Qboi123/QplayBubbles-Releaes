import string
from time import time
from typing import Callable, Union, Optional, List, Type
from qbubbles import globals as g
from qbubbles.exceptions import UnlocalizedNameError


class BaseEffect(object):
    def __init__(self):
        self.callWhen: Callable[[object, float, Union[float, int]], bool] = lambda game, time, strength: True
        self.incompatibles: List[BaseEffect] = []

    def on_apply(self, effect: 'AppliedEffect', sprite):
        pass

    def on_stop(self, effect: 'AppliedEffect', sprite):
        pass

    def __call__(self, game, time, strength) -> Optional['AppliedEffect']:
        """
        Used for getting the applied effect for the sprite, featuring event handling and remaining time.

        :param game: The Game Scene
        :param time: The amount of time the effect shold be active
        :param strength: The strength of the effect
        :return: AppliedEffect instance or None if the BaseEffect callWhen call returns False.
        """
        if not self.callWhen(game, time, strength):
            return

        active_effects = [applied_effect.baseEffectClass for applied_effect in game.player.appliedEffects]
        for base_effect in self.incompatibles:
            if base_effect in active_effects:
                return
            if self.__class__ in base_effect.incompatibles:
                return

        return AppliedEffect(self, game, time, strength)

    def set_uname(self, name):
        """
        Sets the unlocalized name with given parameter.

        :param name:
        :return:
        """

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

        return self.get_uname()

    def __repr__(self):
        return f"Effect(<{self.get_uname()}>)"

    def get_uname(self):
        if self not in g.EFFECT2NAME.keys():
            raise ValueError(f"Effect '{self.__class__.__module__}.{self.__class__.__name__}' has no unlocalized name")

        return g.EFFECT2NAME[self]


class AppliedEffect(object):
    def __init__(self, base_class: BaseEffect, game, time_length: float, strength: Union[float, int]):
        self.baseEffectClass: BaseEffect = base_class
        self.baseEffectId: str = base_class.get_uname()
        self.strength = strength
        self._game = game

        self._endTime = time() + time_length

    def __repr__(self):
        return f"AppliefEffect(<{self.baseEffectClass.get_uname()}>, {self.get_remaining_time()}, {self.strength})"

    def get_end_time(self):
        return self._endTime

    def get_data(self):
        return {"id": self.baseEffectId, "time": self.get_remaining_time()}

    def get_unlocalized_name(self):
        self.baseEffectClass.get_uname()

    def get_remaining_time(self):
        return self._endTime - time()

    def set_remaining_time(self, time_length: int):
        self._endTime = time() + time_length


class SpeedBoostEffect(BaseEffect):
    def __init__(self):
        super(SpeedBoostEffect, self).__init__()

    def on_apply(self, effect: 'AppliedEffect', sprite):
        sprite.speed += (effect.strength * sprite.baseSpeed) / 4

    def on_stop(self, effect: 'AppliedEffect', sprite):
        sprite.speed -= (effect.strength * sprite.baseSpeed)


class DefenceBoostEffect(BaseEffect):
    def __init__(self):
        super(DefenceBoostEffect, self).__init__()

    def on_apply(self, effect: 'AppliedEffect', sprite):
        sprite.defence += effect.strength * 2

    def on_stop(self, effect: 'AppliedEffect', sprite):
        sprite.defence -= effect.strength * 2
