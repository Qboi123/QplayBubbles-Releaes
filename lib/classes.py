from .sprites import *
from .bubbles import *
from .events import *
from .status import *
from typing import *


SPRITES: List[Type[Sprite]] = [Bubble]
BUBBLES: List[Type[Bubble]] = [NormalBubble]
STATUSES: List[Type[Status]] = []
EVENTS: List[BaseEvent] = []