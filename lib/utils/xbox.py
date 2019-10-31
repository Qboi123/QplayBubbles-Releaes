from inputs import get_gamepad, UnpluggedError
import threading

import math

class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self, widget):

        self.leftJoystickY = 0
        self.leftJoystickX = 0
        self.rightJoystickY = 0
        self.rightJoystickX = 0
        self.leftTrigger = 0
        self.rightTrigger = 0
        self.leftBumper = 0
        self.rightBumper = 0
        self.a = 0
        self.x = 0
        self.y = 0
        self.b = 0
        self.leftThumb = 0
        self.rightThumb = 0
        self.nack = 0
        self.start = 0
        self.leftDPad = 0
        self.rightDPad = 0
        self.upDPad = 0
        self.downDPad = 0
        self.widget = widget

        # self._monitor_thread = threading.Thread(target=self.update, args=())
        # self._monitor_thread.daemon = True
        # self._monitor_thread.start()


    # def read(self):
    #     x = self.leftJoystickX
    #     y = self.leftJoystickY
    #     a = self.a
    #     b = self.b # b=1, x=2
    #     rb = self.rightBumper
    #     return [x, y, a, b, rb]


    def _event(self, event):
        if event.code == 'ABS_Y':
            self.leftJoystickY = int(event.state / XboxController.MAX_JOY_VAL * 10)  # normalize between -1 and 1
        elif event.code == 'ABS_X':
            self.leftJoystickX = int(event.state / XboxController.MAX_JOY_VAL * 10)  # normalize between -1 and 1
        elif event.code == 'ABS_RY':
            self.rightJoystickY = int(event.state / XboxController.MAX_JOY_VAL * 10)  # normalize between -1 and 1
        elif event.code == 'ABS_RX':
            self.rightJoystickX = int(event.state / XboxController.MAX_JOY_VAL * 10)  # normalize between -1 and 1
        elif event.code == 'ABS_Z':
            self.leftTrigger = int(event.state / XboxController.MAX_TRIG_VAL * 10)  # normalize between 0 and 1
        elif event.code == 'ABS_RZ':
            self.rightTrigger = int(event.state / XboxController.MAX_TRIG_VAL * 10)  # normalize between 0 and 1
        elif event.code == 'BTN_TL':
            self.leftBumper = event.state
        elif event.code == 'BTN_TR':
            self.rightBumper = event.state
        elif event.code == 'BTN_SOUTH':
            self.a = event.state
        elif event.code == 'BTN_NORTH':
            self.x = event.state
        elif event.code == 'BTN_WEST':
            self.y = event.state
        elif event.code == 'BTN_EAST':
            self.b = event.state
        elif event.code == 'BTN_THUMBL':
            self.leftThumb = event.state
        elif event.code == 'BTN_THUMBR':
            self.rightThumb = event.state
        elif event.code == 'BTN_SELECT':
            self.back = event.state
        elif event.code == 'BTN_START':
            self.start = event.state
        elif event.code == 'BTN_TRIGGER_HAPPY1':
            self.leftDPad = event.state
        elif event.code == 'BTN_TRIGGER_HAPPY2':
            self.rightDPad = event.state
        elif event.code == 'BTN_TRIGGER_HAPPY3':
            self.upDPad = event.state
        elif event.code == 'BTN_TRIGGER_HAPPY4':
            self.downDPad = event.state
        elif event.code == "ABS_HAT0X":
            if event.state == -1:
                self.leftDPad = 1
            elif event.state == 0:
                self.leftDPad = 0
                self.rightDPad = 0
            elif event.state == 1:
                self.rightDPad = 1
        elif event.code == "ABS_HAT0Y":
            if event.state == -1:
                self.upDPad = 1
            elif event.state == 0:
                self.upDPad = 0
                self.downDPad = 0
            elif event.state == 1:
                self.downDPad = 1
        elif event.code == "SYN_REPORT":
            pass
        else:
            from sys import stderr
            print("[XboxContoller]: Invalid input: %s" % event.code, file=stderr)
        # print(event.__dict__)

    def update(self):
        try:
            events = get_gamepad()
        except UnpluggedError:
            return
        for event in events:
            self._event(event)

if __name__ == '__main__':
    def update():
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
    from threadsafe_tkinter import *

    root = Tk()
    a = XboxController(root)
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
    root.update()
    while 1:
        Thread(None, lambda: a.update()).start()
        Thread(None, lambda: update()).start()
        root.update_idletasks()
        root.update()
    # root.mainloop()
