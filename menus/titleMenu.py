import os
import sys

from tkinter import Button, CENTER, TclError

from background import Background
from registry import Registry
from scenemanager import Scene
from utils import Font


class TitleMenu(Scene):
    def __init__(self):
        super(TitleMenu, self).__init__(Registry.get_window("default"))

        self.lang = Registry.gameData["language"]
        self.config = Registry.gameData["config"]
        self.btnFont: Font = Registry.gameData["fonts"]["titleButtonFont"]

        # Items
        self.items = list()

        # Create background
        self.background = Background(self.frame)

        # Create buttons
        self.start_btn = Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, command=lambda: self.play_event(), text=self.lang["home.start"],
            relief="flat", font=self.btnFont.get_tuple())
        self.quit_btn = Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, command=lambda: os.kill(os.getpid(), 0),
            text=self.lang["home.quit"], relief="flat", font=self.btnFont.get_tuple())
        self.options_btn = Button(
            self.frame, bg="#007f7f", fg="#7fffff", bd=15, text=self.lang["home.options"], relief="flat",
            font=self.btnFont.get_tuple())

        # Place buttons on screen
        self.start_btn.place(
            x=Registry.gameData["WindowWidth"] / 2, y=Registry.gameData["WindowHeight"] / 2 - 40, width=310, anchor="center")
        self.quit_btn.place(
            x=Registry.gameData["WindowWidth"] / 2 + 80, y=Registry.gameData["WindowHeight"] / 2 + 40, width=150, anchor=CENTER)
        self.options_btn.place(
            x=Registry.gameData["WindowWidth"] / 2 - 80, y=Registry.gameData["WindowHeight"] / 2 + 40, width=150, anchor="center")

        # Refresh game.
        self.frame.update()

        self.loop_active = True

    def mainloop(self):
        import time
        # Titlemenu mainloop
        self.background._canvas.update()
        end_time = time.time() + 10
        while self.loop_active:
            try:
                # Update background
                self.background.create_bubble()
                self.background.move_bubbles()
                self.background.cleanup_bubs()

                # Update window
                self.frame.update()
                self.frame.update_idletasks()

                if "--travis" in sys.argv:
                    if time.time() > end_time:
                        Registry.get_window("default").destroy()
                        break
            except TclError:
                break

    def show_scene(self, *args, **kwargs):
        super(TitleMenu, self).show_scene()

        self.loop_active = True
        self.mainloop()

    def hide_scene(self):
        super(TitleMenu, self).hide_scene()
        self.loop_active = False

    def play_event(self):
        self.scenemanager.change_scene("SaveMenu")

    def destroy(self):
        self.options_btn.destroy()
        self.background.destroy()
        self.start_btn.destroy()
        self.quit_btn.destroy()
