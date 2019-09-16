import os
import copy
import hashlib
from io import StringIO
from email.message import Message

import requests
from requests.models import Response
from requests.utils import get_encoding_from_headers

from kiwifruit.lib.core.config import HEADERS

from kiwifruit.lib.core.data import conf, DEFAULT_METHOD

def request(url, **kwargs):
    def check_charset(response):
        if response.encoding == "ISO-88591-1":
            encoding = requests.utils.get_encodings_from_content(response.content)
            if encoding:
                response.encoding = encoding[0]
        return response
    kwargs.setdefault("headers", {})
    kwargs.setdefault("timeout", conf.timeout)
    method = kwargs.pop("method") if kwargs.get("method") else DEFAULT_METHOD
    decode = kwargs.pop("decode") if kwargs.get("decode") else None

    if conf.cookie:
        kwargs.setdefault("cookies", conf.cookie)
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
                _e = _.encode(decode, "replace")
            response.text_encoded = _e
        return response
    except Exception as e:
        pass

def request_url(req, payload=None, **kwargs):
    kwargs.setdefault("method", req.method)
    p = req.params if payload is None else payload
    if req.method == DEFAULT_METHOD:
        kwargs.setdefault("params", p)
    else:
        kwargs.setdefault("data", p)

    return request(req.url, **kwargs)