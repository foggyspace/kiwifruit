import os
import sys

from kiwifruit.lib.core.config import SCRIPTS_NAME, SCRIPTS_DIC_NAME, TEMP_NAME, LOG_NAME
from kiwifruit.lib.core.data import paths


def root_path(path=__file__):
    return os.path.dirname(str(sys.executable if hasattr(sys, "frozen") else path, sys.getfilesystemencoding()))


def set_paths():
    _ = paths.ROOT_PATH
    paths.SCRIPTS = os.path.join(_, SCRIPTS_NAME)
    paths.FILELOG = os.path.join(_, LOG_NAME)
    paths.TEMP = os.path.join(_, TEMP_NAME)
    paths.DIC = os.path.join(paths.SCRIPTS, SCRIPTS_DIC_NAME)


def envinit(path):
    paths.ROOT_PATH = root_path(path)
    set_paths()

