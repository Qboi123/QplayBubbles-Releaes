from typing import *

registry: Dict[str, Type[Union[Dict[str, Type[object]]]]] = {}


def init():
    global registry
    registry = {}


# noinspection PyDefaultArgument
def add_register(name, _dict: Type[Union[Dict[str, Type[object]]]] = {}):
    global registry
    registry[name] = _dict


def register(name: str, key: str, value: object):
    global registry
    registry[name][key] = value


def set_register(name: str, value: Type[Union[Dict[str, Type[object]]]]):
    global registry
    registry[name] = value


def get_value(name: str, key: str):
    global registry
    return registry[name][key]


def get_register(name: str):
    global registry
    return registry[name]


def get_whole_registry():
    global registry
    return registry
