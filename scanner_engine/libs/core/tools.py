import os
from os.path import isdir
import shutil
from urllib.parse import urlsplit, urlunsplit, urljoin as _urljoin
from posixpath import normpath
from datetime import datetime


from libs.core.logs import ERROR
from libs.core.data import paths, config
from libs.core.settings import IGNORE_DEFAULT_FILE_SUFFIX
from libs.utils import db


def urljoin(base: str, url: str, allow_fragments: bool = True) -> str:
    _ = _urljoin(base, url, allow_fragments)
    p = urlsplit(_)
    path = p.path + "/" if p.path.endswith("/") else p.path
    return urlunsplit((p.scheme, p.netloc, normpath(path), p.query, p.fragment))


def show_paths():
    print(paths)


def mkdir(path: str, remove: bool = True):
    if isdir(path):
        if remove:
            try:
                shutil.rmtree(path)
                os.mkdir(path)
            except Exception:
                ERROR("rmtree except, path : " + path)
    else:
        os.mkdir(path)

def discard(url):
    index = url.rfind('.')
    if index != -1 and url[index+1:] in IGNORE_DEFAULT_FILE_SUFFIX:
        return True
    return False


def set_unreachable_flag(task_id):
    sql = "UPDATE task SET `reachable`=0 WHERE id=%s" % task_id
    try:
        db.execute(sql)
    except Exception:
        ERROR('set_unreachable failed,task_id:%s,please check' % task_id)

def update_task_status(task_id):
    sql = "UPDATE task SET `status`=3 WHERE id=%s" % task_id
    try:
        db.execute(sql)
    except Exception:
        ERROR('update_task_status failed,task_id:%s,please check' % task_id)

def update_end_time(task_id):
    sql = "UPDATE task SET `end_time`=%s WHERE id=%s"
    try: 
        db.execute(sql, datetime.now(), task_id)
    except Exception:
        ERROR('update_end_time failed,task_id:%s,please check' % task_id)


def task_finsh_clean(task_id=None):
    if task_id is None:
        task_id = config.taskid

    update_task_status(task_id)
    update_end_time(task_id)
