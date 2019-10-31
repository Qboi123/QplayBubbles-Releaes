from typing import *
from .sprites import Bubble

stats: Dict[str, Union[List[Type[Bubble]], Dict]] = {"Bubbles": List[Type[Bubble]], "Game": Dict}


def init():
    global stats
    stats = {}


def add_stats(**kwargs):
    global stats
    for i in range(len(kwargs.keys())):
        key = list(kwargs.keys())[i]
        value = list(kwargs.values())[i]
        stats[key] = value
    return stats


def set_stats(**kwargs):
    global stats
    for i in range(len(kwargs.keys())):
        key = list(kwargs.keys())[i]
        value = list(kwargs.values())[i]
        stats[key] = value
    return stats


def get_stat(name: str):
    global stats
    return stats[name]


def get_stats():
    global stats
    return stats


if __name__ == '__main__':
    init()
    print("Will be: {}")
    print("Stats:   %s" % str(get_stats()))
    add_stats(a=3, b=2, c=1)
    print("Will be: {'a': 3, 'b': 2, 'c': 1}")
    print("Stats:   %s" % str(get_stats()))
    set_stats(a=4, b=5)
    print("Will be: {'a': 4, 'b': 5, 'c': 1}")
    print("Stats:   %s" % str(get_stats()))
