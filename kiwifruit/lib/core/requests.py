import os
import copy
import hashlib

from io import StringIO
from mimetools import Message

import requests
from requests.models import Response
from requests.utils import get_encoding_from_headers

from lib.core.log import ERROR, DEBUG, INFO
from lib.core.data import conf, paths, DEFAULT_METHOD

from lib.core.settings import DEFAULT_PAGE_ENDCODING, HEADER_BODY_BOUNDRY


HEADERS = {
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0"
}


def cach_file_name(url, method, kw):
    _ = "*".join((url, method, str(kw)))
    return os.path.join(conf.requestCache, hashlib.md5(_).hexdigest())


class FileResponse(object):
    def __init__(self, filename, url, method, **kwargs):
        self.filename = filename
        self.url = url
        self.method = method
        self.kwargs = kwargs

    def load(self):
        buff = None
        with open(self.filename, "r") as fs:
            buff = StringIO(fs.read())
        if not buff:
            return None
        version, status, reason = buff.readline().split(" ", 2)
        headers = Message(buff).dict
        response = Response()

        response.status_code = int(status)
        response.headers = headers
        response.encoding = get_encoding_from_headers(response.headers)
        response.raw = buff
        response.reason = reason

        if isinstance(self.url, str):
            response.url = self.url.decode("utf-8")
        else:
            response.url = self.url

        return response

    def store(self, response):
        r = response
        def headers():
            status_line = f"HTTP/1.1 {r.status_code} {r.reason}"
            headers = [f"{k}: {v}" for k, v in r.headers.items()]
            return "\n".join((status_line, "\n".join(headers)))
        buff = "\n".join((headers(), HEADER_BODY_BOUNDRY, r.content))
        with open(self.filename, "w") as fs:
            fs.write(buff)


def request(url, **kwargs):
    def check_charset(response):
        if response.encoding == "ISO-8859-1":
            encoding = request.utils.get_encoding_from_headers(response.content)
            if encoding:
                response.encoding = encoding[0]
        return response

    kwargs.setdefault("headers", {})
    kwargs.setdefault("timeout", conf.timeout)
    method = kwargs.pop("method") if "method" in kwargs else DEFAULT_METHOD
    decode = kwargs.pop("decode") if "decode" in kwargs else None
    if conf.cookie:
        kwargs.setdefault("cookies", conf.cookie)
    if method.upper() in ("GET", "POST", "options"):
        kwargs.setdefault("allow_redirects", True)
    else:
        kwargs.setdefault("allow_redirects", False)

    h = [k.title() for k in kwargs["headers"].keys()]
    kwargs["headers"].update(dict([(k, v) for k, v in HEADERS.items() if k not
                                  in h]))
    try:
        response = requests.get(method, url, **kwargs)
        response = check_charset(response)
        if decode:
            _ = response.text
            assert isinstance(_, str)
            try:
                _e = _.encode(decode)
            except UnicodeEncodeError:
                ERROR(f"encodePage error, charset: {response.encoding} , url :
                      {url}")
                _e = _.encode(decode, "replace")
            response.text_encoded = _e
        return response
    except Exception as e:
        ERROR(f"request exception url : {url}")


def requests_url(req, payload=None, **kwargs):
    kwargs.setdefault("method", req.method)
    p = req.params if payload is None else payload
    if req.method == DEFAULT_METHOD:
        kwargs.setdefault("params", p)
    else:
        kwargs.setdefault("data", p)
    return request(req.url, **kwargs)

