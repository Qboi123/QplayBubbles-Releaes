import sys


def printerr(*text, sep=' ', end='\n'):
    print(*text, sep=sep, end=end, file=sys.stderr)
