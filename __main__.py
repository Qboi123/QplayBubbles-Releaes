import sys
import os

from qbubbles.__main__ import Main


if __name__ == '__main__':
    sys.path.insert(0, os.path.split(__file__)[0])
    main = Main()
    main.mainloop()
