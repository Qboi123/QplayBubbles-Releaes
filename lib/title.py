import time
from random import randint
from typing import Union

from threadsafe_tkinter import *


class TitleMenu:
    def __init__(self):
        from .utils.get_set import get_root
        from .registry import registry

        # Detect Root
        self._root = get_root()
        self.config = registry["Config"]
        self.lang = registry["Language"]
        self.font = "Helvetica"
        self.f_size = 12

        self._root.update()
        self._root.update_idletasks()
        # Defining self.background class.
        self.background = Background(self._root)

        self._root.update()
        self._root.update_idletasks()

        self.startBtn = Button(self._root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.set("start"),
                               text=self.lang["home.start"],
                               relief=FLAT, font=(self.font, 9 + self.f_size))
        self.startBtn.place(x=self._root.winfo_width() / 2, y=self._root.winfo_height() / 2 - 40, width=310,
                            anchor=CENTER)

        self.quitBtn = Button(self._root, bg="#007f7f", fg="#7fffff", bd=4, command=lambda: self.set("quit"),
                              text=self.lang["home.quit"],
                              relief=FLAT, font=(self.font, 9 + self.f_size))
        self.quitBtn.place(x=self._root.winfo_width() / 2 + 80, y=self._root.winfo_height() / 2 + 40, width=150,
                           anchor=CENTER)

        self.optionsBtn = Button(self._root, bg="#007f7f", fg="#7fffff", bd=4,
                                 text=self.lang["home.options"],
                                 relief=FLAT, font=(self.font, 9 + self.f_size), command=lambda: self.set("options"))
        self.optionsBtn.place(x=self._root.winfo_width() / 2 - 80, y=self._root.winfo_height() / 2 + 40, width=150,
                              anchor=CENTER)

        # Refresh game.
        self._root.update()

        self._selected: Union[str, None] = None

        self.exists = True

        self.background.start()

        # Non-stop refreshing the background.
        time2 = time.time()
        while self.exists:
            time1 = time.time()
            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                self.move_fps = 1 / (time1 - time2)
            except ZeroDivisionError:
                self.move_fps = 1
            time2 = time.time()
            try:
                self.background.create_bubble()
                self.background.move_bubbles(self.move_fps)
                self.background.cleanup_bubs()
                self.background.update()
                # time.sleep(0.0001)
            except TclError:
                break

    def get(self):
        return self._selected

    def set(self, string: str):
        self._selected = string
        self.exists = False
        time.sleep(0.1)
        self.destroy()

    def destroy(self):
        self.background.destroy()
        self.startBtn.destroy()
        self.quitBtn.destroy()
        self.optionsBtn.destroy()

    def __del__(self):
        self.destroy()


class Background:
    """
    Background for the title menu.
    This is a random animation.
    """

    def __init__(self, root: Tk):
        # Widgets
        self._root = root
        self._canvas = Canvas(root, bg="#00afaf", highlightthickness=0)
        self._canvas.pack(fill=BOTH, expand=TRUE)

        # Bubble-sprites config.
        self.__bubbles = []
        self.__speed = []

        self.maxBubbles = 200

        # for i in range(0, 150):
        #     self.create_bubble()

    def start(self):
        while len(self.__bubbles) < self.maxBubbles:
            try:
                if len(self.__bubbles) < self.maxBubbles:
                    r = randint(9, 60)
                    x = randint(0 - int(r), self._root.winfo_width() + r)
                    y = randint(int(r), int(self._canvas.winfo_height() - r))

                    spd = randint(7, 10)

                    self.__bubbles.append(self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="white"))
                    self.__speed.append(spd)
            except IndexError:
                pass
            except TclError:
                pass

    def create_bubble(self):
        try:
            if len(self.__bubbles) < self.maxBubbles:
                r = randint(9, 60)
                x = self._root.winfo_width() + r
                y = randint(int(r), int(self._canvas.winfo_height() - r))

                spd = randint(7, 10)

                self.__bubbles.append(self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="white"))
                self.__speed.append(spd)
        except IndexError:
            pass
        except TclError:
            pass

    def cleanup_bubs(self):
        """
        Cleaning up bubbles.
        Deleting bubble if the x coord of the bubble is under -100
        :return:
        """
        from .utils import get_coords

        for index in range(len(self.__bubbles) - 1, -1, -1):
            try:
                x, y, = get_coords(self._canvas, self.__bubbles[index])
                if x < -100:
                    self._canvas.delete(self.__bubbles[index])
                    del self.__bubbles[index]
                    del self.__speed[index]
            except IndexError:
                pass
            except TclError:
                pass

    def move_bubble(self, index, fps1):
        try:
            self._canvas.move(self.__bubbles[index], -self.__speed[index] / (fps1 / 40), 0)
        except TclError:
            pass
        except IndexError:
            pass

    def move_bubbles(self, fps1):
        """
        Move all bubble to the left with the self.__speed with index of the bubble
        :return:
        """
        for index in range(len(self.__bubbles) - 1, -1, -1):
            try:
                # print(time1 - time2)
                # print(1/(time1 - time2))
                # noinspection PyUnboundLocalVariable
                pass
            except ZeroDivisionError:
                pass
            except NameError:
                pass
            self.move_bubble(index, fps1)

    def update(self):
        self._canvas.update()

    def destroy(self):
        """
        Destroys this custom widget.
        :return:
        """
        self._canvas.destroy()

    def __del__(self):
        self.destroy()
