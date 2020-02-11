from lib.utils.get_set import get_root


class Init(object):
    def __init__(self, registry, launcher_cfg):
        self._root = get_root()
        self.registry = registry
        self.launcherConfig = launcher_cfg

    # noinspection PyPep8Naming
    def pre_initialize(self):
        # Register Init
        self.registry.init()

        # Register Launcher Config
        self.registry.add_register("LauncherCfg")

        lCfgKeys = list(self.launcherConfig.keys())
        lCfgValues = list(self.launcherConfig.values())
        for i in range(len(self.launcherConfig.keys())):
            key = lCfgKeys[i]
            value = lCfgValues[i]
            self.registry.register("LauncherCfg", key, value)

        # Register Config
        from json import JSONDecoder, JSONDecodeError, JSONEncoder
        try:
            with open("config/config.json") as file:
                config: dict = JSONDecoder().decode(file.read())
                if "font" not in config.keys():
                    config2 = {"font": {"family": "helvetica",
                                        "size": -9
                                        }
                               }
                    config.update(**config2)
        except FileNotFoundError:
            config = {"bubble": {"chance": 10,
                                 "max-radius": 30,
                                 "min-radius": 21,
                                 "max-speed": 4.8,
                                 "base-speed": 4.8,
                                 "screen-gap": 100
                                 },
                      "game": {"level-score": 10000,
                               "time-limit": 90,
                               "pause": False,
                               "resolution": "1920x1080",
                               "ship-radius": 15,
                               "ship-speed": 10,
                               "fullscreen": True,
                               "language": "en"
                               },
                      "font": {"family": "helvetica",
                               "size": -9
                               }
                      }
            with open("config/config.json", "w+") as file:
                file.write(JSONEncoder().encode(config))
        except JSONDecodeError as err:
            config = {"bubble": {"chance": 10,
                                 "max-radius": 30,
                                 "min-radius": 21,
                                 "max-speed": 4.8,
                                 "base-speed": 4.8,
                                 "screen-gap": 100
                                 },
                      "game": {"level-score": 10000,
                               "time-limit": 90,
                               "pause": False,
                               "resolution": "1920x1080",
                               "ship-radius": 15,
                               "ship-speed": 10,
                               "fullscreen": True,
                               "language": "en"
                               },
                      "font": {"family": "helvetica",
                               "size": -9
                               }
                      }
            with open("config/config.json", "w+") as file:
                file.write(JSONEncoder().encode(config))
            Warning(*err.args)

        config["height"] = self._root.winfo_height()
        config["width"] = self._root.winfo_width()
        config["middle-y"] = self._root.winfo_height()
        config["middle-x"] = self._root.winfo_width()

        # noinspection PyTypeChecker
        self.registry.add_register("Config", config)
        print(self.registry.get_register("Config"))

        # Register Launguage
        self.registry.add_register("Launguage")

        from yaml import unsafe_load
        file = open("lang/%s.yaml" % config["game"]["language"])
        lang = unsafe_load(file)
        file.close()

        self.registry.registry["Language"] = lang

        # Other Registers
        self.registry.add_register("Events")
        self.registry.add_register("Sprites")
        self.registry.add_register("Bubbles")

    def initialize(self):
        from .classes import BUBBLES, EVENTS, SPRITES

        for i in SPRITES:
            self.registry.register("Sprites", "%s:%s" % (i.sprite_prefix, i.sprite_id), i)
        for i in BUBBLES:
            self.registry.register("Bubbles", f"qplay:{i.get_unlocalized_name()}", i)
        for i in EVENTS:
            self.registry.register("Events", "%s:%s" % (i.event_prefix, i.event_id), i)
        self.registry.register("Config", "ScoreEval", "({radius}+{speed})*{multiplier}")

        # registry.register("Events", )

    def post_initialize(self):
        """
        Post initialization.
        """
        # self.registry.add_register("Stats")
        self._root.game = self
