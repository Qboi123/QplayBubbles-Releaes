from typing import *

# from .sprites import Bubble

stats: Dict[str, dict] = \
    {"Bubbles": {"bub-id": [],
                 "bub-action": [],
                 "bub-speed": [],
                 "bub-hardness": [],
                 "bub-rad": [],
                 "bub-radius": []},
     "Game": {"seed": 123456789,
              "x-update": 0,
              "coins": 0,
              "diamonds": 0,
              "level": 1,
              "level-score": 10000,
              "lives": 7,
              "score": 0,
              "hiscore": 0,
              "teleports": 0,
              "bubspeed": 5,
              "confusion": False,
              "confusion-time": 0,
              "notouch": False,
              "notouch-time": 0,
              "paralis": False,
              "paralis-time": 0,
              "scorestate": 1,
              "scorestate-time": 0,
              "secure": False,
              "secure-time": 0,
              "shipspeed": 10,
              "shotspeed": 0.1,
              "shotspeed-time": 0,
              "slowmotion": False,
              "slowmotion-time": 0,
              "special-level": False,
              "special-level-time": 0,
              "speedboost": False,
              "speedboost-time": 0,
              "timebreak": False,
              "timebreak-time": 0,
              "ship-position": [960, 540]
              },
     "Modes": {"store": False,
               "present": False,
               "teleport": False,
               "pause": False,
               "window": False}
     }


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


def set_kwstats(**kwargs):
    global stats
    for i in range(len(kwargs.keys())):
        key = list(kwargs.keys())[i]
        value = list(kwargs.values())[i]
        stats[key] = value
    return stats


def set_stats(name: str, _dict: dict):
    global stats
    stats[name] = _dict
    return stats


def set_stat(name: str, **kwargs):
    global stats
    for i in range(len(kwargs.keys())):
        stats[name][list(kwargs.keys())[i]] = list(kwargs.values())[i]
    return stats


def get_stat(name: str, key: str):
    global stats
    return stats[name][key]


def get_stats(name: str):
    global stats
    return stats[name]


def get_allstats():
    global stats
    return stats

# if __name__ == '__main__':
#     init()
#     print("Will be: {}")
#     print("Stats:   %s" % str(get_allstats()))
#     add_stats(a=3, b=2, c=1)
#     print("Will be: {'a': 3, 'b': 2, 'c': 1}")
#     print("Stats:   %s" % str(get_allstats()))
#     set_stat(a=4, b=5)
#     print("Will be: {'a': 4, 'b': 5, 'c': 1}")
#     print("Stats:   %s" % str(get_allstats()))
