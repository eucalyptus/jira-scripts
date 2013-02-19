# "import debugmode" to debug exceptions in your code!

import sys
import bdb
import traceback
try:
    import epdb as debugger
except ImportError:
    import pdb as debugger

def excepthook(typ, value, tb):
    if typ is bdb.BdbQuit:
        sys.exit(1)
    sys.excepthook = sys.__excepthook__

    debugger.post_mortem(tb, typ, value)
sys.excepthook = excepthook

