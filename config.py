import json


class Reader(json.JSONDecoder):
    def __init__(self, config_file):
        super().__init__()
        file = open(config_file, "r")
        self.json = file.read()
        file.close()
        self.config_file = config_file

    def get_decoded(self):
        return self.decode(self.json)


class Writer(json.JSONEncoder):
    def __init__(self, config_file, obj):
        super().__init__()
        self.json = self.encode(obj)
        file = open(config_file, "w")
        file.write(self.json)
        file.close()
