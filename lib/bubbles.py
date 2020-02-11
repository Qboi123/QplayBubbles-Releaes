from .evals import score_eval
from .registry import get_value
from .sprites import Bubble, Player


class NormalBubble(Bubble):
    def __init__(self):
        from .player import Player

        super(NormalBubble, self).__init__()

        self.rarity: int = 30000

        self.health: float = 0.5

        self.collisionable: bool = True
        self.collisionWith: list = [Player]

        self.scoreMultiplier: float = 1
        self.speedMultiplier: float = 1
        self.attackMultiplier: float = 1
        self.defenceMultiplier: float = 1

        self.set_unlocalized_name("normal")

        # self.radius = seedint(get_stats("game")["seed"], xupd, 2, 15, 30)
        #
        # self.creationCoord = {'x': get_canvas().winfo_width()+(self.radius*2),
        #                       'y': seedint(get_stats("game")["seed"],
        #                                    xupd, 3, 72 + self.radius, (get_canvas().winfo_height() - self.radius))}
        #
        # self.speed = seedint(get_stats("game")["seed"], xupd, 1, ((xupd / 1000) * 5) * self.speedMultiplier, ((xupd / 1000) * 5) * self.speedMultiplier)
        #
        # self._image = createbubble_image(self.radius*2)
        #
        # self._id = get_canvas().create_image()
        # self.position = {'x': None, 'y': None}

    def on_collision(self, obj):
        if isinstance(obj, Player):
            obj.score += score_eval(get_value("Config", "ScoreEval"))
            
            
class DoubleBubble(Bubble):
    def __init__(self, xupd):
        from .player import Player
        
        super(DoubleBubble, self).__init__()

        self.rarity: int = 8000

        self.health: float = 1.00

        self.collisionable: bool = True
        self.collisionWith: list = [Player]

        self.scoreMultiplier: float = 2
        self.speedMultiplier: float = 1.5
        self.attackMultiplier: float = 1
        self.defenceMultiplier: float = 1.5

        self.set_unlocalized_name("double_value")

        # self.radius = seedint(get_stats("game")["seed"], xupd, 2, 15, 30)
        #
        # self.creationCoord = {'x': get_canvas().winfo_width()+(self.radius*2),
        #                       'y': seedint(get_stats("game")["seed"],
        #                                    xupd, 3, 72 + self.radius, (get_canvas().winfo_height() - self.radius))}
        #
        # self.speed = seedint(get_stats("game")["seed"], xupd, 1, ((xupd / 1000) * 5) * self.speedMultiplier, ((xupd / 1000) * 5) * self.speedMultiplier)
        #
        # self._image = createbubble_image(self.radius*2)
        #
        # self._id = get_canvas().create_image()
        # self.position = {'x': None, 'y': None}

    def on_collision(self, obj):
        if isinstance(obj, Player):
            obj.score += score_eval(get_value("Config", "ScoreEval"))
