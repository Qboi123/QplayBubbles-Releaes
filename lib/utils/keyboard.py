from threadsafe_tkinter import *
from typing import *


class KeyBoardController(object):
    def __init__(self, widget: Union[Widget, Tk] = None):
        try:
            from .get_set import get_root
        except ModuleNotFoundError:
            from get_set import get_root
        if widget is None:
            widget = get_root()
        widget.bind("<KeyPress>", self.set)
        widget.bind("<KeyRelease>", self.set)
        self._bEvt: Union[EventType.KeyPress, EventType.KeyRelease] = None
        self.char = ""
        self.keyCode = 0
        self.keySym = ""
        self.keySymNum = 0
        self.num = 0
        self.serial = 0
        self.state = -1
        self.time = 0
        self.type = ""
        self.widget = widget

    def update(self):
        if hasattr(self, "_evt"):
            if self._bEvt is not None:
                if (self._evt.time == self._bEvt.time) and (self._evt.type == EventType.KeyRelease):
                    self.char = ""
                    self.keyCode = 0
                    self.keySym = ""
                    self.keySymNum = 0
                    self.num = 0
                    self.serial = 0
                    self.state = -1
                    self.time = 0
                    self.type = ""
                else:
                    self.char = self._evt.char
                    self.keyCode = self._evt.keycode
                    self.keySym = self._evt.keysym
                    self.keySymNum = self._evt.keysym_num
                    self.num = self._evt.num
                    self.serial = self._evt.serial
                    self.state = self._evt.state
                    self.time = self._evt.time
                    self.type = self._evt.type
                    self.widget = self._evt.widget
            else:
                self.char = self._evt.char
                self.keyCode = self._evt.keycode
                self.keySym = self._evt.keysym
                self.keySymNum = self._evt.keysym_num
                self.num = self._evt.num
                self.serial = self._evt.serial
                self.state = self._evt.state
                self.time = self._evt.time
                self.type = self._evt.type
                self.widget = self._evt.widget
            self._bEvt = self._evt

    def set(self, evt: Union[EventType.KeyPress, EventType.KeyRelease]):
        self._evt = evt
        print(dir(evt))
        print("Char: %s" % evt.char)
        print("Delta: %s" % evt.delta)
        print("Height: %s" % evt.height)
        print("Keycode: %s" % evt.keycode)
        print("Keysym: %s" % evt.keysym)
        print("Keysym Num: %s" % evt.keysym_num)
        print("Num: %s" % evt.num)
        print("Serial: %s" % evt.serial)
        print("State: %s" % evt.state)
        print("Time: %s" % evt.time)
        print("Type: %s" % evt.type)
        print("Widget: %s" % evt.widget)
        print("Width: %s" % evt.width)
        print("X: %s" % evt.x)
        print("X Root: %s" % evt.x_root)
        print("Y: %s" % evt.y)
        print("Y Root: %s" % evt.y_root)


if __name__ == '__main__':
    def update():
        a.update()
        b = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
             '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
             '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
             '__str__', '__subclasshook__', '__weakref__']
        c = a.__dict__.copy()
        for d in b:
            if d in c.keys():
                c.pop(d)
        label.config(text=str(c))

    from threading import Thread
    from time import sleep

    root = Tk()
    a = KeyBoardController(root)
    b = ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
         '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__',
         '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__',
         '__str__', '__subclasshook__', '__weakref__']
    c = a.__dict__.copy()
    for d in b:
        if d in c.keys():
            c.pop(d)
    label = Label(root, text=str(c))
    label.pack()
    while 1:
        Thread(None, update()).start()
        root.update()
        sleep(0.01)
    root.mainloop()
