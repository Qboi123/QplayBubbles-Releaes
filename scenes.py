import os
import random
import string
from tkinter import ttk
from typing import Optional

from threadsafe_tkinter import Frame, Canvas, Button

from config import Reader
from game import log
from nzt import NZTFile
from registry import Registry
from scenemanager import Scene
from special import ScrolledWindow
from utils import Font

TREEVIEW_BG = "#7f7f7f"
TREEVIEW_FG = "#9f9f9f"
TREEVIEW_SEL_BG = "#00a7a7"
TREEVIEW_SEL_FG = "white"

BUTTON_BG = "#7f7f7f"
BUTTON_BG_FOC = "#00a7a7"
BUTTON_BG_DIS = "#5c5c5c"
BUTTON_FG = "#a7a7a7"
BUTTON_FG_FOC = "white"
BUTTON_FG_DIS = "#7f7f7f"
BUTTON_BD_COL = "#00a7a7"
BUTTON_RELIEF = "flat"
BUTTON_BD_WID = 0

ENTRY_BG = "#5c5c5c"
ENTRY_BG_FOC = "#00a7a7"
ENTRY_BG_DIS = "#7f7f7f"
ENTRY_FG = "#7f7f7f"
ENTRY_FG_FOC = "white"
ENTRY_FG_DIS = "#a7a7a7"
ENTRY_BD_COL = "#00a7a7"
ENTRY_RELIEF = "flat"
ENTRY_BD_WID = 0
ENTRY_SEL_BG = "#00c9c9"
ENTRY_SEL_BG_FOC = "#00dada"
ENTRY_SEL_BG_DIS = "#a7a7a7"
ENTRY_SEL_FG = "#7f7f7f"
ENTRY_SEL_FG_FOC = "white"
ENTRY_SEL_FG_DIS = "#ffffff"


class SavesMenu(Scene):
    def __init__(self, reload=False):
        root = Registry.get_root()

        if not reload:
            super(SavesMenu, self).__init__(root)

        self.btnFont = Registry.gameData["fonts"]["slotsButtonFont"]
        self.lang = Registry.gameData["language"]
        # self.save = None
        # self.frame2 = None
        # self.addBtn = None
        # self.add_input = None
        # self.main_f = None
        # self.s_frame = None
        # self.sw = None
        # self.canv = None
        # self.oFrame = None
        # self.frames = []
        # self.canvass = []
        # self.buttons = []
        # 

        # import os
        # 
        # # Log
        # log.info("Game.load", "Loading...")
        # 
        # # Getting list of slots.
        # path = "slots/"
        # try:
        #     index = os.listdir(path)
        # except FileNotFoundError:
        #     os.makedirs(path, exist_ok=True)
        #     index = os.listdir(path)
        # dirs = []
        # for item in index:
        #     file_path = path + item
        # 
        #     if os.path.isdir(file_path):
        #         dirs.append(item)
        # 
        # # Frame for adding slots.
        # self.frame2 = Frame(bg="#5c5c5c")
        # 
        # # Add-button and -entry (Input)
        # self.addBtn = Button(self.frame2, text=self.lang["slots.add"], relief="flat", bg="#7f7f7f", fg="white",
        #                      command=self.add_save, font=self.btnFont.get_tuple())
        # self.addBtn.pack(side="right", padx=2, pady=5)
        # 
        # # Save add entry (input)
        # self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief="flat", font=("helvetica"))
        # self.add_input.pack(side="left", fill="x", expand=True, padx=2, pady=5)
        # self.add_input.bind("<Return>", self.add_event)
        # 
        # # Update root GUI.
        # root.update()
        # 
        # # Packing the config frame for adding a slot.
        # self.frame2.pack(side="bottom", fill="x")
        # 
        # # Main frame.
        # self.main_f = Frame(root, background="#3c3c3c", height=root.winfo_height() - 100)
        # self.main_f.pack(fill="both", expand=True)
        # 
        # # Slots frame.
        # self.s_frame = Frame(self.main_f, height=self.main_f.winfo_height() - 100, width=700)
        # self.s_frame.pack(fill="y")
        # 
        # # Scrollwindow for the slots frame
        # self.sw = ScrolledWindow(self.s_frame, 700, root.winfo_height() + 0, expand=True, fill="both",
        #                          scrollbarbg="#3c3c3c", scrollbarfg="#5a5a5a")
        # 
        # # Configurate the canvas from the scrollwindow
        # self.canv = self.sw.canv
        # self.canv.config(bg="#2e2e2e")
        # 
        # # self.oFrame.
        # self.oFrame = self.sw.scrollwindow
        # self.frames = []
        # 
        # # Defining the list of widgets
        # self.canvass = []
        # self.buttons = []
        # 
        # # Getting the list of directories in the slots-folder.
        # import os
        # 
        # names = os.listdir("slots/")
        # 
        # # Information variables for each slot.
        # infos = {"dates": [], "score": [], "level": []}
        # 
        # import time
        # 
        # # Prepare info variables
        # for i in names.copy():
        #     if not os.path.exists("slots/" + i + "/bubble.nzt"):
        #         names.remove(i)
        #         continue
        #     mtime = os.path.getmtime("slots/" + i + "/bubble.nzt")
        #     a = time.localtime(mtime)
        # 
        #     b = list(a)
        # 
        #     if a[4] < 10:
        #         b[4] = "0" + str(a[4])
        #     else:
        #         b[4] = str(a[4])
        #     if a[5] < 10:
        #         b[5] = "0" + str(a[5])
        #     else:
        #         b[5] = str(a[5])
        # 
        #     tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
        #     infos["dates"].append(tme_var)
        # 
        #     a = Reader("slots/" + i + "/game.nzt").get_decoded()
        #     infos["score"].append(a["Player"]["score"])
        #     infos["level"].append(a["Player"]["level"])
        # 
        # self.item_info = names
        # 
        # # Define the index variable.
        # i = 0
        # 
        # # Startloop
        # for name in names:
        #     self.frames.append(Frame(self.oFrame, height=200, width=700))
        #     self.canvass.append(Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
        #     self.canvass[-1].pack()
        # 
        #     self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")
        #     self.frames[-1].grid(row=i)
        # 
        #     i += 1

        style = ttk.Style()
        style.theme_settings("default", {
            "TEntry": {
                "configure": {"font": ("Helvetica", 10), "relief": "flat", "selectborderwidth": 0, "padding": 10},
                "map": {
                    "relief": [("active", ENTRY_RELIEF),
                               ("focus", ENTRY_RELIEF),
                               ("!disabled", ENTRY_RELIEF)],
                    "bordercolor": [("active", ENTRY_BD_COL),
                                    ("focus", ENTRY_BD_COL),
                                    ("!disabled", ENTRY_BD_COL)],
                    "background": [("active", ENTRY_BG),
                                   ("focus", ENTRY_BG_FOC),
                                   ("!disabled", ENTRY_BG_DIS)],
                    "fieldbackground": [("active", ENTRY_BG),
                                        ("focus", ENTRY_BG_FOC),
                                        ("!disabled", ENTRY_BG_DIS)],
                    "foreground": [("active", ENTRY_FG),
                                   ("focus", ENTRY_FG_FOC),
                                   ("!disabled", ENTRY_FG_DIS)],
                    "selectbackground": [("active", ENTRY_SEL_BG),
                                         ("focus", ENTRY_SEL_BG_FOC),
                                         ("!disabled", ENTRY_SEL_BG_DIS)],
                    "selectforeground": [("active", ENTRY_SEL_FG),
                                         ("focus", ENTRY_SEL_FG_FOC),
                                         ("!disabled", ENTRY_SEL_FG_DIS)]
                }
            },
            "TLabel": {
                "configure": {"background": "#5c5c5c",
                              "foreground": "#7f7f7f",
                              "font": ("Helvetica", 10)}
            },
            "TButton": {
                "configure": {"font": ("Helvetica", 10), "relief": BUTTON_RELIEF, "bd": 1},
                "map": {
                    "background": [("active", BUTTON_BG_FOC),
                                   ("focus", BUTTON_BG),
                                   ("!disabled", BUTTON_BG)],
                    "bordercolor": [("active", BUTTON_BD_COL),
                                    ("focus", BUTTON_BG_FOC),
                                    ("!disabled", BUTTON_BD_COL)],
                    "foreground": [("active", BUTTON_FG_FOC),
                                   ("focus", BUTTON_FG_FOC),
                                   ("!disabled", BUTTON_FG)],
                }
            },
            "Treeview": {
                "configure": {"padding": 0, "font": ("Helvetica", 10), "relief": "flat", "border": 0,
                              "rowheight": 24},
                "map": {
                    "background": [("active", TREEVIEW_BG),
                                   ("focus", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_BG),
                                   ("selected", TREEVIEW_BG)],
                    "fieldbackground": [("active", TREEVIEW_BG),
                                        ("focus", TREEVIEW_BG),
                                        ("!disabled", TREEVIEW_BG)],
                    "foreground": [("active", TREEVIEW_FG),
                                   ("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_FG),
                                   ("selected", TREEVIEW_FG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            },
            "Treeview.Item": {
                "configure": {"padding": 0},
                "map": {
                    "background": [("active", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_SEL_BG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "fieldbackground": [("!disabled", TREEVIEW_SEL_BG),
                                        ("active", TREEVIEW_SEL_BG),
                                        ("!selected", TREEVIEW_SEL_BG)],
                    "foreground": [("active", TREEVIEW_SEL_BG),
                                   ("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_SEL_FG),
                                   ("selected", TREEVIEW_SEL_BG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            },
            "Treeview.Cell": {
                "configure": {"padding": 0},
                "map": {
                    "background": [("active", TREEVIEW_SEL_BG),
                                   ("!disabled", TREEVIEW_SEL_BG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "fieldbackground": [("!disabled", TREEVIEW_SEL_BG),
                                        ("active", TREEVIEW_SEL_BG),
                                        ("!selected", TREEVIEW_SEL_BG)],
                    "foreground": [("focus", TREEVIEW_SEL_FG),
                                   ("!disabled", TREEVIEW_SEL_FG),
                                   ("!selected", TREEVIEW_SEL_BG)],
                    "relief": [("focus", "flat"),
                               ("active", "flat"),
                               ("!disabled", "flat")]
                }
            }
        })
        # print(style.map("Treeview"))
        # print(style.configure("Treeview"))
        # print(style.co("Treeview"))

        # style.configure("BW.TTreeview", foreground=", background="white")
        #
        # foreground = "black", background = "white"
        # sty
        style.theme_use("default")
        style.configure('TEntry', relief='flat', bd=0, borderwidth=0)

        print(style.layout("TEntry"))

        #   lets try to change this structure
        style.layout('TEntry', [
            ('Entry.highlight', {
                "border": 0,
                'sticky': 'nswe',
                'children': [('Entry.border', {
                    'border': 0,
                    'sticky': 'nswe',
                    'children':
                        [('Entry.padding', {
                            'sticky': 'nswe',
                            'children':
                                [('Entry.textarea', {
                                    'sticky': 'nswe',
                                    "border": 0})]
                        })]
                    }), ('Entry.bd', {
                     'sticky': 'nswe',
                     'children': [(
                         'Entry.padding', {
                             'sticky': 'nswe',
                             'children': [(
                                 'Entry.textarea', {
                                     'sticky': 'nswe'})]
                         })],
                     'border': 0})
                ]
            })])
        style.configure('TEntry', relief='flat', bd=0)

        # style.map("TTreeview", foreground="")
        # print(style)
        self.buttons = []
        self.names = {}

        self.oFrame = Frame(self.frame, bg="#5c5c5c")

        # for shell in SHELLS: self.buttons.append(Button(self.oFrame, text=shell["name"], bg="#4f4f4f", fg="#7f7f7f",
        # command=lambda path=shell["path"]: self.open_shell(path), width=10, relief="flat", border=0,
        # font=("Helvetica", 16))) self.buttons[-1].pack(fill="both", expand=True, pady=2, padx=4)
        #
        # self.oFrame.pack(fill="both", expand=True)

        # Frame for adding slots.
        self.frame2 = Frame(self.oFrame, bg="#5c5c5c", height=94, width=720)

        self.controlsFrame = Frame(self.frame2, height=92, width=720)
        self.controlsFrameA = Frame(self.controlsFrame, bg="#5c5c5c", width=720, height=36)

        # Add-button and -entry (Input)
        self.openBtn = ttk.Button(self.controlsFrameA, text="Open",  # relief="flat", bg="#7f7f7f", fg="white",
                                  command=self.open_save, width=24)  # , font=["Helvetica", 10], bd=5)
        self.openBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.renameBtn = ttk.Button(self.controlsFrameA, text="Add",  # relief="flat", bg="#7f7f7f", fg="white",
                                    command=self.add_save, width=24)  # , font=["Helvetica", 10], bd=5)
        self.renameBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.controlsFrameA.pack()
        self.controlsFrameA.pack_propagate(0)
        self.controlsFrameA.update()

        self.controlsFrameB = Frame(self.controlsFrame, bg="#5c5c5c", width=720, height=36)

        # Add-button and -entry (Input)
        self.removeBtn = ttk.Button(self.controlsFrameB, text="Remove",  # relief="flat", bg="#7f7f7f", fg="white",
                                    command=self.remove_save,
                                    width=12)  # , font=["Helvetica", 10], bd=5)
        self.removeBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        # Add-button and -entry (Input)
        self.removeBtn = ttk.Button(self.controlsFrameB, text="Remove",  # relief="flat", bg="#7f7f7f", fg="white",
                                    command=self.rename_save,
                                    width=12)  # , font=["Helvetica", 10], bd=5)
        self.removeBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)
        self.resetBtn = ttk.Button(self.controlsFrameB, text="Reset",
                                   command=self.reset_save,
                                   width=12)
        self.resetBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)

        self.backBtn = ttk.Button(self.controlsFrameB, text="Back",
                                  command=self.back_title, width=12)
        self.backBtn.pack(side="left", padx=1, pady=1, fill="both", expand=True)

        # self.rename = Button(self.controlsFrameA, text="Rename Shell", relief="flat", bg="#7f7f7f", fg="white",
        #                   command=self.add_shell, font=["Helvetica", 10], bd=5)
        # self.rename.pack(side="left", padx=2, pady=5, fill="both", expand=True)
        self.controlsFrameB.pack()
        self.controlsFrameB.pack_propagate(0)
        self.controlsFrameB.update()

        root.update()
        root.update_idletasks()

        self.controlsFrame.pack(padx=1, pady=1)
        self.controlsFrame.pack_propagate(0)

        # print(self.controlsFrameA.winfo_reqwidth())
        # self.add_input = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief="flat", font=("helvetica", 10))
        # self.add_input.pack(side=LEFT, fill="x", expand=True, padx=2, pady=5)
        # self.add_input.bind("<Return>", self.add_shell)

        # Update root GUI.
        self.update()

        # Packing the config frame for adding a slot.
        self.frame2.pack(side="bottom", fill="x", padx=2)

    def show_scene(self, *args, **kwargs):
        super(SavesMenu, self).show_scene(*args, **kwargs)
        self.initialize_scene()

    def initialize_scene(self):
        # Main frame.
        self.main_f = Frame(self.oFrame, background="#3c3c3c", height=Registry.gameData["WindowHeight"] - 100)
        self.main_f.pack(fill="both", expand=True)

        # Slots frame.
        self.s_frame = Frame(self.main_f, height=self.main_f.winfo_height() - 100, width=700)
        self.s_frame.pack(fill="y", expand=True)

        # Scrollwindow for the slots frame
        self.sw = ScrolledWindow(self.s_frame, 700, self.oFrame.winfo_height() + 0, expand=True, fill="both")

        self.sw.vbar.configure(bg="#3c3c3c", fg="#7f7f7f")

        # Configurate the canvas from the scrollwindow
        self.canv = self.sw.canv
        self.canv.config(bg="#2e2e2e")

        # self.oFrame.
        self.frame_sw = self.sw.scrollwindow
        self.frames = []

        # Defining the list of widgets
        self._id = {}
        self.index = {}
        self.canvass = []
        self.buttons = []

        self.oldSelected: Optional[Canvas] = None
        self.selectedCanvas: Optional[Canvas] = None
        self._hoverCanvasOld: Optional[Canvas] = None
        self._hoverCanvas: Optional[Canvas] = None

        titlefont = Font("Helvetica", 25, "bold")
        infofont = Font("Helvetica", 16)

        # Get slots
        names = os.listdir("slots/")

        # Information variables for each slot.
        infos = {"dates": [], "score": [], "level": []}

        import time

        # Prepare info variables
        for i in names.copy():
            if not os.path.exists("slots/" + i + "/bubble.nzt"):
                names.remove(i)
                continue
            mtime = os.path.getmtime("slots/" + i + "/bubble.nzt")
            a = time.localtime(mtime)

            b = list(a)

            if a[4] < 10:
                b[4] = "0" + str(a[4])
            else:
                b[4] = str(a[4])
            if a[5] < 10:
                b[5] = "0" + str(a[5])
            else:
                b[5] = str(a[5])

            # tme_var = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            tme_var = f"{a[2]}/{a[1]}/{a[0]} {a[3]}:{a[4]}:{a[5]}"
            infos["dates"].append(tme_var)

            a = Reader("slots/" + i + "/game.nzt").get_decoded()
            infos["score"].append(a["Player"]["score"])
            infos["level"].append(a["Player"]["level"])
        print(infos)

        self.item_info = names

        # Define the index variable.
        i = 0

        # Startloop
        for name in names:
            print(i)
            self.frames.append(Frame(self.frame_sw, height=200, width=700))
            self.canvass.append(
                Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()
            self._id[self.canvass[-1]] = {}
            self._id[self.canvass[-1]]["Title"] = self.canvass[-1].create_text(10, 10, text=name,
                                                                               fill="#a7a7a7", anchor="nw",
                                                                               font=("Consolas", 26, "bold"))
            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")
            subids = [self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor="nw",
                                                   font=infofont.get_tuple()),
                      self.canvass[-1].create_text(240, 50, text="Level: " + str(infos["level"][i]), fill="#afafaf",
                                                   anchor="nw", font=infofont.get_tuple()),
                      self.canvass[-1].create_text(370, 50, text="Score: " + str(infos["score"][i]), fill="#afafaf",
                                                   anchor="nw", font=infofont.get_tuple())]
            self._id[self.canvass[-1]]["Infos"] = subids
            self.canvass[-1].bind("<ButtonRelease-1>",
                                  lambda event, c=self.canvass[-1]: self._on_canv_lclick(c))
            self.canvass[-1].bind("<Double-Button-1>", lambda event, n_=name: self.open_direct(n_))
            self.canvass[-1].bind("<Motion>", lambda event, c=self.canvass[-1]: self._on_canv_motion(c))
            self.canvass[-1].bind("<Leave>", lambda event, c=self.canvass[-1]: self._on_canv_leave(c))
            self.names[self.canvass[-1]] = name
            self.index[self.canvass[-1]] = i
            self.frames[-1].grid(row=i)

            i += 1

        self.oFrame.pack(fill="both", expand=True)

    def hide_scene(self):
        self.main_f.destroy()
        self.oFrame.pack_forget()

        super(SavesMenu, self).hide_scene()

    def _on_canv_leave(self, hover_canvas):
        if self._hoverCanvasOld is not None:
            if self.selectedCanvas != self._hoverCanvasOld:
                self._hoverCanvasOld.config(bg="#7f7f7f")
                self._hoverCanvasOld.itemconfig(self._id[self._hoverCanvasOld]["Title"], fill="#a7a7a7")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#a7a7a7")
            else:
                self._hoverCanvasOld.config(bg="darkcyan")
                self._hoverCanvasOld.itemconfig(self._id[hover_canvas]["Title"], fill="#00bfbf")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
        self._hoverCanvasOld = None

    def _on_canv_motion(self, hover_canvas):
        if self._hoverCanvasOld == hover_canvas:
            return
        if self._hoverCanvasOld is not None:
            if self.selectedCanvas != self._hoverCanvasOld:
                self._hoverCanvasOld.config(bg="#7f7f7f")
                self._hoverCanvasOld.itemconfig(self._id[self._hoverCanvasOld]["Title"], fill="#a7a7a7")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#939393")
            else:
                self._hoverCanvasOld.config(bg="darkcyan")
                self._hoverCanvasOld.itemconfig(self._id[hover_canvas]["Title"], fill="#007f7f")
                for subid in self._id[self._hoverCanvasOld]["Infos"]:
                    self._hoverCanvasOld.itemconfig(subid, fill="#00a7a7")
        # print(self.selectedCanvas, self._hoverCanvasOld)
        print(self.selectedCanvas == self._hoverCanvasOld)
        print(self.selectedCanvas == hover_canvas)
        self._hoverCanvasOld = hover_canvas

        if hover_canvas != self.selectedCanvas:
            hover_canvas.config(bg="#a7a7a7")
            hover_canvas.itemconfig(self._id[hover_canvas]["Title"], fill="#ffffff")
            for subid in self._id[hover_canvas]["Infos"]:
                hover_canvas.itemconfig(subid, fill="#dadada")
        else:
            hover_canvas.config(bg="#00a7a7")
            hover_canvas.itemconfig(self._id[hover_canvas]["Title"], fill="#7fffff")
            for subid in self._id[hover_canvas]["Infos"]:
                hover_canvas.itemconfig(subid, fill="#00dada")
        self._hoverCanvas = hover_canvas

    def _on_canv_lclick(self, c: Canvas):
        if self.oldSelected is not None:
            self.oldSelected.config(bg="#7f7f7f")
            self.oldSelected.itemconfig(self._id[self.oldSelected]["Title"], fill="#a7a7a7")
            for subid in self._id[self.oldSelected]["Infos"]:
                self.oldSelected.itemconfig(subid, fill="#939393")
        self.oldSelected = c

        c.config(bg="#00a7a7")
        c.itemconfig(self._id[c]["Title"], fill="#7fffff")
        for subid in self._id[c]["Infos"]:
            c.itemconfig(subid, fill="#00dada")

        self.selectedCanvas = c

    def reset_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = Registry.get_root()

        self.oFrame.destroy()
        self.oFrame = Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Are you sure you want to reset the save'{src}'?", fill="cyan",
                                     anchor="nw", font=("Helvetica", 24))
        self.titleCanvas.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = Frame(self.oFrame, bg="#5c5c5c", width=480)
        self.buttonFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.noBtn = ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="No")
        self.yesBtn = ttk.Button(self.buttonFrame, command=lambda: self.reset_action(src), text="Yes")
        self.noBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        self.yesBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320, anchor="nw", width=480)

        self.textInput = ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def remove_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = Registry.get_root()

        self.oFrame.destroy()
        self.oFrame = Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Are you sure you want to remove the save '{src}'?", fill="cyan",
                                     anchor="nw", font=("Helvetica", 24))
        self.titleCanvas.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = Frame(self.oFrame, bg="#5c5c5c", width=480)
        self.buttonFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.noBtn = ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(),
                                # bg="#7f7f7f", fg="#a7a7a7",
                                text="No")  # , relief="flat", border=0, bd=5)
        self.yesBtn = ttk.Button(self.buttonFrame, command=lambda: self.remove_action(src),
                                 # bg="#7f7f7f", fg="#a7a7a7",
                                 text="Yes")  # , relief="flat", border=0, bd=5)
        self.noBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.yesBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        # print("Width:", self.buttonFrame.winfo_width())
        self.optionsFrame.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320, anchor="nw", width=480)

        self.textInput = ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def close_options_frame(self):
        self.oFrame.destroy()
        self.__init__(reload=True)
        self.initialize_scene()

    def add_save(self):
        """
        Add-save menu.

        :return:
        """

        root = Registry.get_root()

        def update(event):
            if event.char in string.digits:
                pass
            elif event.keysym.lower() == "backspace":
                pass
            else:
                return "break"

        self.oFrame.destroy()
        self.oFrame = Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text="Add shell", fill="cyan", anchor="nw", font=("Consolas", 24))
        self.titleCanvas.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = Frame(self.oFrame, bg="#5c5c5c", width=480)

        self.nameEntryFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.nameLabel = ttk.Label(self.nameEntryFrame, relief="flat", width=8, text="Name:", anchor="w")
        self.nameLabel.pack(side="left")
        self.nameEntry = ttk.Entry(self.nameEntryFrame)
        self.nameEntry.pack(side="left", fill="x", expand=True)
        self.nameEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.seedEntryFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.seedLabel = ttk.Label(self.seedEntryFrame, relief="flat", width=8, text="Seed:", anchor="w")
        self.seedLabel.pack(side="left")
        self.seedEntry = ttk.Entry(self.seedEntryFrame)
        self.seedEntry.pack(side="left", fill="x", expand=True)
        self.seedEntry.bind("<Key>", update)
        self.seedEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.buttonFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.emptyLabel = ttk.Label(self.buttonFrame, relief="flat", width=8, text="", anchor="w")
        self.emptyLabel.pack(side="left")
        self.cancelBtn = ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="Cancel")
        self.resetBtn = ttk.Button(self.buttonFrame, command=lambda: self.add_action(self.nameEntry.get(), self.seedEntry.get()), text="Add")
        self.cancelBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.resetBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240 - 69, y=320, anchor="nw", width=480)

        self.textInput = ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def rename_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        root = Registry.get_root()

        self.oFrame.destroy()
        self.oFrame = Frame(self.frame, bg="#5c5c5c")
        self.titleCanvas = Canvas(self.oFrame, bg="#5c5c5c", highlightthickness=0, width=480, height=48)
        self.titleCanvas.create_text(0, 0, text=f"Rename save '{src}'", fill="cyan", anchor="nw", font=("Consolas", 24))
        self.titleCanvas.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240, y=320 - 48, anchor="nw")
        self.optionsFrame = Frame(self.oFrame, bg="#5c5c5c", width=480)

        self.nameEntryFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.nameLabel = ttk.Label(self.nameEntryFrame, relief="flat", width=8, text="Name:", anchor="w")
        self.nameLabel.pack(side="left")
        self.nameEntry = ttk.Entry(self.nameEntryFrame)
        self.nameEntry.pack(side="left", fill="x", expand=True)
        self.nameEntryFrame.pack(fill="x", expand=True, padx=1, pady=1)

        self.buttonFrame = Frame(self.optionsFrame, bg="#5c5c5c", width=480)
        self.emptyLabel = ttk.Label(self.buttonFrame, relief="flat", width=8, text="", anchor="w")
        self.emptyLabel.pack(side="left")
        self.cancelBtn = ttk.Button(self.buttonFrame, command=lambda: self.close_options_frame(), text="Cancel")
        self.renameBtn = ttk.Button(self.buttonFrame, command=lambda: self.rename_action(src, self.nameEntry.get()),
                                    text="Add")
        self.cancelBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.renameBtn.pack(side="left", fill="x", expand=True, padx=1, pady=1)  # , height=20)
        self.buttonFrame.pack(fill='x', side="bottom", expand=True)

        root.update()
        root.update_idletasks()
        self.optionsFrame.place(x=int(Registry.gameData["WindowWidth"] / 2) - 240 - 69, y=320, anchor="nw", width=480)

        self.textInput = ttk.Entry()
        self.oFrame.pack(fill="both", expand=True)

    def add_action(self, new, seed):
        """
        Adding a slot to your game.

        :param new: Name of the new save
        :return:
        """

        max_seed = 2**32

        if seed == "":
            seed = random.randint(0, max_seed)

        print(max_seed)

        seed = int(seed)

        import os

        if (new in ("aux", "con", "num", "..")) or (len(new) < 3) or (
                new.lower() in [f.lower() for f in os.listdir("slots/")]):
            return

        # Creating dir for the game.
        os.makedirs("slots/" + new, exist_ok=True)

        game_data = {"Player": {"Money": {"diamonds": 0, "coins": 0},
                                "ShipStats": {"ship_speed": 10, "ShipPosition": [960, 540]},
                                "Abilities": {"teleports": 0, "level-score": 10000},
                                "lives": 7, "score": 0, "high_score": 0, "teleports": 0, "level": 1},
                     "BubbleStats": {"bubspeed": 5},
                     "Effects": {"confusion": False, "confusion_time": 0, "notouch": False, "notouch_time": 0,
                                 "paralyse": False, "paralyse_time": 0, "scorestate": 1, "scorestate_time": 0,
                                 "secure": False, "secure_time": 0, "shotspeed": 0.1, "shotspeed_time": 0,
                                 "slowmotion": False, "slowmotion_time": 0, "special_level": False,
                                 "special_level_time": 0,
                                 "speedboost": False, "speedboost_time": 0, "timebreak": False,
                                 "timebreak_time": 0},
                     "GameInfo": {
                         "seed": seed}
                     }

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile("slots/" + new + "/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        game_data_file = NZTFile("slots/" + new + "/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()

        self.close_options_frame()

    def reset_action(self, src):
        """
        Resets the game save

        :param src: Name of the save
        :return:
        """

        max_seed = 2**32
        seed = random.randint(0, max_seed)

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the save (dir)
        os.removedirs("slots/" + src)

        # Getting the input text.
        if src in ("aux", "con", ".", ".."):
            return

        # Creating dir for the game.
        os.makedirs("slots/" + src, exist_ok=True)

        game_data = {"Player": {"Money": {"diamonds": 0, "coins": 0},
                                "ShipStats": {"ship-speed": 10, "ShipPosition": [960, 540]},
                                "Abilities": {"teleports": 0, "level-score": 10000},
                                "lives": 7, "score": 0, "high-score": 0, "teleports": 0, "level": 1},
                     "BubbleStats": {"bubspeed": 5},
                     "Effects": {"confusion": False, "confusion_time": 0, "notouch": False, "notouch_time": 0,
                                 "paralyse": False, "paralyse_time": 0, "scorestate": 1, "scorestate_time": 0,
                                 "secure": False, "secure_time": 0, "shotspeed": 0.1, "shotspeed_time": 0,
                                 "slowmotion": False, "slowmotion_time": 0, "special-level": False,
                                 "special-level_time": 0,
                                 "speedboost": False, "speedboost_time": 0, "timebreak": False, "timebreak_time": 0},
                     "GameInfo": {
                         "seed": seed}
                     }

        bubble_data = {"bub-id": [], "bub-special": [], "bub-action": [], "bub-radius": [], "bub-speed": [],
                       "bub-position": [], "bub-index": [], "key-active": False}

        game_data_file = NZTFile("slots/" + src + "/game.nzt", "w")
        game_data_file.data = game_data
        game_data_file.save()
        game_data_file.close()

        game_data_file = NZTFile("slots/" + src + "/bubble.nzt", "w")
        game_data_file.data = bubble_data
        game_data_file.save()
        game_data_file.close()

        self.close_options_frame()

    def open_direct(self, n_):
        """
        Open the game direct from the name

        :param n_: The name of the save
        :return:
        """

        self.open(n_)

    # noinspection PyTypeChecker
    def remove_action(self, src):
        """
        Deletes the save.

        :param src: The name of the save
        :return:
        """

        import os

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("slots/" + src)

        self.close_options_frame()

    def rename_action(self, src, new):
        """
        Renames a save.

        :param src: Source name of the save
        :param new: New name of the save
        :return:
        """

        import os

        # noinspection PyTypeChecker
        # Rename the dir for the slot.
        os.rename("slots/" + src, "slots/" + new)

        self.close_options_frame()

    def open_save(self):
        if self.selectedCanvas is None:
            return
        else:
            src = self.names[self.selectedCanvas]

        self.open_action(src)

    def open_action(self, src):
        """
        Opens and run the game save.

        :param src: Name of the save
        :return:
        """

        # Removes oFrame.
        self.oFrame.destroy()

        # Runs the game
        self.scenemanager.change_scene("GameScene", src)

    def back_title(self):
        self.scenemanager.change_scene("TitleScreen")
