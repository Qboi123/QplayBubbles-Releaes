#!/usr/bin/env python

"""
oldoldsetup.py  to build mandelbot code with cython
"""
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import *
import threadsafe_tkinter, tkinter, os, json, time, math, sys, random, winsound, tkinter.ttk # to get includes


setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("Qplay Bubbles", ["main.py", 'ammo.py', 'bubble.py', 'components.py', 'config.py',
                                             'extras.py', 'info.py', 'state.py', 'teleport.py'], )],
    include_dirs=["config", "assets", "logs", "saves"],
    requires=['pygame', 'tkinter', 'threadsafe_tkinter', 'tkinter.ttk', 'os', 'json', 'sys', 'random', 'math', 'windound']
)
