from time import time
from .extras import get_coords


def create_shot(c, ammo, config, ship, stats):
    """
    Creates Shooting ammo
    """
    if ammo["retime"] < time():
        x, y = get_coords(c, ship["id"])
        ammo["ammo-id"].append(c.create_line(10 + x + config["game"]["ship-radius"] / 2, y, 15 + x + config["game"]["ship-radius"] / 2,
                                             y, fill="yellow"))
        ammo["ammo-speed"].append(stats["shotspeed"])
        ammo["ammo-damage"].append(0)
        ammo["retime"] = time() + 0.5


def move_ammo(c, log, root, ammo):
    """
    Motion for ammo.
    """
    for i in range(len(ammo["ammo-id"])-1, -1, -1):
        try:
            c.move(ammo["ammo-id"][i], ammo["ammo-speed"][i], 0)
        except IndexError:
            log.warning("move_ammo", "Can't move ammo index '" + str(i) + "'.")
        root.update()


def del_shoot(c, i, ammo):
    """
    Deletes ammo by request.
    :param c:
    :param ammo:
    :param i:
    :return:
    """
    c.delete(ammo["ammo-id"][i])
    del ammo["ammo-id"][i]
    del ammo["ammo-speed"][i]
    del ammo["ammo-damage"][i]


def clean_up_shots(c, ammo, config):
    """
    Removes ammo if it's off screen.
    :return:
    """
    for i in range(len(ammo["ammo-id"]) - 1, -1, -1):
        x, y = get_coords(c, ammo["ammo-id"][i])
        if x > config["width"] + config["screen-gap"]:
            del_shoot(c, i, ammo)
