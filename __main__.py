import io
from typing import *


# noinspection PyShadowingNames
class Game(object):
    def __init__(self, launcher_cfg):
        from . import lib as main

        print(launcher_cfg["launcher"].all)
        exit(0)

        launcher_cfg["build"] = None

        main.Game(launcher_cfg)


class Log(io.IOBase):
    def __init__(self, file, std, name="Out"):
        self.file = file
        self.std = std
        self.name = name
        self.old = "\n"
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def write(self, o: str):
        l = o.splitlines(True)
        for i in l:
            if self.old[-1] == "\n":
                self.std.write("[" + time.ctime(time.time()) + "] [" + self.name + "]: " + i)
                self.fp = open(self.file, "a+")
                self.fp.write("[" + time.ctime(time.time()) + "] [" + self.name + "]: " + i)
                self.fp.close()
            else:
                self.std.write(i)
                self.fp = open(self.file, "a+")
                self.fp.write(i)
                self.fp.close()
            self.old = i

    def writelines(self, lines: Iterable[Union[bytes, bytearray]]) -> None:
        for line in lines:
            self.write(line)

    def potato(self, exefile):
        self.write(exefile)
        self.flush()

    def flush(self):
        pass

    def fileno(self):
        self.fp = open(self.file, "a+")
        return self.fp.fileno()

    def read(self):
        import time
        self.std.write("[{time}] [In]: ".format(time=time.ctime(time.time())))

        a = self.std.read()
        self.fp = open(self.file, "a+")
        self.fp.write("[{time}] [In]: ".format(time=time.ctime(time.time())) + a)
        self.fp.close()


if __name__ == "__main__":
    import sys
    import os
    import time

    startup = time.time()
    startup2 = time.ctime(startup).replace(" ", "-").replace(":", ".")

    if not os.path.exists("../../logs"):
        os.makedirs("../../logs")

    if not os.path.exists("../../logs"):
        os.makedirs("../../logs")

    log_file = time.strftime("%M-%d-%Y %H.%M.%S.log", time.gmtime(startup))

    stderr = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stderr__, "Err")
    stdout = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "Out")
    stdin = Log(os.getcwd().replace("\\", "/") + "/logs/" + log_file, sys.__stdout__, "In")

    sys.stderr = stderr
    sys.stdout = stdout
    sys.stdin = stdin
    print("Args:", sys.argv)

    launcher_cfg = {"version": sys.argv[1],
                    "versionDir": sys.argv[2],
                    "build": int(sys.argv[3]),
                    "file": sys.argv[0],
                    "debug": False
                    }

    if "--debug" in sys.argv:
        launcher_cfg["debug"] = True

    main_path = os.path.abspath(os.path.join(os.getcwd().replace("\\", "/"), "../../"))
    print("Launcher Path: %s" % main_path)

    sys.path.append(main_path)

    if not launcher_cfg["debug"]:
        os.chdir("../../")

    from lib import Main
    Main.Game(launcher_cfg)
