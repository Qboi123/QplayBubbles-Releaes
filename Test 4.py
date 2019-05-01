import tkinter as tk
import tkinter.ttk as ttk
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

    def __init__(self, parent, canv_w=400, canv_h=400, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)

        self.parent = parent

        # creating a scrollbars

        self.canv = Canvas(self.parent, bg='#FFFFFF', width=canv_w-100, height=canv_h-100,
                           scrollregion=(0, 0, canv_w, canv_h), highlightthickness=0)
        # self.hbar = Scrollbar(self.parent, orient=HORIZONTAL)
        # self.hbar.pack(side=BOTTOM, fill=X)
        # self.hbar.config(command=self.canv.xview)
        self.vbar = Scrollbar(self.parent, orient=VERTICAL)
        self.vbar.pack(side=RIGHT, fill=Y)
        self.vbar.config(command=self.canv.yview)
        self.canv.config(width=300, height=300)
        self.canv.config(# xscrollcommand=self.hbar.set,
                         yscrollcommand=self.vbar.set)
        self.canv.pack(side=LEFT, expand=True, fill=BOTH)
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
        self.scrollwindow = tk.Frame(self.parent, width=canv_w-20, height=canv_h-20)

        self.canv.create_window(0, 0, window=self.scrollwindow, anchor='nw')

        self.canv.config( # xscrollcommand=self.hbar.set,
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
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        self.canv.config(scrollregion='0 0 %s %s' % size)
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width=self.scrollwindow.winfo_reqwidth())
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height=self.scrollwindow.winfo_reqheight())


def open(event):
    print(event.widget.master.__dict__)
    print(event.widget.master)
    print(event.widget.master.grid_info()["row"])
    print(item_info[event.widget.master.grid_info()["row"]])


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("716x600")
    main = Frame(background="#3c3c3c")
    main.pack(expand=True, fill=BOTH)
    s_frame = Frame(main, height=main.winfo_height(), width=700)
    s_frame.pack()
    sw = ScrolledWindow(s_frame, root.winfo_height(), 700, heigh=400, width=400)
    frame = sw.scrollwindow
    frames = []
    canvass = []
    open_btn = []

    import os
    names = os.listdir("/Windows/")
    item_info = names

    print(names)

    i = 0

    for name in tuple(names):
        print("Round: "+str(i))
        print(names[i])
        item_info.append(i)
        frames.append(tk.Frame(frame, height=200, width=700))
        canvass.append(tk.Canvas(frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
        canvass[-1].pack()
        canvass[-1].create_text(10, 10, text=name, fill="#afafaf", anchor=NW, font=("Helvetica", 26))
        canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")

        open_btn.append(Button(frames[-1], relief=FLAT, text="open", bg="#afafaf"))
        open_btn.copy()[-1].place(x=650, y=150, anchor=SE)
        open_btn.copy()[-1].bind("<ButtonRelease-1>", open)
        frames[-1].grid(row=i)

        i += 1

    print(sw.scrollwindow.children)
    root.mainloop()
