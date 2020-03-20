# def hello_world(a=dict, b=dict, c=dict, d=dict):
#     print(a, b, c, d)
#
# a = hello_world
# args = {"a": 3, "b": 8, "c": 12, "d": 1}
# print(a.__call__(**args))

import runpy

d = {}

runpy._run_code(
    """
    """, d, d)

def exclusion_generator(base_dict, to_excludes):
    for item in base_dict.copy().keys():
        if item in to_excludes:
            del base_dict[item]

e = {}

file = open("items.py", "r")
runpy._run_code(file.read(), e, e)

exclusion_generator(e, d.keys())

# print(list(e.items()))
f = []
for i in tuple(e.items()):
    if (not i[0] == "BaseItem") and (not i[0] == "State") and (not i[0] == "BaseBubble") and (
            not i[0] == "BaseState") and  (not i[0] == "BaseEvolve") and (not i[0] == "BaseScript"):
        if i[1].type == "item":
            f.append(i[1])

item = f[self.selected]

func = item.use

kwargs = {}

if "stats" in item.required:
    kwargs["stats"] = stats
if "canvas" in item.required:
    kwargs["canvas"] = canvas
if "log" in item.required:
    kwargs["log"] = log
if "root" in item.required:
    kwargs["root"] = root
if "modes" in item.required:
    kwargs["modes"] = modes
if "temp" in item.required:
    kwargs["temp"] = modes
if "commands" in item.required:
    kwargs["commands"] = commands
if "store_exit" in item.required:
    kwargs["store_exit"] = self.exit
if "backgrounds" in item.required:
    kwargs["backgrounds"] = backgrounds
if "texts" in item.required:
    kwargs["texts"] = texts
func(**kwargs)
# print(f)
