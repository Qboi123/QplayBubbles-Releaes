from lib.utils import seedrange, seedint
from .get_set import *
from ..registry import *
from ..stats import get_stats


def create_bubble():
    bubbles = get_register("Bubbles")
    seed = get_stats("Game")["seed"]
    xupd = get_stats("Game")["x-update"]
    for bubble in bubbles:
        if round(seedint(seed, xupd, 0, 0, 65535) <= bubble.rarity:
            bubble.create()
