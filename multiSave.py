import tkinter as tk
import tkinter.ttk as ttk


class Logging:
    def __init__(self, save_dir):
        self.save_dir = save_dir

    def _log_(self, info, args):
        import time
        info = str(info)
        text = ""
        for item in args:
            text += "["+str(item)+"] "
        print("["+time.strftime("%d-%m-%Y - %H:%M:%S", time.localtime(time.time()))+"] "+text+"- "+info)

    def log(self, info, *args):
        import threading as thread
        thread.Thread(None, lambda: self._log_(info, args)).start()


class Main(Logging):
    def __init__(self, save_dir, start_path=None):
        super().__init__(save_dir)

        if start_path:
            self.path = start_path
        else:
            self.path = "C:\\"

        self.items = []
        self.item_info = [[[]]]
        self.max_pages = 0
        self.frames = []
        self.root = tk.Tk()
        self.root.wm_attributes("-fullscreen", True)
        # self.back = ttk.Button(self.root, text="Up", command=lambda: self.dir_up())
        # self.back.pack(side=tk.TOP)
        self.tabs = ttk.Notebook(self.root)
        self.refresh_explorer()
        self.root.mainloop()

    def dir_up(self):
        import os
        paths = self.path.split(sep="\\")
        a = ""
        for item in paths[0:-1]:
            a = os.path.join(a, item)
        print(paths[0:-1])
        print(len(paths))
        if len(paths) == 1:
            a = "/"
        elif len(paths) == 2:
            print(paths[0])
            if paths[0] == "":
                a = "/"
        print(a)
        self.path = a
        self.refresh_explorer()

    def delete_all(self):
        for i in range(len(self.items)-1, -1, -1):
            self.items[i].destroy()
            del self.items[i]
        self.tabs.destroy()

    def open_dir(self, event):
        import os

        print(event.widget.grid_info())
        x = event.widget.grid_info()["column"]
        y = event.widget.grid_info()["row"]
        print(self.tabs.grab_current())

        p = self.tabs.index("current")

        if p > 0 or x > 0:
            y -= 1

        print(p, x, y)
        print(self.item_info)

        dir = self.item_info[p][0][x][y]

        print(tk.Radiobutton())
        self.log("Open dir")
        for item in self.items:
            print(tk.Radiobutton(self.root))
        self.path = os.path.join(self.path, dir)
        self.refresh_explorer()

    def on_tab_changed(self, event):
        str(event.widget.index("current") + 1)

    def refresh_explorer(self):
        self.delete_all()
        self.tabs = ttk.Notebook(self.root)
        width = 7
        height = 30

        dirs, files, execs = self.read_dir()

        y = -1
        x = 0
        p = 0
        i = 0
        self.item_info = [[[[]]]]
        self.frames.append(tk.Frame(self.tabs, bg="#3c3c3c"))
        items2 = []
        while i < len(dirs):
            y += 1
            self.item_info[p][0][x].append(dirs[i])
            if y >= height:
                y = 0
                self.item_info[p][0].append([])
                x += 1
            if x > width:
                self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
                self.log("Append tab")
                self.frames.append(tk.Frame(self.tabs, bg="#3c3c3c"))
                y = 0
                x = 0
                self.item_info.append([[[]]])
                p += 1
            items2.append(dirs[i])
            b = None

            self.log("Page=" + str(p) + "| x=" + str(x) + "| y=" + str(y) + "| i=" + str(i) + "| Len Dirs=" + str(
                len(dirs) - 1),
                     "Main", "RefreshExplorer")
            # print(len(self.item_info)-1, len(self.item_info[p]), len(self.item_info[p][x]), len(self.item_info[p][x][y]))

            self.frames2.append(tk.Frame(self.frames[-1], bg="#3c3c3c", bd=2, relief=tk.RAISED))
            self.items.append(tk.Button(self.frames[-1], width=30, relief=tk.FLAT, text="<"+dirs[i]+">", bg="#707070"))
            self.log("Append Item: "+dirs[i], "Main", "RefreshExplorer")
            self.items.copy()[-1].grid(column=x, row=y)
            self.items.copy()[-1].bind("<ButtonRelease-1>", self.open_dir)
            self.max_pages = p
            i += 1

        self.tabs.add(self.frames.copy()[-1], text=' {} '.format(p))
        self.log("Append tab")
        self.tabs.enable_traversal()
        self.tabs.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self.root.update()

    def read_dir(self):
        import os
        self.log("self.path = "+self.path, "Main")
        index = os.listdir(self.path)
        dirs = []
        files = []
        execs = []

        for item in index:
            file_path = os.path.join(self.path, item)

            if os.path.isdir(file_path):
                self.log("Reading Dir Info, " + str(file_path), "Main", "ReadDir")
                dirs.append(item)
                execs.append(self.open_dir)
            elif os.path.isfile(file_path):
                self.log("Reading File Info, " + str(file_path), "Main", "ReadDir")
                files.append(item)
            else:
                files += file_path
        self.log("Returning Dirs: "+str(dirs))
        self.log("Returning Files: "+str(files))
        return dirs, files, execs


if __name__ == "__main__":
    Main("logs")
