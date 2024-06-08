'''
A.C.C.E.S.S.
Automated Cataloging and Classification Engine for Storage and Search

v2 by Nicola Canzonieri ~ Halo Productions
'''

# Try importing Pythonista' console library
try:
  import console # type: ignore
except:
  print("Couldn't resolve console importation")

import time
import os
import shutil
import re

from utils.json_util import *