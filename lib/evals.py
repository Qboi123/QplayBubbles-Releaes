from typing import *


def score_eval(_eval: str, sprite):
    if hasattr(sprite, "scoreMultiplier"):
        score_multiplier = sprite.scoreMultiplier
    else:
        score_multiplier = 0
    if hasattr(sprite, "radius"):
        radius = sprite.radius
    else:
        radius = 1
    eval(_eval.format(radius=radius, multiplier=score_multiplier))


def minspeed_eval(_eval: str, **kwargs: Dict[str, int]):
    # if hasattr(sprite, "scoreMultiplier"):
    #     score_multiplier = sprite.scoreMultiplier
    # else:
    #     score_multiplier = 0
    # if hasattr(sprite, "radius"):
    #     radius = sprite.radius
    # else:
    #     radius = 1
    eval(_eval.format(**kwargs))


def maxspeed_eval(_eval: str, **kwargs: Dict[str, int]):
    eval(_eval.format(**kwargs))
