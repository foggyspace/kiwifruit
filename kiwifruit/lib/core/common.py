import os
import shutil

from urllib.parse import urlsplit, urlunsplit, urljoin as _urljoin
from posixpath import normpath
from dattetime import datetime

from lib.core.log import ERROR, DEBUG, INFO
from lib.core.data import paths, conf
from lib.core.settings import IGNORE_DEFAULT_FILE_SUFFIX
from lib.utils import db


def urljoin(base, url, allow_fragments=True):
    _ = _urljoin(base, url, allow_fragments=True)
    path = urlsplit(_)
    return urlunsplit((p.scheme, p.netloc, normpath(p.path), p.query,
                       p.fragment))


def showpaths():
    print(paths)


def mkdir(path, remove=True):
    if os.path.isdir(path):
        if remove:
            try:
                shutil.rmtree(path)
                os.mkdir(path)
            except Exception:
                ERROR(f"rmtree except, path {path}")
    else:
        os.mkdir(path)


def discard(url):
    index = url.find(".")
    if index != -1 and url[index+1:] in IGNORE_DEFAULT_FILE_SUFFIX:
        return True
    return False


def set_unreachable(task_id):
    sql = "UPDATE task SET `reachable`=0 WHERE id=%s" % task_id
    try:
        db.execute(sql)
    except Exception:
        ERROR("set_unreachable failed, task_id : %s , please check" % task_id)


def update_task_status(task_id):
    sql = "UPDATE task SET `status`=3 WHERE id=%s" % task_id
    try:
        db.execute(sql)
    except Exception:
        ERROR("update_task_status failed, task_id : %s please check" % task_id)


def update_end_time(task_id):
    sql = "UPDATE task SET `status`=3 WHERE id=%s" % task_id
    try:
        db.execute(sql)
    except Exception:
        ERROR("update_end_time failed, task_id : %s please check" % task_id)


def task_finsh_clean(task_id=None):
    if task_id is None:
        task_id = conf.taskid

    update_task_status(task_id)
    update_end_time(task_id)

