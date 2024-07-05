import re


DOMAIN_PAHT = re.compile(r"^(?P<domain>.+//[^/]+)(?P<path>.*)$")
ROBOTS_ALLOW_PATH = re.compile(r"allow\s*:\s*(?P<path>[^*]+).*$",re.I)
SITEMAP_URL = re.compile(r"(?P<url>http[^<>]+)")


def pipeline(request):
    pass


def unique(value, stripchars):
    _ = []
    v = not not stripchars
    for t in value :
        if t not in _[-1:] or (v and t not in stripchars):
            _.append(t)
    return "".join(_)



class CrawlerSpider(object):
    def __init__(self) -> None:
        pass
