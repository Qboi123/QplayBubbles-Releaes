from tkinter import Canvas as _Canvas
from typing import Dict as _Dict, Any as _Any, Optional as _Optional

NAME2EFFECT: _Dict[str, _Any] = {}
EFFECT2NAME: _Dict[_Any, str] = {}

CANVAS: _Optional[_Canvas] = None

MAX_BUBBLES = 100
