from typing import *

import json
import pickle
import builtins


class Reader(object):
    def __init__(self, config_file):
        file = open(config_file, "rb")
        self.data = pickle.load(file)
        file.close()

    def get_decoded(self):
        return self.data


class Convert(json.JSONDecoder):
    def __init__(self, config_file):
        super().__init__()
        file = open(config_file, "r")
        self.json = file.read()
        file.close()
        self.config_file = config_file

    def convert(self):
        file = open(self.config_file[:-5]+".data", "wb+")
        print(self.json)
        pickle.dump(self.decode(self.json), file)
        file.close()


class ConvertBubble(object):
    def __init__(self, _bubble_index, _bubble_data):
        pass


class File():
    def __init__(self, config_file):
        self._fp = open(config_file, "wb+")

    def read(self) -> Any:
        return pickle.load(self._fp, True)

    def write(self, o) -> object:
        pickle.dump(o, self._fp, None, True)

    def load(self) -> Any:
        return self.read()

    def dump(self, o) -> object:
        return self.write(o)

    def close(self):
        self._fp.close()


class ConfigReader(json.JSONDecoder):
    def __init__(self, config_file):
        super().__init__()
        file = open(config_file, "r")
        self.json = file.read()
        file.close()
        self.config_file = config_file

    def get_decoded(self):
        return self.decode(self.json)


class Writer(object):
    def __init__(self, config_file, obj, flags="wb"):
        file = open(config_file, flags)
        pickle.dump(obj, file)
        file.close()
