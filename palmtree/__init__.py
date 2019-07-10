
# encoding: utf-8

# =========================================
#       IMPORTS / EXPORTS
# --------------------------------------

import sys

if sys.version_info[0] < 3:
    raise ImportError('Python 3 is required for `palmtree` - Python 2 is not supported anymore.')

from palmtree.tree import *
