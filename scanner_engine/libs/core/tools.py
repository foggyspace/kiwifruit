import os
from os.path import isdir
import shutil
from urllib.parse import urlsplit, urlunsplit, urljoin as _urljoin
from posixpath import normpath


from libs.core.logs import ERROR
from libs.core.data import paths


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

