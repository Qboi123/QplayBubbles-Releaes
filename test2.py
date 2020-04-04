import time
from tkinter import Tk, Canvas

from PIL import ImageGrab, ImageFilter, ImageTk

root = Tk()

image = ImageGrab.grab(
    (0, 0, root.winfo_screenwidth(), root.winfo_screenheight()),
    True
)
tkim = ImageTk.PhotoImage(image)

root.wm_attributes("-fullscreen", True)

canvas = Canvas(root, highlightthickness=0)
id_ = canvas.create_image(0, 0, image=tkim, anchor="nw")
canvas.pack(fill="both", expand=True)

hwnd = win32gui.FindWindow(None, "Your window title") # Getting window handle
# hwnd = root.winfo_id() getting hwnd with Tkinter windows
# hwnd = root.GetHandle() getting hwnd with wx windows
lExStyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
lExStyle |=  win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE , lExStyle )

# cimage = canvas.create_image(0, 0, image=tkim)
ims = []
tkims = []
for i in range(1, 61):
    im = image.copy()
    ims.append(im.filter(ImageFilter.GaussianBlur(radius=i)))
    tkims.append(ImageTk.PhotoImage(ims[-1]))
for tkimage in tkims:
    canvas.itemconfig(id_, image=tkimage)
    # cimage.config(image=tkimage)
    time.sleep(0.1)
    root.update()
    root.update_idletasks()

# for i in range(1, 21, 2):
#     im = image.copy()
#     im = im.filter(ImageFilter.GaussianBlur(radius=i))
#     tkim = ImageTk.PhotoImage(im)
#     canvas.itemconfig(id_, image=tkim)
#     # time.sleep(0.01)
#     root.update()
#     root.update_idletasks()

root.mainloop()
