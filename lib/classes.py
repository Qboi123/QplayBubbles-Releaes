from .sprites import *
from .bubbles import *
from .events import *
from .status import *
from typing import *


SPRITES: List[Type[Sprite]] = []
BUBBLES: List[Bubble] = [NormalBubble()]
STATUSES: List[Type[Status]] = []
EVENTS: List[BaseEvent] = []