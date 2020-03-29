import sys
from tkinter import Canvas
from typing import Callable

from lib.xbox import XboxController
from registry import Registry
from scenemanager import Scene, SceneManager
from utils import get_error_with_class_path, get_adv_error, print_adv_error, tkinter_adv_error, adv_excepthook, \
    tkinter_excepthook


class Event(object):
    _handlers = list()

    def __init__(self, scene):
        self.frame = scene.frame
        # self.audio = scene.audio
        self.scene = scene

        for handler in self._handlers:
            handler(self)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class ExperienceEvent(Event):
    _handlers = list()

    def __init__(self, scene, experience):
        self.experience = experience

        super(ExperienceEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class ResizeEvent(Event):
    _handlers = list()

    def __init__(self, scene, width, height):
        self.width = width
        self.height = height

        super(ResizeEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class SavedataReadedEvent(Event):
    _handlers = list()

    def __init__(self, data):
        super(Event, self).__init__()

        for handler in self._handlers:
            handler(data)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UpdatableEvent(Event):
    _handlers = list()
    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyMethodOverriding
class CanvasIDEvent(Event):
    _handlers = dict()
    event = ""

    def __init__(self, scene):
        super(CanvasIDEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene)

    @classmethod
    def bind(cls, func, id: int, canvas: Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


class MouseEnterEvent(CanvasIDEvent):
    _handlers = dict()
    event = "<Enter>"

    def __init__(self, scene, x, y):
        self.x = x
        self.y = y
        super(MouseEnterEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene, event.x, event.y)

    @classmethod
    def bind(cls, func, id: int, canvas: Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


# noinspection PyMethodOverriding
class MouseLeaveEvent(CanvasIDEvent):
    _handlers = dict()
    event = "<Leave>"

    def __init__(self, scene, x, y):
        self.x = x
        self.y = y
        super(MouseLeaveEvent, self).__init__(scene)

    @classmethod
    def _call(cls, scene, event):
        cls(scene, event.x, event.y)

    @classmethod
    def bind(cls, func, id: int, canvas: Canvas, scene):
        cls._handlers[func] = canvas.tag_bind(id, cls.event, lambda event: cls._call(scene, event))
        # print(func)
        return func

    @classmethod
    def unbind(cls, func, id, canvas: Canvas, scene):
        canvas.tag_unbind(id, cls.event, cls._handlers[func])
        del cls._handlers[func]
        # print(f"Unbind: {func.__name__}")
        return func


class KeyPressEvent(Event):
    _handlers = list()

    def __init__(self, scene, tkevent):
        self.keySym = tkevent.keysym
        self.char = tkevent.char

        super(KeyPressEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class KeyReleaseEvent(Event):
    _handlers = list()

    def __init__(self, scene, tkevent):
        self.keySym = tkevent.keysym
        self.char = tkevent.char

        super(KeyReleaseEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class UpdateEvent(Event):
    _handlers = list()

    def __init__(self, scene: Scene, dt: float, canvas: Canvas):
        self.dt: float = dt
        self.canvas: Canvas = canvas

        super(UpdateEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: Callable):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: Callable):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class CollisionEvent(Event):
    _handlers = list()

    def __init__(self, scene: Scene, eventobj, collidedobj, canvas: Canvas):
        self.eventObject = eventobj
        self.collidedObj = collidedobj
        self.canvas: Canvas = canvas

        super(CollisionEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func: Callable):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func: Callable):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


class XInputEvent(UpdatableEvent):
    _handlers = list()
    xboxController = XboxController()
    _A = None
    _B = None
    _X = None
    _Y = None
    _LB = None
    _RB = None
    _LTR = None
    _RTR = None
    _LTH = None
    _RTH = None
    _LJOY = None
    _RJOY = None
    _START = None
    _SELEC = None

    # noinspection PyMissingConstructor
    def __init__(self, scene):
        """
        Triggers to update xinput values, and call event handlers on parent class

        :param scene:
        """

        self.eventype = "button"
        if self._A != XInputEvent.xboxController.A:
            self.event = "A"
            self.value = XInputEvent.xboxController.A
            super(UpdatableEvent, self).__init__(scene)
        if self._B != XInputEvent.xboxController.B:
            self.event = "B"
            self.value = XInputEvent.xboxController.B
            super(UpdatableEvent, self).__init__(scene)
        if self._X != XInputEvent.xboxController.X:
            self.event = "X"
            self.value = XInputEvent.xboxController.X
            super(UpdatableEvent, self).__init__(scene)
        if self._Y != XInputEvent.xboxController.Y:
            self.event = "Y"
            self.value = XInputEvent.xboxController.Y
            super(UpdatableEvent, self).__init__(scene)
        if self._LB != XInputEvent.xboxController.LeftBumper:
            self.event = "LBUMPER"
            self.value = XInputEvent.xboxController.LeftBumper
            super(UpdatableEvent, self).__init__(scene)
        if self._RB != XInputEvent.xboxController.RightBumper:
            self.event = "RBUMPER"
            self.value = XInputEvent.xboxController.RightBumper
            super(UpdatableEvent, self).__init__(scene)
        if self._LTH != XInputEvent.xboxController.LeftThumb:
            self.event = "LTHUMB"
            self.value = XInputEvent.xboxController.LeftThumb
            super(UpdatableEvent, self).__init__(scene)
        if self._RTH != XInputEvent.xboxController.RightThumb:
            self.event = "RTHUMB"
            self.value = XInputEvent.xboxController.RightThumb
            super(UpdatableEvent, self).__init__(scene)

        self.eventype = "trigger"
        if self._LTR != XInputEvent.xboxController.LeftTrigger:
            self.event = "LTRIGGER"
            self.value = XInputEvent.xboxController.LeftTrigger
            super(UpdatableEvent, self).__init__(scene)
        if self._RTR != XInputEvent.xboxController.RightTrigger:
            self.event = "RTRIGGER"
            self.value = XInputEvent.xboxController.RightTrigger
            super(UpdatableEvent, self).__init__(scene)

        self.eventype = "joystick"
        x = XInputEvent.xboxController
        if self._LJOY != (x.LeftJoystickX, x.LeftJoystickY):
            self.event = "LJOYSTICK"
            self.value = (x.LeftJoystickX, x.LeftJoystickY)
            super(UpdatableEvent, self).__init__(scene)
        if self._RJOY != (x.RightJoystickX, x.RightJoystickY):
            self.event = "RJOYSTICK"
            self.value = (x.RightJoystickX, x.RightJoystickY)
            super(UpdatableEvent, self).__init__(scene)

    @classmethod
    def bind(cls, func):
        cls._handlers.append(func)
        # print(func)
        return func

    @classmethod
    def unbind(cls, func):
        cls._handlers.remove(func)
        # print(f"Unbind: {func.__name__}")
        return func


def error(c):
    return int(c)


class Error(object):
    def __init__(self, var):
        self.var = var
        # print(dir(self.return_int))
        # print(dir(self.return_int.__func__))
        # print(self.return_int.__func__.__name__)
        # print(self.return_int.__class__.__name__)
        # print(self.return_int.__qualname__)

    def return_int(self):
        return int(self.var)


class Error2(Error):
    def __init__(self, var):
        super().__init__(var)

        self.number = int(var)


if __name__ == '__main__':
    a = "984jfjjjfjj"
    try:
        b = error(a)
    except Exception as e:
        print(get_error_with_class_path(e, error), file=sys.stderr)

    try:
        b = Error(a).return_int()
    except Exception as e:
        print(get_error_with_class_path(e, Error(a).return_int), file=sys.stderr)

    try:
        b = Error2(a)
    except Exception as e:
        print(get_error_with_class_path(e, Error2), file=sys.stderr)

    try:
        b = int(a)
    except Exception as e:
        print(get_error_with_class_path(e, int), file=sys.stderr)

    c = lambda a_=a: int(a_)
    try:
        b = c()
    except Exception as e:
        print(get_error_with_class_path(e, c), file=sys.stderr)

    a = "984jfjjjfjj"
    try:
        b = error(a)
    except Exception as e:
        print_adv_error(e, error)

    try:
        b = Error(a).return_int()
    except Exception as e:
        print_adv_error(e, Error(a).return_int)

    try:
        b = Error2(a)
    except Exception as e:
        print_adv_error(e, Error2)

    try:
        b = int(a)
    except Exception as e:
        print_adv_error(e, int)

    c = lambda a_=a: int(a_)
    try:
        b = c()
    except Exception as e:
        print_adv_error(e, c)

    c = lambda a_=a: int(a_)
    try:
        b = c()
    except Exception as e:
        tkinter_adv_error(e, c)

    sys.excepthook = adv_excepthook

    c = lambda a_=a: int(a_)
    b = c()

    sys.excepthook = tkinter_excepthook

    c = lambda a_=a: int(a_)
    b = c()
