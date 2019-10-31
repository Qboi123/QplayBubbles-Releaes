from threadsafe_tkinter import *
from typing import *


class MouseController(object):
    def __init__(self, widget: Union[Widget, Tk, Canvas], tag_or_id=None):
        if tag_or_id is None:
            widget.bind("<ButtonPress>", self.set)
            widget.bind("<ButtonRelease>", self.set)
            widget.bind("<Motion>", self.set)
            widget.bind("<MouseWheel>", self.set)
            widget.bind("<Leave>", self.set)
        elif type(widget) == Canvas:
            widget.tag_bind(tag_or_id, "<ButtonPress>", self.set)
            widget.tag_bind(tag_or_id, "<ButtonRelease>", self.set)
            widget.tag_bind(tag_or_id, "<Motion>", self.set)
            widget.tag_bind(tag_or_id, "<MouseWheel>", self.set)
            widget.tag_bind(tag_or_id, "<Leave>", self.set)
        self._bEvt: Union[EventType.Motion, EventType.ButtonPress, EventType.ButtonRelease, EventType.MouseWheel] = None
        self._evt: Union[EventType.Motion, EventType.ButtonPress, EventType.ButtonRelease, EventType.MouseWheel, EventType.Leave] = None
        self.num = -1
        self.time = 0
        self.serial = 0
        self.state = -1
        self.delta = 0
        self.x = -1
        self.y = -1
        self.xRoot = -1
        self.yRoot = -1
        self.widget = widget

    def update(self):
        if self._evt is not None:
            if self._bEvt is not None:
                if (self._evt.time == self._bEvt.time) and ((self._evt.type == EventType.ButtonRelease) or
                                                            ((self._evt.type == EventType.MouseWheel) or (self._evt.type == EventType.Leave))):
                    self.num = -1
                    self.time = 0
                    self.serial = 0
                    self.state = -1
                    self.delta = 0
                    self.x = -1
                    self.y = -1
                    self.xRoot = -1
                    self.yRoot = -1
                else:
                    self.num = self._evt.num
                    self.time = self._evt.time
                    self.serial = self._evt.serial
                    self.state = self._evt.state
                    self.delta = self._evt.delta
                    self.x = self._evt.x
                    self.y = self._evt.y
                    self.xRoot = self._evt.x_root
                    self.yRoot = self._evt.y_root
                    self.widget = self._evt.widget
            else:
                self.num = self._evt.num
                self.time = self._evt.time
                self.serial = self._evt.serial
                self.state = self._evt.state
                self.delta = self._evt.delta
                self.x = self._evt.x
                self.y = self._evt.y
                self.xRoot = self._evt.x_root
                self.yRoot = self._evt.y_root
                self.widget = self._evt.widget
            self._bEvt = self._evt

    def set(self, evt: Union[EventType.Motion, EventType.ButtonPress, EventType.ButtonRelease, EventType.MouseWheel]):
        self._evt = evt
        print(evt.__dict__)


if __name__ == '__main__':
    pass


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
    a = MouseController(root)
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
        root.update_idletasks()
        sleep(0.01)
    # root.mainloop()
