# noinspection PyUnresolvedReferences
from extras import dict2class
import json

with open("config/slotInfo.nzt") as file:
    dict = json.decoder.JSONDecoder().decode(file.read())

obj = dict2class(dict)

print(obj.version.pre)
version = obj.version
print("%s.%s.%s-pre%s" % (version.a, version.b, version.c, version.pre)

