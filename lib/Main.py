class Game(object):
    def __init__(self, launcher_cfg):
        from threadsafe_tkinter import Tk
        from . import registry
        self._root = Tk()
        self._root.wm_attributes("-fullscreen", True)
        self.registry = registry

        self.launcher_cfg = launcher_cfg
        self.pre_initialize()
        self.initialize()
        self.post_initialize()

        from .title import TitleMenu
        from .slots import SlotsMenu
        self.t_choice = TitleMenu().get()
        self.active = True
        while self.active:
            if self.t_choice == "start":
                self.slotsMenu = SlotsMenu(self.start_game, self.return_title)
            elif self.t_choice == "quit":
                print("Quit")
                self.active = False
            else:
                print("error")
        exit(0)

    def return_title(self, slots_menu):
        from .title import TitleMenu
        slots_menu.destroy()
        self.t_choice = TitleMenu().get()

    # noinspection PyPep8Naming
    def pre_initialize(self):
        # Register Init
        self.registry.init()

        # Register Launcher Config
        self.registry.add_register("LauncherCfg")

        lCfgKeys = list(self.launcher_cfg.keys())
        lCfgValues = list(self.launcher_cfg.values())
        for i in range(len(self.launcher_cfg.keys())):
            key = lCfgKeys[i]
            value = lCfgValues[i]
            self.registry.register("LauncherCfg", key, value)

        # Register Config
        from json import JSONDecoder, JSONDecodeError, JSONEncoder
        try:
            with open("config.json") as file:
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
            with open("config.json", "w+") as file:
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
            with open("config.json", "w+") as file:
                file.write(JSONEncoder().encode(config))
            Warning(*err.args)

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
            self.registry.register("Bubbles", "%s:%s" % (i.bubble_prefix, i.bubble_id), i)
        for i in EVENTS:
            self.registry.register("Events", "%s:%s" % (i.event_prefix, i.event_id))
        self.registry.register("Config", "ScoreEval", "({radius}+{speed})*{multiplier}")

        # registry.register("Events", )

    def post_initialize(self):
        self.registry.add_register("Stats")

    def start_game(self):
        print("Game Stating")

    def mainloop(self):
        from .stats import get_stats, set_stats, add_stats, get_stat
        for i in get_stat("Bubbles"):
            i.update()
