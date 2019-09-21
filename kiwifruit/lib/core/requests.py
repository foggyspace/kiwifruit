import os
import hashlib
from io import StringIO
from email.message import Message

import requests
from requests.models import Response
from requests.utils import get_encoding_from_headers

from kiwifruit.lib.core.config import HEADERS, HEADER_BODY_BOUNDRY
from kiwifruit.lib.core.log import ERROR

from kiwifruit.lib.core.data import conf, DEFAULT_METHOD


def request_url(req, payload=None, **kwargs):
    kwargs.setdefault("method", req.method)
    p = req.params if payload is None else payload
    if req.method == DEFAULT_METHOD:
        kwargs.setdefault("params", p)
    else:
        kwargs.setdefault("data", p)

    return request(req.url, **kwargs)


def cache_file_name(url, method, kw):
    _ = '*'.join((url, method, str(kw)))
    return os.path.join(conf.requestCache, hashlib.md5(_).hexdigest())


class FileResponse(object):
    def __init__(self, filename, url, method, **kwargs):
        self.filename = filename
        self.url = url
        self.method = method
        self.kwargs = kwargs

    def load(self):
        buffer = None
        with open(self.filename, "r") as fs:
            buffer = StringIO(fs.read())

        if not buffer:
            return None

        version, status, reason = buffer.readlines().split(' ', 2)
        headers = Message(buffer).dict

        response = Response()

        response.status_code = int(status)

        response.headers = headers

        response.encoding = get_encoding_from_headers(response.headers)

        response.raw = buffer

        response.reason = reason

        if isinstance(self.url, str):
            response.url = self.url

        return response

    def store(self, response):
        r = response
        def headers():
            status_line = f"HTTP/1.1{r.status_code},{r.reason}"
            headers = [f"{k}: {v}" for k, v in r.headers.items()]
            return '\n'.join((status_line, '\n'.join(headers)))
        buffer = '\n'.join((headers(), HEADER_BODY_BOUNDRY, r.content))

        with open(self.filename, "w") as fs:
            fs.write(buffer)


def request(url, **kwargs):
    def check_charset(response):
        if response.encoding == "ISO-8859-1":
            encoding = requests.utils.get_encodings_from_content(response.content)
            if encoding:
                response.encoding = encoding[0]
        return response

    kwargs.setdefault('headers', {})
    kwargs.setdefault('timeout', conf.timeout)
    method = kwargs.pop('method') if kwargs.get('method') else DEFAULT_METHOD
    decode = kwargs.pop('decode') if kwargs.get('decode') else None

    if conf.cookie:
        kwargs.setdefault('cookies', conf.cookie)

    if method.upper() in ("GET", "POST", "options"):
        kwargs.setdefault("allow_redirects", True)
    else:
        kwargs.setdefault("allow_redirects", False)

    h = [k.title() for k in kwargs["headers"].keys()]
    kwargs["headers"].update(dict([(k, v) for k, v in HEADERS.items() if k not in h]))

    try:
        response = requests.request(method, url, **kwargs)
        response = check_charset(response)
        if decode:
            _ = response.text
            assert isinstance(_, str)
            try:
                _e = _.encode(decode)
            except UnicodeEncodeError:
                ERROR(f"encodePage error, charset: {response.encoding} : {url}")
                _e = _.encode(decode, "replace")
            response.text_encoded = _e
        return response
    except Exception as e:
        ERROR(f"request exception {e} => url: {url}")
