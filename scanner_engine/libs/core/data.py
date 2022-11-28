import re
from collections import namedtuple
from typing import Any


GET, POST = "GET", "POST"

DEFAULT_METHOD = "GET"

TITLE_PATTERN_RE = re.compile(r"<title>(?P<title>[^<]+)</title>", re.I)

PARAMS_PATTERN = re.compile(r"(?P<key>[^&=]+)(?:=(?P<value>[^&=]*))?")


SITETYPES = {'PHP':'.php', 'JSP':'.jsp', 'ASP.NET':'.asp', 'ASP':'.asp'}


class ObjectDict(dict):
    def __getattr__(self, name: str) -> None:
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value


class Url(object):
    def __init__(self, url: str, method: str, params: Any, referer: Any) -> None:
        self.url = url
        self.method = method
        self.params = params
        self.referer = referer

    @classmethod
    def from_url(cls, url: str, referer: str = "") -> Any:
        url, params = url.split("?", 1) if url.find("?") != -1 else (url, "")
        return cls(url, DEFAULT_METHOD, params, referer)

    @property
    def name(self):
        return self.__class__.__name__

    def __str__(self) -> str:
        return f"<{self.name} - {self.method} - {self.url}, {self.params} - {self.referer}>"

    __repr__ = __str__


paths = ObjectDict()

cmdOptions = ObjectDict()

config = ObjectDict()

Result = namedtuple("Result", "response details")

