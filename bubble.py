from .ammo import *
from .info import *
from .components import *
from .extras import play_sound


def place_bubble(c, bub, x, y, r, act):
    """
    Places a bubble.
    The bubble can't moving or removed (only by closing game).
    :param c:
    :param bub:
    :param x:
    :param y:
    :param r:
    :param act:
    """

    if act == "Normal":
        return c.create_image(x, y, image=bub["Normal"][r * 2])
    if act == "Double":
        return c.create_image(x, y, image=bub["Double"][r * 2])
    if act == "Kill":
        return c.create_image(x, y, image=bub["Kill"][r * 2])
    if act == "Triple":
        return c.create_image(x, y, image=bub["Triple"][r * 2])
    if act == "SpeedUp":
        return c.create_image(x, y, image=bub["SpeedUp"][r * 2])
    if act == "SpeedDown":
        return c.create_image(x, y, image=bub["SpeedDown"][r * 2])
    if act == "Up":
        return c.create_image(x, y, image=bub["Up"][r * 2])
    if act == "Ultimate":
        return c.create_image(x, y, image=bub["Ultimate"][r * 2])
    if act == "DoubleState":
        return c.create_image(x, y, image=bub["DoubleState"][r * 2])
    if act == "Protect":
        return c.create_image(x, y, image=bub["Protect"][r * 2])
    if act == "SlowMotion":
        return c.create_image(x, y, image=bub["SlowMotion"][r * 2])
    if act == "TimeBreak":
        return c.create_image(x, y, image=bub["TimeBreak"][r * 2])
    if act == "Confusion":
        return c.create_image(x, y, image=bub["Confusion"][r * 2])
    if act == "HyperMode":
        return c.create_image(x, y, image=bub["HyperMode"][r * 2])
    if act == "ShotSpdStat":
        return c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])
    if act == "Teleporter":
        return c.create_image(x, y, image=bub["Teleporter"][r * 2])
    if act == "Coin":
        return c.create_image(x, y, image=bub["Coin"])
    if act == "NoTouch":
        return c.create_image(x, y, image=bub["NoTouch"][r * 2])
    if act == "LevelKey":
        return c.create_image(x, y, image=bub["Key"][60])
    if act == "Paralis":
        return c.create_image(x, y, image=bub["Paralis"][r * 2])
    if act == "SpecialKey":
        return c.create_image(x, y, image=bub["SpecialKey"][48])
    if act == "Diamond":
        return c.create_image(x, y, image=bub["Diamond"][36])
    if act == "StoneBub":
        return c.create_image(x, y, image=bub["StoneBub"][r * 2])
    if act == "Present":
        return c.create_image(x, y, image=bub["Present"][40])


def create_bubble(stats, config, bub, c, bubble, modes, index, i=None, x=None, y=None, r=None, s=None):
    """
    Creates a bubble that can moving and removing by touching with the ship
    :param index:
    :param modes:
    :param s:
    :param bubble:
    :param c:
    :param bub:
    :param config:
    :param stats:
    :param i:
    :param x:
    :param y:
    :param r:
    Todo: Add more bubbles.
    """
    from random import randint
    if x is None:
        x = config["width"] + config["bubble"]["screen-gap"]
    else:
        x = x
    if r is None:
        r = randint(int(config["bubble"]["min-radius"]), int(config["bubble"]["max-radius"]))
    else:
        r = r
    if y is None:
        y = randint(72 + r, (config["height"] - r))
    else:
        y = y
    if i is None:
        i = randint(0, 1600)
    else:
        i = i
    if stats["level"] <= 100:
        level_dat = stats["level"]
    else:
        level_dat = 100
    if 0 <= i < 800:
        ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
        act = "Normal"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 800 <= i < 830:
        ids = [c.create_image(x, y, image=bub["Double"][r * 2])]
        act = "Double"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 830 <= i < 930:
        ids = [c.create_image(x, y, image=bub["Kill"][r * 2])]
        act = "Kill"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 930 <= i < 940:
        ids = [c.create_image(x, y, image=bub["Triple"][r * 2])]
        act = "Triple"
        spd = randint(int(stats["bubspeed"]) + 2, int(stats["bubspeed"]) + 6)
        hardness = 1
    elif 940 <= i < 950:
        ids = [c.create_image(x, y, image=bub["SpeedUp"][r * 2])]
        act = "SpeedUp"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 3)
        hardness = 1
    elif 950 <= i < 960:
        ids = [c.create_image(x, y, image=bub["SpeedDown"][r * 2])]
        act = "SpeedDown"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 3)
        hardness = 1
    elif 960 <= i < 965:
        if stats["lives"] < 7:
            ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
            act = "Up"
            spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 3)
            hardness = 1
        else:
            ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
            act = "Normal"
            spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
            hardness = 1
    elif 973 <= i < 974:
        ids = [c.create_image(x, y, image=bub["Ultimate"][r * 2])]
        act = "Ultimate"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif 974 <= i < 976:
        ids = [c.create_image(x, y, image=bub["DoubleState"][r * 2])]
        act = "DoubleState"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif 979 <= i < 981:
        ids = [c.create_image(x, y, image=bub["Protect"][r * 2])]
        act = "Protect"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif 981 <= i < 984:
        ids = [c.create_image(x, y, image=bub["SlowMotion"][r * 2])]
        act = "SlowMotion"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif 984 <= i < 985:
        ids = [c.create_image(x, y, image=bub["TimeBreak"][r * 2])]
        act = "TimeBreak"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r * 2])]
        act = "HyperMode"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])]
        act = "ShotSpdStat"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 985 <= i < 1085:
        ids = [c.create_image(x, y, image=bub["Confusion"][r * 2])]
        act = "Confusion"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 1085 <= i < 1100:
        ids = [c.create_image(x, y, image=bub["Paralis"][r * 2])]
        act = "Paralis"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 1100 <= i < 1101:
        ids = [c.create_image(x, y, image=bub["HyperMode"][r * 2])]
        act = "HyperMode"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 1101 <= i < 1120:
        ids = [c.create_image(x, y, image=bub["ShotSpdStat"][r * 2])]
        act = "ShotSpdStat"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1
    elif 1120 <= i < 1121 and stats["level"] > 19:
        ids = [c.create_image(x, y, image=bub["Teleporter"][r * 2])]
        act = "Teleporter"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
        hardness = 1
    elif 1121 <= i < 1123 and stats["level"] > 4:
        ids = [c.create_image(x, y, image=bub["Diamond"][36])]
        r = 18
        act = "Diamond"
        spd = randint(int(stats["bubspeed"]) + 2, int(stats["bubspeed"]) + 4)
        hardness = 1
    elif 1124 <= i < 1130 and stats["level"] > 4:
        ids = [c.create_image(x, y, image=bub["Coin"])]
        r = 20
        act = "Coin"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
        hardness = 2
    elif 1130 <= i < 1150 and stats["level"] > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["NoTouch"][r * 2])]
        act = "NoTouch"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
        hardness = 1
    elif 1150 <= i < 1160 and stats["level"] > 4:
        r = 20
        ids = [c.create_image(x, y, image=bub["Present"][40])]
        act = "Present"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
        hardness = 1
    elif 1160 <= i < 1263 + (197 * level_dat / 100):
        ids = [c.create_image(x, y, image=bub["StoneBub"][r * 2])]
        act = "StoneBub"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 3 + int(level_dat / 2)
        # elif 1360 <= i < ???:
    elif 1460 <= i < 1491:
        ids = [c.create_image(x, y, image=bub["Coin"])]
        r = 20
        act = "Coin"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 2)
        hardness = 2
    elif 1491 <= i < 1492:
        ids = [c.create_image(x, y, image=bub["SpecialKey"][48])]
        r = 24
        act = "SpecialKey"
        spd = randint(int(stats["bubspeed"]) + 5, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif i == -1:
        ids = [c.create_image(x, y, image=bub["Key"][60])]
        r = 26
        act = "LevelKey"
        spd = randint(int(stats["bubspeed"]) + 4, int(stats["bubspeed"]) + 8)
        hardness = 1
    elif i == -2:
        ids = [c.create_image(x, y, image=bub["Up"][r * 2])]
        act = "Up"
        spd = randint(int(stats["bubspeed"]), int(stats["bubspeed"]) + 3)
        hardness = 1
    else:
        ids = [c.create_image(x, y, image=bub["Normal"][r * 2])]
        act = "Normal"
        spd = randint(int(stats["bubspeed"]) - 3, int(stats["bubspeed"]))
        hardness = 1

    if s is not None:
        spd = s
    bubble["bub-special"].append(False)
    bubble["bub-index"].append(i)
    bubble["bub-position"].append([x, y])
    bubble["bub-hardness"].append(hardness)
    bubble["bub-action"].append(act)
    bubble["bub-id"].append(ids)
    bubble["bub-radius"].append(r)
    bubble["bub-speed"].append(spd)
    index = bubble["bub-id"].index(ids, 0, len(bubble["bub-id"]))
    if not bubble["active2"][index]:
        bubble["active2"][index] = True
        bubble["active"] += 1
    # Thread(None, lambda: movebubble_thread(ids, bubble, spd, act, ids[0], r, c, stats, modes)).start()


def move_bubbles(bubble, stats, root, canvas):
    """
    The base of motion for the bubbles
    """
    try:
        for i in range(len(bubble["bub-id"])):
            Thread(None, lambda: Collision.move_bubble(i, bubble, canvas, stats, root)).start()
    except IndexError:
        pass
    except TclError:
        exit(0)


def del_bubble(index, bubble, canvas):
    """
    Removes a bubble.
    :param canvas:
    :param bubble:
    :param index:
    """
    del bubble["bub-radius"][index]
    del bubble["bub-speed"][index]
    for j in bubble["bub-id"][index]:
        canvas.delete(j)
    del bubble["bub-id"][index]
    if bubble["bub-action"][index] == "LevelKey":
        bubble["key-active"] = False
    del bubble["bub-action"][index]
    del bubble["bub-hardness"][index]
    del bubble["bub-position"][index]
    del bubble["bub-index"][index]


def clean_up_bubs(bubble, canvas, config):
    """
    Removes bubbles that's out of screen. If x is lower than -100
    """
    try:
        for index in range(len(bubble["bub-id"]) - 1, -1, -1):
            x, y = get_coords(canvas, bubble["bub-id"][index][0])
            if x < -100:
                # Checks if the Level-key is active.
                # If it's active then sets it the variable
                # for the key-bubble to off.
                if bubble["bub-action"][index] == "LevelKey":
                    bubble["key-active"] = False
                del_bubble(index, bubble, canvas)
    except IndexError:
        pass


def clean_level_keys(bubble, canvas):
    """
    Removes all Level-Keybubble.
    :param bubble:
    :param canvas:
    :return:
    """
    for index in range(len(bubble["bub-action"]) - 1, -1, -1):
        try:
            if bubble["bub-action"][index] == "LevelKey":
                del_bubble(index, bubble, canvas)
        except TypeError:
            pass
        except IndexError:
            pass


class Collision:
    def __init__(self):
        self.shot = None
        self.bub = None

    @staticmethod
    def move_bubble(index, bubble, canvas, stats, root):
        """
        Moves 1 bubble.
        :param root:
        :param stats:
        :param canvas:
        :param bubble:
        :param index:
        :rtype: object
        """
        try:
            for j in range(len(bubble["bub-id"][index]) - 1, -1, -1):
                if not bubble["bub-action"][index] == "Null":
                    if stats["slowmotion"]:
                        canvas.move(bubble["bub-id"][index][j], -bubble["bub-speed"][index] / 10, 0)
                    else:
                        canvas.move(bubble["bub-id"][index][j], -bubble["bub-speed"][index], 0)
                    root.update()
                x, y, = get_coords(canvas, bubble["bub-id"][index][j])
                bubble["bub-position"][index] = [x, y]
                canvas.update()
        except IndexError:
            pass
        except TclError:
            exit(0)
        except AttributeError:
            exit(0)

    @staticmethod
    def move_ammo(index, ammo, canvas, log):
        """
        Moves 1 ammo.
        :param log:
        :param canvas:
        :param ammo:
        :param index:
        :rtype: object
        """
        try:
            canvas.move(ammo["ammo-id"][index], ammo["ammo-speed"][index], 0)
        except IndexError:
            log.warning("move_ammo", "Can't move ammo index '" + str(index) + "'.")

    @staticmethod
    def coll_func(index, canvas, commands, root, log, stats, bubscore, action, bubble, backgrounds, texts, panels,
                  accept_negative):
        """
        Collision.
        All bubbles have a function.
        This Method sets a state or sets a variable.
        :param log:
        :param log:
        :param index:
        :param texts:
        :param commands:
        :param root:
        :param canvas:
        :param backgrounds:
        :param bubble:
        :param bubscore:
        :param stats:
        :param action:
        :param accept_negative:
        :return:
        """
        if action == "Normal":
            stats["score"] += bubscore * stats["scorestate"]
        if action == "Double":
            stats["score"] += bubscore * 2 * stats["scorestate"]
        if action == "Triple":
            stats["score"] += bubscore * 3 * stats["scorestate"]
        if (not stats["secure"]) and accept_negative:
            if action == "Kill":
                stats["lives"] -= 1
            if action == "Min":
                stats["score"] -= bubscore
            if action == "SpeedDown":
                if stats["shipspeed"] == 5:
                    return
                stats["shipspeed"] -= 5
            if action == "Confusion":
                State.set_state(canvas, log, stats, "Confusion", backgrounds)
            if action == "Paralis":
                State.set_state(canvas, log, stats, "Paralis", backgrounds)
            if action == "NoTouch":
                stats["score"] += bubscore * stats["scorestate"]
                State.set_state(canvas, log, stats, action, backgrounds)
        if action == "DoubleState":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "TripleState":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "SpeedUp":
            if stats["shipspeed"] == 20:
                return
            elif stats["shipspeed"] == 25:
                return
            stats["shipspeed"] += 5
        if action == "Up":
            stats["lives"] += 1
        if action == "Protect":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "SlowMotion":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "TimeBreak":
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "Ultimate":
            if stats["lives"] < 7:
                stats["lives"] += 1
            stats["shipspeed"] = 25
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "HyperMode":
            stats["lives"] += 2
            stats["shipspeed"] = 25
            stats["score"] += bubscore * 30 * stats["scorestate"]
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "ShotSpdStat":
            stats["score"] += bubscore * stats["scorestate"]
            State.set_state(canvas, log, stats, action, backgrounds)
        if action == "Diamond":
            stats["diamonds"] += 1
        if action == "Coin":
            stats["coins"] += 1
        if action == "Teleporter":
            stats["teleports"] += 1
        if action == "StoneBub":
            stats["score"] += (bubscore * (bubble["bub-hardness"][index] / 9))
        if action == "LevelKey":
            stats["level"] += 1
            # clean_level_keys()
            bubble["key-active"] = False
            view_level(canvas, root, texts, stats["level"])
        if action == "Present":
            commands["present"] = True
        play_sound("data/sounds/bubpop.mp3")
        if action == "SpecialKey":
            canvas.itemconfig(backgrounds["id"], image=backgrounds["special"])
            canvas.itemconfig(panels["game/top"], fill="#3f3f3f")
            stats["special-level"] = True
            stats["special-level-time"] = time() + 30
            log.info("State", "(CollFunc) Special Level State is ON!!!")
            play_sound("data/sounds/specialmode.mp3")
        log.debug("CollFunc", "Bubble popped with id: "+str(index)+" | action: "+action)

    @staticmethod
    def clean_up_bub(canvas, index, bubble, config, log):
        """
        Cleans 1 bubble.
        :param log:
        :param config:
        :param bubble:
        :param canvas:
        :rtype: object
        :param index:
        """
        try:
            x, y = get_coords(canvas, bubble["bub-id"][index][0])
            if x < -config["bubble"]["screen-gap"]:
                # Checks if the Level-key is active.
                # If it's active then sets it the variable
                # for the key-bubble to off.
                if bubble["bub-action"][index] == "LevelKey":
                    bubble["keyactive"] = False
                del_bubble(index, bubble, canvas)
        except IndexError as e:
            log.error("Collision.clean_up_bub", "IndexError: '"+e.args[0]+"' on line no. "+str(e.__traceback__.tb_lineno))

    @staticmethod
    def clean_up_shot(canvas, index, ammo, config):
        """
        Cleans 1 shot.
        :param canvas:
        :param config:
        :param ammo:
        :rtype: object
        :param index:
        """
        x, y = get_coords(canvas, ammo["ammo-id"][index])
        if x > config["width"] + config["bubble"]["screen-gap"]:
            del_shoot(canvas, index, ammo)

    def check_collision(self, root, commands, bubble, config, stats, ammo, ship, canvas, log, backgrounds, texts,
                        panels):
        """
        Collision bubble by touching or shooting the bubble
        :rtype: object
        """
        from .extras import distance, replace_list
        from threading import Thread
        for index_bub in range(len(bubble["bub-id"].copy()) - 1, -1, -1):
            # print(distance(canvas, log, ship["id"], bubble["bub-id"][index_bub][0]) - (config["game"]["ship-radius"] + bubble["bub-radius"][index_bub]))
            self.bub = index_bub
            try:
                if distance(canvas, log, ship["id"], bubble["bub-id"][index_bub][0]) < (
                        config["game"]["ship-radius"] + bubble["bub-radius"][index_bub]):
                    if not stats["notouch"]:
                        # Sets score / status etc. and deletes bubble
                        if bubble["bub-hardness"][index_bub] == 1:
                            Thread(None, lambda: self.coll_func(index_bub, canvas, commands, root, log, stats,
                                                                (bubble["bub-radius"][index_bub] +
                                                                 bubble["bub-speed"][index_bub]),
                                                                bubble["bub-action"][index_bub], bubble, backgrounds,
                                                                texts, panels, True)).start()
                            del_bubble(index_bub, bubble, canvas)
                        elif bubble["bub-hardness"][index_bub] > 1:
                            replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                if not stats["timebreak"]:
                    self.move_bubble(index_bub, bubble, canvas, stats, root)
                    canvas.update()
                    self.clean_up_bub(canvas, index_bub, bubble, config, log)
                # Collision with ammo
                for ammo_index in range(len(ammo["ammo-id"].copy()) - 1, -1, -1):
                    self.shot = ammo_index
                    if not stats["timebreak"]:
                        # self.move_ammo(ammo_index, ammo, canvas, log, )
                        self.clean_up_shot(canvas, ammo_index, ammo, config)
                    try:
                        if distance(canvas, log, ammo["ammo-id"][ammo_index], bubble["bub-id"][index_bub][0]) < (
                                1 + bubble["bub-radius"][index_bub]):
                            if bubble["bub-hardness"][index_bub] == 1:
                                try:
                                    Thread(None, lambda: self.coll_func(index_bub, canvas, commands, root, log, stats,
                                                                        (bubble["bub-radius"][index_bub] +
                                                                         bubble["bub-speed"][index_bub]),
                                                                        bubble["bub-action"][index_bub], bubble, backgrounds,
                                                                        texts, panels, False)).start()
                                except IndexError:
                                    pass
                                del_bubble(index_bub, bubble, canvas)
                                replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                                if ammo["ammo-damage"][ammo_index] > 4:
                                    del_shoot(canvas, ammo_index, ammo)
                                # Thread(None, PlaySound("data/bubpop.wav", 1)).start()
                            elif bubble["bub-hardness"][index_bub] > 1:
                                replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                                replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                                if ammo["ammo-damage"][ammo_index] > 4:
                                    del_shoot(canvas, ammo_index, ammo)
                            root.update()
                    except TypeError:
                        pass
                    except IndexError:
                        pass
                    except AttributeError:
                        exit(0)
                    except TclError:
                        exit(0)
            except TypeError:
                pass
            except IndexError:
                pass
            except TclError:
                exit(0)
            except AttributeError:
                exit(0)

def movebubble_thread(index, bubble, speed, action, id, radius, canvas, stats, modes):
    # print("start")
    index = bubble["bub-id"].index(index, 0, len(bubble["bub-id"]))
    while True:
        try:
            # print("ID: "+str(index)+"phase 1")
            if not stats["timebreak"] and not modes["pause"]:
                # print("ID: "+str(index)+"phase 2")
                if not action == "Null":
                    # print("ID: "+str(index)+"phase 3")
                    if stats["slowmotion"]:
                        canvas.move(id, -speed / 10, 0)
                        # print("ID: "+str(index)+'phase 4a')
                    else:
                        canvas.move(id, -speed, 0)
                        # list.
                        # print("phase 4b")
                    # print("ID: "+str(index)+str(bubble["active2"]))
                    # print("ID: "+str(index)+str(len(bubble["active2"])))
                    if not bubble["active2"][index]:
                        bubble["active2"][index] = True
                        bubble["active"] += 1
                        print(bubble["active"])
                    # print("Active:", bubble["active"])
                    # print("ID: "+str(index)+"phase 5")
                try:
                    x, y, = get_coords(canvas, id)
                    # print("ID: " + str(index) + "phase 6")
                    bubble["bub-position"][index] = [x, y]
                    # print("ID: "+str(index)+"phase 7")
                    # print(radius)
                    if x < -radius:
                        del_bubble(index, bubble, canvas)
                        return
                except IndexError:
                    pass
                # print("ID: "+str(index)+"move")
                canvas.update()
        except IndexError as e:
            print("ID: "+str(index), e.args)
            # print(bubble["bub-id"][0][0])
            return
        except TclError:
            # print("exit")
            exit(0)
        except AttributeError:
            # print("exit")
            exit(0)



def clean_all(bubble, canvas):
    """
    Deletes removes bubbles out of the game.
    """
    for i in len(bubble["bub-id"]) - 1, -1, -1:
        del_bubble(i, bubble, canvas)
