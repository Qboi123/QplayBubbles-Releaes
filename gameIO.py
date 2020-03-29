import sys


def printerr(*text, sep=' ', end='\n'):
    print("ERROR: ", *text, sep=sep, end=end, file=sys.stderr)


def printwrn(*text, sep=' ', end='\n'):
    print("WARNING: ", *text, sep=sep, end=end, file=sys.stderr)
