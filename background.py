from random import randint
from threadsafe_tkinter import Canvas, Tk


class Background(object):
    """
    Background for the title menu.
    This is a random animation.
    """

    def __init__(self, root: Tk):
        # Widgets
        self._root = root
        self._canvas = Canvas(root, bg="#00afaf", highlightthickness=0)
        self._canvas.pack(fill="both", expand=True)

        # Bubble-sprites config.
        self.__bubbles = []
        self.__speed = []

    def create_bubble(self):
        r = randint(9, 60)
        x = self._root.winfo_width() + 100
        y = randint(int(r), int(self._canvas.winfo_height() - r))

        spd = randint(7, 10)

        self.__bubbles.append(self._canvas.create_oval(x - r, y - r, x + r, y + r, outline="white"))
        self.__speed.append(spd)

    def cleanup_bubs(self):
        """
        Cleaning up bubbles.
        Deleting bubble if the x coord of the bubble is under -100
        :return:
        """
        from bubble import get_coords

        for index in range(len(self.__bubbles) - 1, -1, -1):
            x, y, = get_coords(self._canvas, self.__bubbles[index])
            if x < -100:
                self._canvas.delete(self.__bubbles[index])
                del self.__bubbles[index]
                del self.__speed[index]

    def move_bubbles(self):
        """
        Move all bubble to the left with the self.__speed with index of the bubble
        :return:
        """
        for index in range(len(self.__bubbles) - 1, -1, -1):
            self._canvas.move(self.__bubbles[index], -self.__speed[index], 0)

    def destroy(self):
        """
        Destroys this custom widget.
        :return:
        """
        self._canvas.destroy()
