import os
import sys
from lib.core.settings import PLUGIN_RULES, SCRIPTS_DIC_NAME, TEMP_NAME, LOG_NAME
from lib.core.data import paths

def rootPath(path=__file__):
    return os.path.dirname(path)

def setPaths():
    _ = paths.ROOT_PATH
    paths.SCRIPTS = os.path.join(_, PLUGIN_RULES)
    paths.FIlELOG = os.path.join(_, LOG_NAME)
    paths.TEMP = os.path.join(_, TEMP_NAME)
    paths.DIC = os.path.join(paths.SCRIPTS, SCRIPTS_DIC_NAME)

def envinit(path):
    paths.ROOT_PATH = rootPath(path)
    setPaths()
