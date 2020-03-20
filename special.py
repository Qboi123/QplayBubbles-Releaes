import tkinter as tk

from tkinter import *


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
