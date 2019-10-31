from .evals import score_eval, minspeed_eval, maxspeed_eval
from .registry import get_value
from .sprites import Bubble


class NormalBubble(Bubble):
    # Define Bubble ID and Prefix
    bubble_id: str = "normal"
    bubble_prefix: str = "qplay"

    def __init__(self, xupd):
        from .utils import createbubble_image, seedint
        from .stats import get_stat
        from .utils.get_set import get_canvas
        from .player import Player

        Bubble.__init__(self)

        self.bubble_id = "normal"
        self.bubble_prefix = "qplay"

        self.health = 0.5

        self.collisionable = True
        self.collisionWith = [Player]

        self.scoreMultiplier = 1
        self.speedMultiplier = 1
        self.attackMultiplier = 1
        self.defenceMultiplier = 1

        self.radius = seedint(get_stat("game")["seed"], xupd, 2, 15, 30)

        self.creationCoord = {'x': get_canvas().winfo_width()+(self.radius*2),
                              'y': seedint(get_stat("game")["seed"],
                                          xupd, 3, 72 + self.radius, (get_canvas().winfo_height() - self.radius))}

        self.speed = seedint(get_stat("game")["seed"], xupd, 1, ((xupd / 1000) * 5) * self.speedMultiplier, ((xupd/1000) * 5) * self.speedMultiplier)

        self._image = createbubble_image(self.radius*2)

        self._id = get_canvas().create_image()
        self.position = {'x': None, 'y': None}

    def on_collision(self, obj):
        if isinstance(obj, Player):
            obj.score += score_eval(get_value("Config", "ScoreEval"))
