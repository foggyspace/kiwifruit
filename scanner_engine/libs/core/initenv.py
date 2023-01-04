import os
import sys
from libs.core.settings import SCRIPTS_NAME, SCRIPTS_DIC_NAME, TEMP_NAME, LOG_NAME
from libs.core.data import paths

def rootPath(path=__file__):
    return os.path.dirname(unicode(sys.executable if hasattr(sys,"frozen") else path,sys.getfilesystemencoding()))

def setPaths():
    _ = paths.ROOT_PATH
    paths.SCRIPTS = os.path.join(_, SCRIPTS_NAME)
    paths.FIlELOG = os.path.join(_, LOG_NAME)
    paths.TEMP = os.path.join(_, TEMP_NAME)
    paths.DIC = os.path.join(paths.SCRIPTS, SCRIPTS_DIC_NAME)

def envinit(path):
    paths.ROOT_PATH = rootPath(path)
    setPaths()




