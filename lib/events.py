from .utils.xbox import XboxController
from .utils.keyboard import KeyBoardController
from .utils.mouse import MouseController
from threadsafe_tkinter import *
from typing import *


class BaseEvent:
    def __init__(self):
        self.event_id = "base"
        self.event_prefix = "qplay"

        self.tickPerUpdate: int = 1

    def update(self):
        pass


class ControllerEvent(BaseEvent, XboxController):
    def __init__(self, parent, widget: Union[Widget, Tk]):
        BaseEvent.__init__(self)
        XboxController.__init__(self)

        self.widget=widget
        self._parent = parent
        self.tickPerUpdate = 0.1

    def update(self):
        print(self.widget.focus_get())

        if self.widget.focus_get():
            XboxController.update(self)
            self._parent(self)


class KeyBoardEvent(BaseEvent, KeyBoardController):
    def __init__(self, parent, widget: Union[Widget, Tk] = None):
        BaseEvent.__init__(self)
        KeyBoardController.__init__(self, widget)

        self._parent = parent
        self.tickPerUpdate = 0.1

    def update(self):
        KeyBoardController.update(self)
        self._parent(self)


class MouseEvent(BaseEvent, MouseController):
    def __init__(self, parent, widget: Union[Widget, Tk, Canvas] = None):
        BaseEvent.__init__(self)
        MouseController.__init__(self, widget)

        self._parent = parent
        self.tickPerUpdate = 0.1

    def update(self):
        MouseController.update(self)
        self._parent(self)


class CollisionEvent(BaseEvent):
    def __init__(self, sprite1, sprite2):
        BaseEvent.__init__(self)
        # sprite1
