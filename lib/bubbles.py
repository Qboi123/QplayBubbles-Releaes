from .evals import score_eval, minspeed_eval, maxspeed_eval
from .registry import get_value
from .sprites import Bubble
from .sprites import Player


class NormalBubble(Bubble):
    # Define Bubble ID and Prefix
    bubble_id: str = "normal"
    bubble_prefix: str = "qplay"

    def __init__(self, xupd):
        from .utils import createbubble_image, seedint
        from .stats import get_stats
        from .utils.get_set import get_canvas
        from .player import Player

        Bubble.__init__(self)

        self.rarity: int = 30000

        self.health: float = 0.5

        self.collisionable: bool = True
        self.collisionWith: list = [Player]

        self.scoreMultiplier: float = 1
        self.speedMultiplier: float = 1
        self.attackMultiplier: float = 1
        self.defenceMultiplier: float = 1

        self.radius = seedint(get_stats("game")["seed"], xupd, 2, 15, 30)

        self.creationCoord = {'x': get_canvas().winfo_width()+(self.radius*2),
                              'y': seedint(get_stats("game")["seed"],
                                           xupd, 3, 72 + self.radius, (get_canvas().winfo_height() - self.radius))}

        self.speed = seedint(get_stats("game")["seed"], xupd, 1, ((xupd / 1000) * 5) * self.speedMultiplier, ((xupd / 1000) * 5) * self.speedMultiplier)

        self._image = createbubble_image(self.radius*2)

        self._id = get_canvas().create_image()
        self.position = {'x': None, 'y': None}

    def on_collision(self, obj):
        if isinstance(obj, Player):
            obj.score += score_eval(get_value("Config", "ScoreEval"))
            
            
class DoubleBubble(Bubble):
    bubble_id: str = "double"
    bubble_prefix: str = "qplay"
    
    def __init__(self, xupd):
        from .utils import createbubble_image, seedint
        from .stats import get_stats
        from .utils.get_set import get_canvas
        from .player import Player
        
        Bubble.__init__(self)

        self.rarity: int = 8000

        self.health: float = 1.00

        self.collisionable: bool = True
        self.collisionWith: list = [Player]

        self.scoreMultiplier: float = 2
        self.speedMultiplier: float = 1.5
        self.attackMultiplier: float = 1
        self.defenceMultiplier: float = 1.5

        self.radius = seedint(get_stats("game")["seed"], xupd, 2, 15, 30)

        self.creationCoord = {'x': get_canvas().winfo_width()+(self.radius*2),
                              'y': seedint(get_stats("game")["seed"],
                                           xupd, 3, 72 + self.radius, (get_canvas().winfo_height() - self.radius))}

        self.speed = seedint(get_stats("game")["seed"], xupd, 1, ((xupd / 1000) * 5) * self.speedMultiplier, ((xupd / 1000) * 5) * self.speedMultiplier)

        self._image = createbubble_image(self.radius*2)

        self._id = get_canvas().create_image()
        self.position = {'x': None, 'y': None}

    def on_collision(self, obj):
        if isinstance(obj, Player):
            obj.score += score_eval(get_value("Config", "ScoreEval"))
