from time import sleep

from threadsafe_tkinter import *

from lib.base import Accent
from .utils.config import *
from .utils.get_set import get_root, get_game


class SlotsMenu(object):
    addBtn: Button
    run: Callable
    returnTitle: Callable
    root: Tk
    game: Optional[Canvas]
    gameBuild: int
    version: int
    versionDir: int
    accent: Accent
    frame3a: Frame
    frame2a: Frame
    cFCanvas: Canvas

    # noinspection PyPep8Naming
    def __init__(self, open_command: Callable, back_command: Callable):
        """
        This is the Slots Menu.

        Loading slots-menu.
        :return:
        """
        self.accent = Accent("#ff3f00")
        from .ui.special import ScrolledWindow
        from .registry import get_value, get_register
        import os

        self.root = get_root()
        self.game = get_game()
        self.gameBuild: int = self.game.gameBuild
        self.version: int = self.game.version
        self.versionDir: int = self.game.versionDir

        self.run = open_command
        self.returnTitle = back_command

        self.font = get_value("Config", "font")["family"]
        self.f_size = get_value("Config", "font")["size"]
        self.lang = get_register("Language")

        # Removes title-menu items.

        # Getting list of slots.
        path: str = "slots/"
        try:
            index: List[str] = os.listdir(path)
        except FileNotFoundError:
            os.makedirs(path, exist_ok=True)
            index = os.listdir(path)
        dirs: List[str] = []
        item: str
        for item in index:
            filePath: str = path + item

            if os.path.isdir(filePath):
                dirs.append(item)

        # Frames for adding slots.
        self.frame2a = Frame(bg="#5c5c5c", height=30)
        self.frame3a = Frame(bg="#5c5c5c", height=30)
        self.frame2 = Frame(self.frame2a, bg="#5c5c5c", height=30, width=900)
        self.frame3 = Frame(self.frame3a, bg="#5c5c5c", height=30, width=900)

        # Language Alternatives
        addBtnText: str = self.checkLangItem("slots.create", "Create")
        openBtnText: str = self.checkLangItem("slots.open", "Open")
        renameBtnText: str = self.checkLangItem("slots.rename", "Rename")
        deleteBtnText: str = self.checkLangItem("slots.remove", "Remove")
        resetBtnText: str = self.checkLangItem("slots.reset", "Reset")
        backBtnText: str = self.checkLangItem("menu.cancel", "Cancel")

        # Define "rename" menu objects
        self.canvasRenameSave: Union[Frame, None] = None
        self.cFrame: Union[Frame, None] = None
        self.cFCanvas: Union[Canvas, None] = None
        self.renameInput: Union[Entry, None] = None
        self.saveRename: Union[Button, None] = None
        self.saveRenameCancel: Union[Button, None] = None

        # Define "create save" menu objects
        self.canvasAddSave: Union[Frame, None] = None
        self.saveInput: Union[Entry, None] = None
        self.seedInput: Union[Entry, None] = None
        self.saveAdd: Union[Button, None] = None
        self.saveAddCancel: Union[Button, None] = None

        # Buttons
        self.addBtn = Button(self.frame2, text=addBtnText, relief=FLAT, bg="#7f7f7f", fg="white",
                             font=[self.font, 20 + self.f_size], command=lambda: self.add_save_menu())
        self.addBtn.place(x=0, y=2, width=449)
        self.openBtn = Button(self.frame2, relief=FLAT, text=openBtnText, bg="#7f7f7f", fg="white",
                              font=[self.font, 20 + self.f_size], command=lambda: self.open(None))
        self.openBtn.place(x=451, y=2, width=449)
        self.renameBtn = Button(self.frame3, relief=FLAT, text=renameBtnText, bg="#7f7f7f", fg="white",
                                font=[self.font, 20 + self.f_size], command=lambda: self.rename_menu())
        self.renameBtn.place(x=0, y=2, width=223)
        self.deleteBtn = Button(self.frame3, relief=FLAT, text=deleteBtnText, bg="#7f7f7f", fg="white",
                                font=[self.font, 20 + self.f_size], command=lambda: self.remove(None))
        self.deleteBtn.place(x=225, y=2, width=224)
        self.resetBtn = Button(self.frame3, relief=FLAT, text=resetBtnText, bg="#7f7f7f", fg="white",
                               font=[self.font, 20 + self.f_size], command=lambda: self.reset_save(None))
        self.resetBtn.place(x=451, y=2, width=224)
        self.backBtn = Button(self.frame3, relief=FLAT, text=backBtnText, bg="#7f7f7f", fg="white",
                              font=[self.font, 20 + self.f_size], command=lambda: self.title_back())
        self.backBtn.place(x=677, y=2, width=223)

        # Add-button and -entry (Input)
        # self.add = Button(self.frame2, text=self.lang["slots.add"], relief=FLAT, bg="#7f7f7f", fg="white",
        #                   command=self.add_save, font=[self.font, 15 + self.f_size])
        # self.addInput = Entry(self.frame2, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT, font=("helvetica"))
        # self.addInput.pack(side=LEFT, fill=X, expand=TRUE, padx=2, pady=5)
        # self.addInput.bind("<Return>", self.add_event)

        # Update root GUI.
        self.root.update()

        # Packing the config frame for adding a slot.
        self.frame3a.pack(side=BOTTOM, fill=X)
        self.frame2a.pack(side=BOTTOM, fill=X)
        self.frame3.pack()
        self.frame2.pack()

        # Main frame.
        self.mainFrame = Frame(self.root, background="#3c3c3c", height=self.root.winfo_height() - 100)
        self.mainFrame.pack(fill=BOTH, expand=True)

        # Slots frame.
        self.sFrame = Frame(self.mainFrame, height=self.mainFrame.winfo_height() - 100, width=700)
        self.sFrame.pack(fill=Y)

        # Scrollwindow for the slots frame
        self.sw = ScrolledWindow(self.sFrame, 700, self.root.winfo_height() + 0, expand=True, fill=BOTH,
                                 scrollbg="#3c3c3c", scrollfg="#7f7f7f")

        # Configurate the canvas from the scrollwindow
        self.canv = self.sw.canv
        self.canv.config(bg="#2e2e2e")

        # self.frame.
        self.frame = self.sw.scrollwindow
        self.frames = []

        # Defining the list of widgets
        self.canvass = []
        self.buttons = []

        # Getting the list of directories in the slots-folder.
        import os

        names = os.listdir("slots/")

        # Information variables for each slot.
        infos = {"dates": [], "score": [], "level": [], "build": []}

        import time
        import pickle

        from . import utils
        from .utils.config import Reader, ConfigReader

        # Prepare info variables
        for i in dirs:
            try:
                mTime = os.path.getmtime("slots/" + i + "/bubble.data")
                a = time.localtime(mTime)

                b = list(a)
                if a[4] < 10:
                    b[4] = "0" + str(a[4])
                else:
                    b[4] = str(a[4])
                if a[5] < 10:
                    b[5] = "0" + str(a[5])
                else:
                    b[5] = str(a[5])

                tmeVar = "%i/%i/%i %i:%s:%s" % (a[2], a[1], a[0], a[3], b[4], b[5])
            except FileNotFoundError:
                try:
                    # mTime = os.path.getmtime("slots/" + i + "/bubble.json")
                    tmeVar = "NEED CONVERTING"
                except FileNotFoundError:
                    tmeVar = None

            try:
                a = Reader("slots/" + i + "/game.data").get_decoded()
            except pickle.UnpicklingError:
                try:
                    a = ConfigReader("slots/" + i + "/game.json").get_decoded()
                except FileNotFoundError:
                    a = None
            except FileNotFoundError:
                try:
                    a = ConfigReader("slots/" + i + "/game.json").get_decoded()
                except FileNotFoundError:
                    a = None

            try:
                try:
                    b = Reader("slots/" + i + "/info.data").get_decoded()
                except pickle.UnpicklingError:
                    b = ConfigReader("slots/" + i + "/info.json").get_decoded()
                except FileNotFoundError:
                    b = ConfigReader("slots/" + i + "/info.json").get_decoded()
                b = utils.dict2class(b)
                print(b.__dict__)
                build = b.LastPlayedOn.build
            except FileNotFoundError:
                b = None
                build = -1

            if (a is not None) and (b is not None) and (tmeVar is not None):
                infos["dates"].append(tmeVar)
                infos["score"].append(a["score"])
                infos["level"].append(a["level"])
                infos["build"].append(build)
            else:
                dirs.__delitem__(dirs.index(i))

        self.itemInfo = names

        # Define the index variable.
        i = 0

        self.selected = -1

        # Startloop
        for name in tuple(dirs):
            self.frames.append(Frame(self.frame, height=200, width=700))
            self.canvass.append(Canvas(self.frames[-1], height=200, width=700, bg="#7f7f7f", highlightthickness=0))
            self.canvass[-1].pack()
            self.canvass[-1].__dict__["build"] = infos["build"][i]
            self.canvass[-1].bind("<ButtonRelease-1>", lambda event: self.select(event))

            self.canvass[-1].create_text(10, 10, text=name, fill="gold", anchor=NW,
                                         font=("Helvetica", 26, "bold"))
            self.canvass[-1].create_text(10, 50, text=infos["dates"][i], fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))
            self.canvass[-1].create_text(240, 50, text="Level: " + str(infos["level"][i]), fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))
            self.canvass[-1].create_text(370, 50, text="Score: " + str(infos["score"][i]), fill="#afafaf", anchor=NW,
                                         font=("Helvetica", 16))

            self.canvass[-1].create_rectangle(0, 0, 699, 201, outline="#3c3c3c")
            #
            # self.buttons.append(
            #     Button(self.frames[-1], relief=FLAT, text=self.lang["slots.open"], bg="#afafaf", width=7,
            #            font=[self.font, 15 + self.f_size]))
            # self.buttons.copy()[-1].place(x=675, y=175, anchor=SE)
            # self.buttons.copy()[-1].bind("<ButtonRelease-1>", lambda event: self.open(event))
            #
            # self.buttons.append(
            #     Button(self.frames[-1], relief=FLAT, text=self.lang["slots.rename"], bg="#afafaf", width=7,
            #            font=[self.font, 15 + self.f_size]))
            # self.buttons.copy()[-1].place(x=600, y=175, anchor=SE)
            # self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.rename)
            #
            # self.buttons.append(
            #     Button(self.frames[-1], relief=FLAT, text=self.lang["slots.remove"], bg="#afafaf", width=7,
            #            font=[self.font, 15 + self.f_size]))
            # self.buttons.copy()[-1].place(x=525, y=175, anchor=SE)
            # self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.remove)
            #
            # self.buttons.append(
            #     Button(self.frames[-1], relief=FLAT, text=self.lang["slots.reset"], bg="#afafaf", width=7,
            #            font=[self.font, 15 + self.f_size]))
            # self.buttons.copy()[-1].place(x=450, y=175, anchor=SE)
            # self.buttons.copy()[-1].bind("<ButtonRelease-1>", self.reset_save)

            self.frames[-1].grid(row=i)

            i += 1

        if len(self.canvass) > 0:
            self.selectedCanv = self.canvass[0]

        self.infos = infos
        self.active = True
        while self.active:
            self.root.update()
            self.root.update_idletasks()

    def select(self, event):
        print("[SelectCanvas]: CLICK!")
        print("event.widget.__dict__: %s" % event.widget.__dict__)
        print("event.widget.master.grid_info(): %s" % event.widget.master.grid_info())

        y = event.widget.master.grid_info()["row"]
        print("[SelectCanvas]: Row %s" % y)

        if y != self.selected:
            self.canvass[self.selected].config(bg="#7f7f7f")
            self.canvass[y].config(bg="#4f4f4f")
            self.selected = y
            self.selectedCanv = event.widget

    @staticmethod
    def hasKey(_dict: dict, key):
        return True if key in _dict.keys() else False

    # noinspection PyUnusedLocal
    def reset_save(self, event):
        import os

        # Getting row-index.
        y = self.selected

        # Getting source dir.
        src = self.itemInfo[y]

        # Backups the old stats, for seed and high score.
        # noinspection PyUnresolvedReferences
        if self.selectedCanv.build < 16:
            stats_old = ConfigReader("slots/%s/game.json" % src).get_decoded()
        else:
            stats_old = Reader("slots/%s/game.data" % src).get_decoded()

        # Checks for the seed, if no seed it will be zero.
        if self.hasKey(stats_old, "seed"):
            seed = stats_old["seed"]
        else:
            seed = 0

        # Checks for the high score, if no high score it will be zero.
        if self.hasKey(stats_old, "hiscore"):
            hiscore = stats_old["hiscore"]
        else:
            hiscore = 0

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("slots/" + src)

        # Disabling the input and the button.
        # self.addInput.config(state=DISABLED)
        # self.saveAdd.config(state=DISABLED)

        # Getting the input text.
        if src in ("aux", "con", ".", ".."):
            return
        for i in "?<>:[]*&^%~":
            if i in src:
                return

        # Creating dir for the game.
        os.makedirs("slots/" + src, exist_ok=True)

        stats_data = {"coins": 0, "diamonds": 0, "level": 1, "level-score": 10000, "lives": 7, "score": 0,
                      "hiscore": hiscore,
                      "teleports": 0, "bubspeed": 5, "confusion": False, "confusion-time": 0, "notouch": False,
                      "notouch-time": 0,
                      "paralis": False, "paralis-time": 0, "scorestate": 1, "scorestate-time": 0, "secure": False,
                      "secure-time": 0, "shipspeed": 10, "shotspeed": 0.1, "shotspeed-time": 0, "slowmotion": False,
                      "slowmotion-time": 0, "special-level": False, "special-level-time": 0, "speedboost": False,
                      "speedboost-time": 0, "timebreak": False, "timebreak-time": 0, "ship-position": [960, 540],
                      "seed": seed, "x-update": 0}
        info_data = {"LastPlayedOn": {"build": self.gameBuild, "version": self.version, "version-dir": self.versionDir},
                     "seed": seed}
        bubbles_data = {"bub-id": list(), "bub-special": list(), "bub-action": list(), "bub-radius": list(),
                        "bub-speed": list(), "bub-position": list(), "bub-hardness": list(), "bub-index": list(),
                        "key-active": False}

        Writer("/slots/%s/game.data" % src, stats_data, "wb+")
        Writer("/slots/%s/bubble.data" % src, bubbles_data, "wb+")
        Writer("/slots/%s/info.data" % src, info_data, "wb+")

        # # Copy the template (resetted save-files)
        # self.copy("versions/" + self.launcherCfg["versionDir"] + "/config/reset.data", "slots/" + src + "/game.data")
        # self.copy("versions/" + self.launcherCfg["versionDir"] + "/config/reset-bubble.data",
        #           "slots/" + src + "/bubble.data")

        # Refreshing slots-menu
        self.delete_all()
        self.__init__(self.run, self.returnTitle)

    def checkLangItem(self, item, alt) -> str:
        return self.lang[item] if item in self.lang.keys() else alt

    def rename_menu(self):
        self.delete_all()

        # saveNameText = self.lang["add.savename"] if "add.savename" in self.lang.keys() else "Save Name"
        # addText = self.lang["add.add"] if "add.add" in self.lang.keys() else "Add"
        addSaveText = self.checkLangItem("rename.rename_name", "Rename")
        saveNameText = self.checkLangItem('add.savename', "Name")
        addText = self.checkLangItem("rename.rename", "Rename")
        cancelText = self.checkLangItem("add.cancel", "Cancel")
        self.canvasRenameSave = Frame(self.root, bg="#3c3c3c", bd=0, height=self.root.winfo_height(),
                                      width=self.root.winfo_width())
        self.cFrame = Frame(self.canvasRenameSave, bg="#3c3c3c", height=108, width=800)
        self.cFCanvas = Canvas(self.cFrame, bg="#3c3c3c", bd=0, highlightthickness=0)

        self.cFCanvas.create_text(5, 5, text=addSaveText, fill=self.accent.getColor(), anchor=NW, font=(self.font, 24))
        self.cFCanvas.create_text(5, 52, text=saveNameText, fill="#7f7f7f", anchor=NW, font=(self.font, 12))
        self.renameInput = Entry(self.cFrame, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT, font=(self.font, 11))
        self.renameInput.place(x=62, y=48, width=736)
        self.renameInput.insert(0, "Name")
        self.saveRename = Button(self.cFrame, text=addText, relief=FLAT, bg="#7f7f7f", fg="white",
                                 command=self.rename, font=[self.font, 15 + self.f_size])
        self.saveRename.place(x=231, y=78, width=168)
        self.saveRenameCancel = Button(self.cFrame, text=cancelText, relief=FLAT, bg="#7f7f7f", fg="white",
                                       command=self.delete_rename_menu, font=[self.font, 15 + self.f_size])
        self.saveRenameCancel.place(x=62, y=78, width=168)
        self.cFCanvas.pack(fill=X, expand=True)
        self.cFrame.place(x=int(self.root.winfo_width() / 2), y=int(self.root.winfo_height() / 2), anchor=CENTER)
        self.canvasRenameSave.pack(fill=BOTH, expand=True)
        self.root.update()

    def delete_rename_menu(self):
        self.saveRename.destroy()
        self.saveRenameCancel.destroy()
        self.cFCanvas.destroy()
        self.cFrame.destroy()
        self.canvasRenameSave.destroy()
        self.__init__(self.run, self.returnTitle)

    def add_save_menu(self):
        self.delete_all()

        # saveNameText = self.lang["add.savename"] if "add.savename" in self.lang.keys() else "Save Name"
        # addText = self.lang["add.add"] if "add.add" in self.lang.keys() else "Add"
        addSaveText = self.checkLangItem("add.addsave", "New Save")
        saveNameText = self.checkLangItem('add.savename', "Name")
        seedNameText = self.checkLangItem('add.seedname', "Seed")
        addText = self.checkLangItem("add.add", "Add")
        cancelText = self.checkLangItem("add.cancel", "Cancel")
        self.canvasAddSave = Frame(self.root, bg="#3c3c3c", bd=0, height=self.root.winfo_height(),
                                   width=self.root.winfo_width())
        self.cFrame = Frame(self.canvasAddSave, bg="#3c3c3c", height=300, width=800)
        self.cFCanvas = Canvas(self.cFrame, bg="#3c3c3c", bd=0, highlightthickness=0)

        self.cFCanvas.create_text(5, 5, text=addSaveText, fill=self.accent.getColor(), anchor=NW, font=(self.font, 24))
        self.cFCanvas.create_text(5, 52, text=saveNameText, fill="#7f7f7f", anchor=NW, font=(self.font, 12))
        self.cFCanvas.create_text(5, 82, text=seedNameText, fill="#7f7f7f", anchor=NW, font=(self.font, 12))
        self.saveInput = Entry(self.cFrame, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT, font=(self.font, 11))
        self.saveInput.place(x=62, y=48, width=736)
        self.saveInput.insert(0, "Name")
        self.seedInput = Entry(self.cFrame, bd=5, fg="#3c3c3c", bg="#7f7f7f", relief=FLAT, font=(self.font, 11))
        self.seedInput.place(x=62, y=78, width=736)
        self.seedInput.insert(0, "123456")
        self.saveAdd = Button(self.cFrame, text=addText, relief=FLAT, bg="#7f7f7f", fg="white",
                              command=self.add_save, font=[self.font, 15 + self.f_size])
        self.saveAdd.place(x=231, y=108, width=168)
        self.saveAddCancel = Button(self.cFrame, text=cancelText, relief=FLAT, bg="#7f7f7f", fg="white",
                                    command=self.delete_add_save_menu, font=[self.font, 15 + self.f_size])
        self.saveAddCancel.place(x=62, y=108, width=168)
        self.cFCanvas.pack(fill=X, expand=True)
        self.cFrame.place(x=int(self.root.winfo_width() / 2), y=int(self.root.winfo_height() / 2), anchor=CENTER)
        self.canvasAddSave.pack(fill=BOTH, expand=True)
        self.root.update()

    def delete_add_save_menu(self):
        self.cFCanvas.destroy()
        self.cFrame.destroy()
        self.canvasAddSave.destroy()
        self.__init__(self.run, self.returnTitle)

    def add_save(self) -> object:
        """
        Adding a slot to your game.
        :return object:
        """
        import os

        if len(os.listdir("slots/")) <= 4000:
            # Disabling the input and the button.
            self.saveInput.config(state=DISABLED)
            self.seedInput.config(state=DISABLED)
            self.saveAdd.config(state=DISABLED)
            self.saveAddCancel.config(state=DISABLED)

            # Getting the input text.
            new = self.saveInput.get()
            seed = self.seedInput.get()
            if seed.isnumeric():
                seed = int(seed)
            else:
                self.saveInput.config(state=NORMAL)
                self.seedInput.config(state=NORMAL)
                self.saveAdd.config(state=NORMAL)
                self.saveAddCancel.config(state=NORMAL)
                return
            if new in ("aux", "con", ".", ".."):
                return

            # Creating dir for the game.
            os.makedirs("slots/" + new, exist_ok=True)

            stats_data = {"coins": 0, "diamonds": 0, "level": 1, "level-score": 10000, "lives": 7, "score": 0,
                          "hiscore": 0,
                          "teleports": 0, "bubspeed": 5, "confusion": False, "confusion-time": 0, "notouch": False,
                          "notouch-time": 0,
                          "paralis": False, "paralis-time": 0, "scorestate": 1, "scorestate-time": 0, "secure": False,
                          "secure-time": 0, "shipspeed": 10, "shotspeed": 0.1, "shotspeed-time": 0, "slowmotion": False,
                          "slowmotion-time": 0, "special-level": False, "special-level-time": 0, "speedboost": False,
                          "speedboost-time": 0, "timebreak": False, "timebreak-time": 0, "ship-position": [960, 540],
                          "seed": seed, "x-update": 0}
            info_data = {"LastPlayedOn": {"build": self.gameBuild}}
            bubbles_data = {"bub-id": list(), "bub-special": list(), "bub-action": list(), "bub-radius": list(),
                            "bub-speed": list(), "bub-position": list(), "bub-hardness": list(), "bub-index": list(),
                            "key-active": False}

            Writer("slots/%s/game.data" % new, stats_data, "wb+")
            Writer("slots/%s/bubble.data" % new, bubbles_data, "wb+")
            Writer("slots/%s/info.data" % new, info_data, "wb+")

            # # Copy the template (resetted save-files)
            # self.copy("versions/" + self.launcherCfg["versionDir"] + "/config/reset.data",
            #           "slots/" + new + "/game.data")
            # self.copy("versions/" + self.launcherCfg["versionDir"] + "/config/reset-bubble.data",
            #           "slots/" + new + "/bubble.data")
            # Writer("slots/" + self.saveName + "/info.data",
            #        """{\n  "LastPlayedOn": {\n    "build": %s\n  }\n}""".encode() % self.gameBuild)

            # Refresh slots-menu
            self.delete_add_save_menu()

        # noinspection PyTypeChecker

    # noinspection PyUnusedLocal
    def remove(self, event) -> None:
        import os

        # Getting row-index.
        # y = event.widget.master.grid_info()["row"]
        y = self.selected

        # Getting source dir.
        src = self.itemInfo[y]

        # Removing the files inside.
        for i in os.listdir("slots/" + src):
            os.remove("slots/" + src + "/" + i)

        # Remove the slot (dir)
        os.removedirs("slots/" + src)

        # Refreshing slots-menu
        self.delete_all()
        self.__init__(self.run, self.returnTitle)

    def rename(self) -> None:
        import os

        # Getting row-index.
        # y = event.widget.master.grid_info()["row"]
        y = self.selected

        # Getting source dir.
        src = self.itemInfo[y]

        # Getting new name.
        new = self.renameInput.get()

        # noinspection PyTypeChecker
        # Rename the dir for the slot.
        os.rename("slots/" + src, "slots/" + new)

        # Refreshing slots-menu
        self.delete_rename_menu()

    def title_back(self):
        self.active = False
        sleep(0.1)
        self.destroy()
        self.returnTitle(self)

    def destroy(self) -> None:
        # Delete all main frames
        self.mainFrame.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame2a.destroy()
        self.frame3a.destroy()

    def delete_all(self):
        # Delete all main frames
        self.mainFrame.destroy()
        self.frame2.destroy()
        self.frame3.destroy()
        self.frame2a.destroy()
        self.frame3a.destroy()

    # noinspection PyUnusedLocal
    def open(self, event) -> None:
        # Getting row-index
        # y = event.widget.master.grid_info()["row"]
        if len(self.canvass) > 0:
            y = self.selected
            print("Running Save Index: %s " % y)

            # noinspection PyUnresolvedReferences
            build = self.selectedCanv.build

            # Getting source dir.
            src = self.itemInfo[y]

            # Remove slots menu and run the game.
            self.delete_all()
            self.run(src, build)
