import sys
from typing import Callable

from utils import get_error_with_class_path, get_adv_error, print_adv_error, tkinter_adv_error, adv_excepthook, \
    tkinter_excepthook


class Event(object):
    _handlers = []

    def __init__(self, game):
        self.game = game

        for handler in Event._handlers:
            try:
                handler()
            except Exception as e:
                handler: Callable
                print(get_error_with_class_path(e, handler), sys.stderr)


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
