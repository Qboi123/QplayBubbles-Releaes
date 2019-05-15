from .fake_main import Game

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
TYPE_DANGEROUS = "dangerous"
TYPE_NEUTRAL = "neutral"
FORM_CIRCLE = "circle"
FORM_RECT = "rectangle"
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
    def __init__(self, parent: Game):
        self.parent = parent

    def on_update(self, parent: Game):
        pass

    def on_t_update(self, parent: Game):
        pass
    

class Bubble:
    def __init__(self, parent: Game):
        self.name = ""
        self.parent = parent
        self.min = 9
        self.max = 60
        self.hardness = 1
        self.images = dict()

    def pre_initialize(self):
        pass
        
    def create(self, parent: Game, x: int, y: int, r: int, s: int):
        r = max(min(r, self.min), self.max)
        self.ids = [parent.create_image(x, y, image=self.images[r * 2])]
        self.speed = s
        parent.bubbles["bub-special"].append(False)
        parent.bubbles["bub-index"].append(self)
        parent.bubbles["bub-position"].append([x, y])
        parent.bubbles["bub-hardness"].append(self.hardness)
        parent.bubbles["bub-action"].append(self.name)
        parent.bubbles["bub-id"].append(self.ids)
        parent.bubbles["bub-radius"].append(r)
        parent.bubbles["bub-speed"].append(s)
        index = parent.bubbles["bub-id"].index(self.ids, 0, len(parent.bubbles["bub-id"]))
    
    def on_move(self, parent: Game):
        parent.move()
    
    def on_collision(self, parent: Game):
        pass
    
    def pop(self, parent: Game):
        pass
    
    
class StatusBubbles(Bubble):
    def __init__(self, parent: Game):
        super().__init__(parent)
        
    def status_event(self, parent: Game):
        pass


DirectionWaring = Warning


class Sprite:
    def __init__(self, parent: Game):
        name = "EmptySprite"
        self.parent = parent

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

        self.__active = False

    def create(self, x, y):
        from threading import Thread
        if self.id <= 0:
            raise ValueError("The ID of the Sprite is not created with Game.canvas")
        self.__active = True
        self.info = {"id": self.id,
                "class": self}
        self.parent.sprites["byID"][self.info["id"]] = self.info
        Thread(None, lambda: self.move()).start()

    def destroy(self):
        self.__active = False
        del self.parent.sprites["byID"][self.info["id"]]

    def _on_move(self):
        pass

    def _hurt_player(self):
        self.parent.stats["lives"] -= self.life_cost

    def _on_collision(self):
        from . import extras
        from . import bubble
        
        from time import sleep
        if self.form == FORM_CIRCLE:
            config = self.parent.config
            if SHIP in self.collision_with:    
                distance = extras.distance(self.parent.canvas, self.parent.log, self.id, self.parent.ship["id"])
                if distance < (config["game"]["ship-radius"] + self.radius):
                    self._hurt_player()
                    sleep(1)
            if ANY_BUBBLE in self.collision_with:
                for index in range(len(self.parent.bubbles["bub-id"])-1, -1, -1):
                    distance = extras.distance(self.parent.canvas, self.parent.log, self.id, 
                                               self.parent.bubbles["bub-id"][index])
                    if distance < (self.parent.bubbles["bub-radius"][index] + self.radius):
                        bubble.del_bubble(index, self.parent.bubbles, self.parent.canvas)
        elif self.form == FORM_RECT:
            if SHIP in self.collision_with:
                pos = self.parent.canvas.coords(self.id)
                paddle_pos = self.parent.canvas.coords(self.parent.ship["id"])
                print(pos, paddle_pos)
                if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                    if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                        self._hurt_player()
                        sleep(1)
            if ANY_BUBBLE in self.collision_with:
                for index in range(len(self.parent.bubbles["bub-id"])-1, -1, -1):
                    pos = self.parent.canvas.coords(self.id)
                    paddle_pos = self.parent.canvas.coords(self.parent.bubbles["bub-id"][index])
                    print(pos, paddle_pos)
                    if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                        if pos[3] >= paddle_pos[1] and pos[1] <= paddle_pos[3]:
                            bubble.del_bubble(index, self.parent.bubbles, self.parent.canvas)

    def move(self):
        while self.__active:
            if self.has_movetag and self.has_skin:
                if HORIZONTAL in self.axis:
                    if self.direction == LEFT:
                        self.x_move = -self.x_speed
                    elif self.direction == RIGHT:
                        self.x_move = self.x_speed
                if VERTICAL in self.axis:
                    if self.direction == UP:
                        self.y_move = -self.y_speed
                    elif self.direction == DOWN:
                        self.y_move = self.y_speed
                if self.return_border:
                    pos = self.parent.canvas.coords(self.id)
                    print(len(pos))
                    if len(pos) == 4:
                        if VERTICAL in self.axis:
                            if pos[3] >= self.parent.config["height"]:
                                self.direction = UP
                            if pos[1] <= 0:
                                self.direction = DOWN
                        if HORIZONTAL in self.axis:
                            if pos[2] >= self.parent.config["width"]:
                                self.direction = LEFT
                            if pos[0] <= 0:
                                self.direction = RIGHT
                    if len(pos) == 2:
                        if VERTICAL in self.axis:
                            if pos[1] >= self.parent.config["height"]:
                                self.direction = UP
                            if pos[1] <= 0:
                                self.direction = DOWN
                        if HORIZONTAL in self.axis:
                            if pos[0] >= self.parent.config["width"]:
                                self.direction = LEFT
                            if pos[0] <= 0:
                                self.direction = RIGHT

                self.parent.move(self.id, self.x_move, self.y_move)
            self._on_collision()
            self._on_move()


# noinspection PyRedundantParentheses
class BaseBarier(Sprite):
    def __init__(self, parent: Game):
        super().__init__(parent)
        self.axis = (VERTICAL)
        self.type = TYPE_DANGEROUS
        self.form = FORM_RECT
        
    def create(self, x, y):
        self.id = self.parent.create_rectangle(x, y, x+10, x+100, fill=RED, outline=RED)
        super().create(x, 72+y)
