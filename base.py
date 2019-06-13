from .fake_main import Game

HORIZONTAL = "horizontal"
VERTICAL = "vertical"

TYPE_DANGEROUS = "dangerous"
TYPE_NEUTRAL = "neutral"

FORM_CIRCLE = "circle"
FORM_RECT = "rectangle/line"
FORM_LINE = "rectangle/line"

BUB_NOSTATE = "nostate"
BUB_WITHSTATE = "withstate"

LEFT = "left"
RIGHT = "right"
UP = "up"
DOWN = "down"

TRUE = True
FALSE = False

COLOR_RED = "red"

RED = COLOR_RED

ANY_BUBBLE = "any.bubble"
SHIP = "ship"

OBJ_SHIP = SHIP
OBJ_ANY_BUBBLE = ANY_BUBBLE
OBJ_BARIER = "barier"


# noinspection PyMissingConstructor
class StoreItem:
    def __init__(self, parent: Game):
        self.parent = parent
        self.coins = 0
        self.diamonds = 0

    def on_buy(self, parent: Game):
        pass

    def on_select(self, parent: Game):
        pass


class Event:
    def __init__(self):
        pass

    def on_update(self, parent: Game):
        pass

    def on_t_update(self, parent: Game):
        pass


DirectionWaring = Warning


# noinspection PyUnusedLocal
class Sprite:
    requires = ("sprites", "config", "canvas", "stats", "log", "ship", "bubbles")

    def __init__(self, **kw):
        name = "EmptySprite"

        self._kw = kw

        # Axis
        self.axis = (HORIZONTAL, VERTICAL)

        # Has- variables
        self.has_skin = TRUE
        self.has_movetag = TRUE

        # Type
        self.type = TYPE_NEUTRAL
        self.shoots = FALSE
        self.form = FORM_CIRCLE

        # Info
        self.radius = int()
        self.height = int()
        self.width = int()

        # Direction movement
        self.return_border = TRUE
        self.direction = LEFT

        # x and y, move and speed variables
        self.x_move = -3
        self.x_speed = 3
        self.y_move = 0
        self.y_speed = 0

        self.collision_with = (SHIP, ANY_BUBBLE)

        self.life_cost = 1

        self.id = int()

        self.coords_len = 2

        self.__active = False

    def create(self, x, y):
        from .components import StoppableThread
        if self.id <= 0:
            raise ValueError("The ID of the Sprite is not created with Game.canvas")
        self.__active = True
        # noinspection PyAttributeOutsideInit
        self.info = {"id": self.id,
                     "class": self}
        self._kw["sprites"]["byID"][self.info["id"]] = self.info
        self.thread3 = StoppableThread(None, lambda: self.move(), __name__ + ".Thread").start()

    def destroy(self):
        self.__active = False
        try:
            self.thread3.stop()
            self.thread2.stop()
        except AttributeError:
            pass
        del self._kw["sprites"]["byID"][self.info["id"]]

    def _on_move(self):

        # print("Has Movetag and Skin")
        if HORIZONTAL in self.axis:
            if self.direction == LEFT:
                self.x_move = -self.x_speed
            elif self.direction == RIGHT:
                self.x_move = self.x_speed
        if VERTICAL in self.axis:
            # print("Move Vertical")
            if self.direction == UP:
                self.y_move = -self.y_speed
            elif self.direction == DOWN:
                self.y_move = self.y_speed
        if self.return_border:
            pos = self._kw["canvas"].coords(self.id)
            # print(len(pos))
            if self.form == FORM_CIRCLE:
                h = self.radius
                w = self.radius
            elif self.form == FORM_RECT:
                h = self.height / 4
                w = self.width / 4
            else:
                return
            if len(pos) == 4:
                # print("return border check")
                if VERTICAL in self.axis:
                    if pos[3] >= self._kw["config"]["height"] - h:
                        self.direction = UP
                    if pos[1] <= h + 72:
                        self.direction = DOWN
                if HORIZONTAL in self.axis:
                    if pos[2] >= self._kw["config"]["width"] - w:
                        self.direction = LEFT
                    if pos[0] <= w:
                        self.direction = RIGHT
            if len(pos) == 2:
                if VERTICAL in self.axis:
                    if pos[1] >= self._kw["config"]["height"] - h:
                        self.direction = UP
                    if pos[1] <= h + 72:
                        self.direction = DOWN
                if HORIZONTAL in self.axis:
                    if pos[0] >= self._kw["config"]["width"] - w:
                        self.direction = LEFT
                    if pos[0] <= w:
                        self.direction = RIGHT
        self._kw["canvas"].move(self.id, self.x_move / self.fps / 2, self.y_move / self.fps / 2)

    def _hurt_player(self):
        self._kw["stats"]["lives"] -= self.life_cost

    def on_collide_bubble(self, index):
        pass

    def on_collide_ship(self, index):
        pass

    def on_collide_sprite(self, _class):
        pass

    def _on_collision(self):
        from . import extras
        from . import bubble

        from time import sleep

        if self.form == FORM_CIRCLE:
            h = self.radius
            w = self.radius
        elif self.form == FORM_RECT:
            h = self.height / 2
            w = self.width / 2
        else:
            return
        if self.form == FORM_CIRCLE:
            config = self._kw["config"]
            if SHIP in self.collision_with:
                distance = extras.distance(self._kw["canvas"], self._kw["log"], self.id, self._kw["ship"]["id"])
                if distance < (config["game"]["ship-radius"] + self.radius):
                    self.on_collide_ship(None)
                    self._hurt_player()
                    sleep(1)
            if ANY_BUBBLE in self.collision_with:
                for index in range(len(self._kw["bubbles"]["bub-id"]) - 1, -1, -1):
                    distance = extras.distance(self._kw["canvas"], self._kw["log"], self.id,
                                               self._kw["bubbles"]["bub-id"][index])
                    if distance < (self._kw["bubbles"]["bub-radius"][index] + self.radius):
                        self.on_collide_bubble(index)
                        bubble.del_bubble(index, self._kw["bubbles"], self._kw["canvas"])
        elif self.form == FORM_RECT:
            if SHIP in self.collision_with:
                pos = self._kw["canvas"].coords(self.id)
                paddle_pos = self._kw["canvas"].coords(self._kw["ship"]["id"])

                # print(pos, paddle_pos)
                if len(paddle_pos) == 2:
                    if len(pos) == 2:
                        if pos[0] + w >= paddle_pos[0] >= pos[0] - w:
                            if pos[1] + h >= paddle_pos[1] >= pos[1] - h:
                                self._hurt_player()
                    if len(pos) == 4:
                        # print("Domme fase 1")
                        if pos[2] + w >= paddle_pos[0] >= pos[0] - w:
                            # print("Domme fase 2")
                            if pos[3] + h >= paddle_pos[1] >= pos[1] - h:
                                # print("Domme fase 3")
                                self._hurt_player()
                                # print("Domme fase 4")
                elif len(paddle_pos) == 4:
                    if len(pos) == 2:
                        if pos[0] + w >= paddle_pos[0] and pos[0] <= paddle_pos[2] - w:
                            if pos[1] + h >= paddle_pos[1] and pos[1] <= paddle_pos[3] - h:
                                self._hurt_player()
                    if len(pos) == 4:
                        if pos[2] + w >= paddle_pos[0] and pos[0] <= paddle_pos[2] - w:
                            if pos[3] + h >= paddle_pos[1] and pos[1] <= paddle_pos[3] - h:
                                self._hurt_player()
            if ANY_BUBBLE in self.collision_with:
                for index in range(len(self._kw["bubbles"]["bub-id"]) - 2, -1, -1):
                    bub_h = bub_w = self._kw["bubbles"]["bub-radius"][index]
                    pos = self._kw["canvas"].coords(self.id)
                    print("[Index, len]: " + str([index, len(self._kw["bubbles"]["bub-id"])]))
                    paddle_pos = self._kw["canvas"].coords(self._kw["bubbles"]["bub-id"][index])
                    print(pos, paddle_pos)
                    if len(paddle_pos) == 2:
                        if len(pos) == 2:
                            if pos[0] + w >= paddle_pos[0] - bub_w and pos[0] - w <= paddle_pos[0] + bub_w:
                                if pos[1] + h >= paddle_pos[1] - bub_h and pos[1] - h <= paddle_pos[1] + bub_h:
                                    self.on_collide_bubble(index)
                                    bubble.del_bubble(index, self._kw["bubbles"], self._kw["canvas"])
                        if len(pos) == 4:
                            if pos[2] + w >= paddle_pos[0] - bub_w and pos[0] - w <= paddle_pos[0] + bub_w:
                                if pos[3] + h >= paddle_pos[1] - bub_h and pos[1] - h <= paddle_pos[1] + bub_h:
                                    self.on_collide_bubble(index)
                                    bubble.del_bubble(index, self._kw["bubbles"], self._kw["canvas"])
                    elif len(paddle_pos) == 4:
                        if len(pos) == 2:
                            if pos[0] + w >= paddle_pos[0] - bub_w and pos[0] <= paddle_pos[2] + bub_w:
                                if pos[1] + h >= paddle_pos[1] - bub_h and pos[1] <= paddle_pos[3] + bub_h:
                                    self.on_collide_bubble(index)
                                    bubble.del_bubble(index, self._kw["bubbles"], self._kw["canvas"])
                        if len(pos) == 4:
                            if pos[2] + w >= paddle_pos[0] - bub_w and pos[0] <= paddle_pos[2] + bub_w:
                                if pos[3] + h >= paddle_pos[1] - bub_h and pos[1] <= paddle_pos[3] + bub_h:
                                    self.on_collide_bubble(index)
                                    bubble.del_bubble(index, self._kw["bubbles"], self._kw["canvas"])

    def move(self):
        from time import time
        from .components import StoppableThread
        time2 = time()
        while self.__active:
            # print("\nhas movetag:", self.has_movetag, "| has skin:", self.has_skin); sleep(0.1)
            # print("\naxis:", self.axis); sleep(0.1)
            # print("\nreturn_border:", self.return_border); sleep(0.1)
            # print("\ndirection:", self.direction); sleep(0.1)
            # print("\nhave horizontal axis:", HORIZONTAL in self.axis); sleep(0.1)
            # print("\nhave vertical axis:", VERTICAL in self.axis); sleep(0.1)
            # print("\nx-speed:", self.x_speed); sleep(0.1)
            # print("\ny-speed:", self.y_speed); sleep(0.1)
            # print("\nx-motion:", self.x_move); sleep(0.1)
            # print("\ny-motion:", self.y_move); sleep(0.1)
            # print("\n\n\n")
            if self.has_movetag and self.has_skin:
                time1 = time()
                try:
                    self.fps = 1 / (time1 - time2)
                except ZeroDivisionError:
                    self.fps = 1
                time2 = time()
                self.thread2 = StoppableThread(None, lambda: self._on_move(), __name__ + ".Collision").start()
                self._on_collision()


# noinspection PyRedundantParentheses
class BaseBarier(Sprite):
    def __init__(self, **kw):
        from random import randint, choice
        self._kw = kw
        super().__init__(**kw)
        self.direction = choice([UP, DOWN])
        self.has_skin = TRUE
        self.has_movetag = TRUE
        self.axis = [VERTICAL]
        self.type = TYPE_DANGEROUS
        self.form = FORM_RECT
        self.direction = UP
        self.__speed = randint(80, 104)
        self.x_speed = 0
        self.y_speed = self.__speed
        self.x_move = 0
        self.y_move = self.__speed
        self.height = 100
        self.width = 10
        self.collision_with = [SHIP]

    def create(self, x, y):
        self.id = self._kw["canvas"].create_rectangle(x, y + 72, x + 10, y + 222, fill=RED, outline=RED)
        # print(self.parent.canvas.coords(self.id))
        super().create(x, 72 + y)


# noinspection PyMethodOverriding
class Bubble(Sprite):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.name = ""
        self.min = 9
        self.max = 60
        self.bubtype = BUB_NOSTATE
        self.hardness = 1
        self.images = dict()
        self.collision_with = []
        self.life_cost = 0
        self.form = FORM_CIRCLE
        self.coords_len = 2

    def pre_initialize(self):
        pass

    def create(self, x: int, y: int, r: int, s: int, **kw):
        r = max(min(r, self.min), self.max)
        self.ids = [self._kw["bubbles"]["canvas"].create_image(x, y, image=self.images[r * 2])]
        self.speed = s
        self._kw["bubbles"]["bubbles"]["bub-special"].append(False)
        self._kw["bubbles"]["bubbles"]["bub-index"].append(self)
        self._kw["bubbles"]["bubbles"]["bub-position"].append([x, y])
        self._kw["bubbles"]["bubbles"]["bub-hardness"].append(self.hardness)
        self._kw["bubbles"]["bubbles"]["bub-action"].append(self.name)
        self._kw["bubbles"]["bubbles"]["bub-id"].append(self.ids)
        self._kw["bubbles"]["bubbles"]["bub-radius"].append(r)
        self._kw["bubbles"]["bubbles"]["bub-speed"].append(s)
        self.index = self._kw["bubbles"]["bubbles"]["bub-id"].index(self.ids, 0, len(self._kw["bubbles"]["bubbles"]["bub-id"]))

    def on_move(self, parent: Game):
        pass

    def on_collision(self, parent: Game):
        from .bubble import del_bubble
        del_bubble(self.index, self._kw["bubbles"], self._kw["canvas"])

    def pop(self):
        pass


ActionIsNoneWarning = Warning


class StatusBubble(Bubble): 
    requires = tuple(list(Bubble.requires) + ["back"])

    def __init__(self, **kw):
        super().__init__(**kw)
        self._kw = kw
        self.name = None

    def on_collfunc(self):
        from .state import State
        if self.name is None:
            raise ActionIsNoneWarning("The name on status-bubble '%s' is None" % __name__)
        State.set_state(self._kw["canvas"], self._kw["log"], self._kw["stats"], self._kw["name"], self._kw["back"])


class Ammo(Sprite):
    requires = tuple(list(Sprite.requires) + ["ship", "ammo"])

    def __init__(self, **kw):
        super().__init__(**kw)
        self._kw = kw
        self.form = FORM_LINE
        self.return_border = FALSE
        self.direction = LEFT
        self.axis = [VERTICAL]
        self.x_speed = 60
        self.x_move = 60
        self.y_speed = 0
        self.y_move = 0
        self.height = 1
        self.width = 5

    def destroy(self):
        try:
            self.thread4.stop()
        except AttributeError:
            pass
        super().destroy()

    def on_collide_bubble(self, index):
        from tkinter import TclError
        from .components import StoppableThread
        from .bubble import del_bubble
        from .extras import replace_list, distance
        from .ammo import del_ammo

        log = self._kw["log"]
        ammo = self._kw["ammo"]
        root = self._kw["root"]
        texts = self._kw["texts"]
        stats = self._kw["stats"]
        canvas = self._kw["canvas"]
        panels = self._kw["panels"]
        bubble = self._kw["bubbles"]
        commands = self._kw["commands"]
        coll_func = self._kw["Coll"].coll_func
        ammo_index = self.id
        backgrounds = self._kw["back"]

        index_bub = index
        try:
            if distance(canvas, log, ammo["ammo-id"][ammo_index], bubble["bub-id"][index_bub][0]) < (
                    1 + bubble["bub-radius"][index_bub]):
                if bubble["bub-hardness"][index_bub] == 1:
                    try:
                        self.thread4 = StoppableThread(
                            None,
                            lambda: coll_func(index_bub, canvas, commands, root, log,
                                              stats,
                                              (bubble["bub-radius"][index_bub] +
                                               bubble["bub-speed"][index_bub]),
                                              bubble["bub-action"][index_bub], bubble,
                                              backgrounds,
                                              texts, panels, False),
                            __name__ + ".CollisionFunction").start()
                    except IndexError:
                        pass
                    del_bubble(index_bub, bubble, canvas)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                    # Thread(None, PlaySound("versions/"+self.launcher_cfg["versionDir"]+"/data/bubpop.wav", 1)).start()
                elif bubble["bub-hardness"][index_bub] > 1:
                    replace_list(bubble["bub-hardness"], index_bub, bubble["bub-hardness"][index_bub] - 1)
                    replace_list(ammo["ammo-damage"], ammo_index, ammo["ammo-damage"][ammo_index] + 1)
                    if ammo["ammo-damage"][ammo_index] > 4:
                        del_ammo(canvas, ammo_index, ammo)
                root.update()
        except TypeError:
            pass
        except IndexError:
            pass
        except AttributeError:
            self.destroy()
        except TclError:
            self.destroy()

    def create(self, x, y):
        id = self._kw["ship"]["id"]
        x, y = self._kw["canvas"].coords(id)

        self.id = self._kw["canvas"].create_line(x+7, y, x+12, y, fill="gold")
        self._kw["ammo"]["ammo-id"][self.id] = self.id
        self._kw["ammo"]["ammo-speed"][self.id] = 5
        self._kw["ammo"]["ammo-damage"][self.id] = 0
        super().create(x, y)
