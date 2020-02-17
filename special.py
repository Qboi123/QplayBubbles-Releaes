import tkinter as tk

from tkinter import *


class CustomScrollbar(tk.Canvas):
    def __init__(self, parent, **kwargs):
        self.command = kwargs.pop("command", None)
        tk.Canvas.__init__(self, parent, **kwargs)
        if "fg" not in kwargs.keys():
            kwargs["fg"] = "darkgray"

        # coordinates are irrelevant; they will be recomputed
        # in the 'set' method\
        self.old_y = 0
        self.create_rectangle(0, 0, 1, 1, fill=kwargs["fg"], outline=kwargs["fg"], tags=("thumb",))
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)

    def redraw(self, event):
        # The command is presumably the `yview` method of a widget.
        # When called without any arguments it will return fractions
        # which we can pass to the `set` command.
        self.set(*self.command())

    def set(self, first, last):
        first = float(first)
        last = float(last)
        height = self.winfo_height()
        x0 = 2
        x1 = self.winfo_width() - 2
        y0 = max(int(height * first), 0)
        y1 = min(int(height * last), height)
        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

        self.coords("thumb", x0, y0, x1, y1)

    def on_press(self, event):
        self.bind("<Motion>", self.on_click)
        self.pressed_y = event.y
        self.on_click(event)

    def on_release(self, event):
        self.unbind("<Motion>")

    def on_click(self, event):
        y = event.y / self.winfo_height()
        y0 = self._y0
        y1 = self._y1
        # print(y0, y1)
        # print(y1-y0)
        # print((y1-y0)/2)
        a = y + ((y1 - y0) / -(self.winfo_height() * 2))
        # print(((y1-y0)/2)*y/100)
        self.command("moveto", a)


class ScrolledWindow(tk.Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """

    def __init__(self, parent, canv_w=400, canv_h=400, expand=False, fill=None, height=None, width=None, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars

        if width is None:
            __width = 0
        else:
            __width = width

        if height is None:
            __height = 0
        else:
            __height = width

        self.canv = Canvas(self.parent, bg='#FFFFFF', width=canv_w, height=canv_h,
                           scrollregion=(0, 0, __width, __height), highlightthickness=0)
        # self.hbar = Scrollbar(self.parent, orient=HORIZONTAL)
        # self.hbar.pack(side=BOTTOM, fill=X)
        # self.hbar.config(command=self.canv.xview)
        self.vbar = Scrollbar(self.parent, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canv.yview)
        self.canv.config(  # xscrollcommand=self.hbar.set,
                         yscrollcommand=self.vbar.set)
        self.canv.pack(side=LEFT, fill=fill, expand=expand)
        # creating a canvas
        # self.canv = tk.Canvas(self.parent, width=canv_w, height=canv_h)
        # self.canv.config(relief='flat',
        #                  width=canv_w,
        #                  heigh=canv_h, bd=2)
        # placing a canvas into frame
        # self.canv.grid(column=0, row=0, sticky='nsew')
        # accociating scrollbar comands to canvas scroling
        # self.hbar.config(command=self.canv.xview)
        self.vbar.config(command=self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = tk.Frame(self.parent)

        self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw', height=height, width=width)

        self.canv.config(  # xscrollcommand=self.hbar.set,
                         yscrollcommand=self.vbar.set,
                         scrollregion=(0, 0, canv_h, canv_w))

        # self.vbar.lift(self.scrollwindow)
        # self.hbar.lift(self.scrollwindow)
        self.scrollwindow.bind('<Configure>', self._configure_window)
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight()+1)
        self.canv.config(scrollregion='0 0 %s %s' % size)
        # if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        # if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
        #     # update the canvas's width to fit the inner frame
        #     # self.canv.config(height=self.scrollwindow.winfo_reqheight())
