from .utils.xbox import XboxController
from .utils.keyboard import KeyBoardController
from .utils.mouse import MouseController
from threadsafe_tkinter import *
from typing import *

from .window import RootWindow


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


# class CollisionEvent(BaseEvent):
#     def __init__(self, sprite1, sprite2):
#         BaseEvent.__init__(self)
#         # sprite1


class EventHandler(object):
    _handlers = []

    def __init__(self, game, canvas):
        self.window: RootWindow = game.window
        self.registry = game.window.registry
        self.canvas = canvas

        for handler in self._handlers:
            handler(self)


class BubbleCreateEvent(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, bubbleobject):
        self.bubbleObject = bubbleobject
        super(BubbleCreateEvent, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class BubbleRemoveEvent(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, bubbleobject):
        self.bubbleObject = bubbleobject
        super(BubbleRemoveEvent, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class CollisionEvent(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, event_obj, other_obj):
        self.eventObj = event_obj
        self.otherObj = other_obj
        super(CollisionEvent, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class UpdateEvent(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, dt):
        self.dt = dt
        super(UpdateEvent, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class KeyboardEventHandler(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, event: KeyBoardEvent):
        self.event = event

        # Symbol and key
        self.char = self.event.char
        self.keySym = self.event.keySym
        self.keyCode = self.event.keyCode
        self.keyState = self.event.state
        self.keySymNum = self.event.keySymNum

        # Type and time
        self.type = self.event.type
        self.time = self.event.time

        # Others
        self.number = self.event.num
        self.serial = self.event.serial
        self.widget = self.event.widget
        super(KeyboardEventHandler, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class MouseEventHandler(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, event: MouseEvent):
        self.event = event

        # Position
        self.x = self.event.x
        self.y = self.event.y
        self.xRoot = self.event.xRoot
        self.yRoot = self.event.yRoot

        # Delta and state
        self.scrolldelta = self.event.delta
        self.mouseState = self.event.state

        # Other
        self.number = self.event.num
        self.serial = self.event.serial
        self.widget = self.event.widget
        super(MouseEventHandler, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)


class ControllerEventHandler(EventHandler):
    _handlers = []

    def __init__(self, game, canvas, event: ControllerEvent):
        self.event = event

        # Buttons right
        self.btnX = self.event.x
        self.btnY = self.event.y
        self.btnA = self.event.a
        self.btnB = self.event.b

        # Buttons middle
        self.start = self.event.start
        self.back = self.event.back

        # Buttons left
        self.downDPad = self.event.downDPad
        self.upDPad = self.event.upDPad
        self.leftDPad = self.event.leftDPad
        self.rightDPad = self.event.rightDPad

        # Yoystick left
        self.leftYoystickX = self.event.leftJoystickX
        self.leftYoystickY = self.event.leftJoystickY

        # Yoystick right
        self.rightYoystickX = self.event.rightJoystickX
        self.rightYoystickY = self.event.rightJoystickY

        # Bumper and thumb left
        self.leftBumper = self.event.leftBumper
        self.leftThumb = self.event.leftThumb

        # Bumper and thumb left
        self.rightBumper = self.event.rightBumper
        self.rightThumb = self.event.rightThumb

        super(ControllerEventHandler, self).__init__(game, canvas)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
