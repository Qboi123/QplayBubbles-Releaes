from threadsafe_tkinter import Button, FLAT, CENTER, TclError

from background import Background


class TitleMenu(object):
    def __init__(self, root, font, f_size, config, lang, on_load=lambda: None):
        self.root = root
        self.font = font
        self.f_size = f_size
        self.config = config
        self.lang = lang
        self.load = on_load

        # Items
        self.items = list()

        # Defining self.background class.
        self.background = Background(self.root)

        self.start_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.load(self),
                                text=self.lang["home.start"],
                                relief=FLAT, font=(self.font, 20 + self.f_size))
        self.start_btn.place(x=self.config["width"] / 2, y=self.config["height"] / 2 - 40, width=310, anchor=CENTER)

        self.quit_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.root.destroy(),
                               text=self.lang["home.quit"],
                               relief=FLAT, font=(self.font, 20 + self.f_size))
        self.quit_btn.place(x=self.config["width"] / 2 + 80, y=self.config["height"] / 2 + 40, width=150, anchor=CENTER)

        self.options_btn = Button(self.root, bg="#007f7f", fg="#7fffff", bd=4,
                                  text=self.lang["home.options"],
                                  relief=FLAT, font=(self.font, 20 + self.f_size))  # , command=lambda: self.options())
        self.options_btn.place(x=self.config["width"] / 2 - 80, y=self.config["height"] / 2 + 40, width=150,
                               anchor=CENTER)

        # Refresh game.
        self.root.update()

        # Non-stop refreshing the background.
        while True:
            try:
                self.background.create_bubble()
                self.background.move_bubbles()
                self.background.cleanup_bubs()
                self.root.update()
            except TclError:
                break

        self.root.mainloop()

    def destroy(self):
        self.options_btn.destroy()
        self.background.destroy()
        self.start_btn.destroy()
        self.quit_btn.destroy()
