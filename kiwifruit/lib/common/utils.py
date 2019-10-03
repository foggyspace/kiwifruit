import os
import shutil
from urllib.parse import urlsplit, urlunsplit, urljoin as _urljoin
from posixpath import normpath
from datetime import datetime

from kiwifruit.lib.core.log import ERROR
from kiwifruit.lib.core.data import paths, conf
from kiwifruit.lib.core.config import IGNORE_DEFAULT_FILE_SUFFIX


def urljoin(base, url, allow_fragments=True):
    """
    连接url
    :param base:
    :param url:
    :param allow_fragments:
    :return:
    """
    _ = _urljoin(base, url, allow_fragments=True)
    p = urlsplit(_)
    path = p.path + '/' if p.path.endswith('/') else p.path
    return urlunsplit((p.scheme, p.netloc, normpath(p.path), p.query, p.fragment))


def show_paths():
    """
    输出路径
    :return:
    """
    return paths


def mkdir(path, remove=True):
    """
    创建目录
    :param path: 目录路径
    :param remove: 一个标致符号
    :return:
    """
    if os.path.isdir(path):
        if remove:
            try:
                shutil.rmtree(path)
                os.mkdir(path)
            except Exception:
                ERROR("[-] rm tree exception path" + path)
    else:
        os.mkdir(path)


def discard(url):
    """
    过滤文件扩展名
    :param url: 待检测的url
    :return: 布尔值
    """
    index = url.rfind('.')
    if index != -1 and url[index+1:] in IGNORE_DEFAULT_FILE_SUFFIX:
        return True
    return False


def set_unreachable_flag(task_id):
    """
    更新reachable
    :param task_id: 任务id
    :return:
    """
    sql_statement = "UPDATE task SET `reachable`=0 WHERE id=%s" % task_id
    try:
        db.execute(sql_statement)
    except Exception:
        ERROR("[-] set unreachable failed task_id : %s, please check" % task_id)


def update_task_status(task_id):
    """
    更新任务状态
    :param task_id: 任务id
    :return:
    """
    sql_statement = "UPDATE task SET `status`=3 WHERE id=%s" % task_id
    try:
        db.execute(sql_statement)
    except Exception:
        ERROR("[-] update task status failed task_id : %s" % task_id)


def update_task_time(task_id):
    """
    更新任务时间
    :param task_id: 任务id
    :return:
    """
    sql_statement = "UPDATE task SET `end_time`=%s WHERE id=%s"
    try:
        db.execute(sql_statement, datetime.now(), task_id)
    except Exception:
        ERROR("[-] update end time failed task_id : %s, please check" % task_id)


def task_finish_clean(task_id=None):
    """
    任务完成做一些清理更新的操作
    :param task_id:
    :return:
    """
    if task_id is None:
        task_id = conf.taskid
    update_task_status(task_id)
    update_task_time(task_id)

