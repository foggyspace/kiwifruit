from typing import Any

import requests
from requests.utils import get_encodings_from_content

from lib.core.logs import ERROR
from lib.core.data import conf as config, DEFAULT_METHOD


HEADERS = {
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0'
}


def request(url: str, **kwargs: Any):
    def check_charset(response):
        if response.encoding == 'ISO-8859-1':
            encoding = get_encodings_from_content(response.content)
            if encoding:
                response.encoding = encoding[0]
        return response

    kwargs.setdefault('headers',{})
    kwargs.setdefault('timeout',config.timeout)
    method = kwargs.pop('method') if kwargs.get('method') else DEFAULT_METHOD
    decode = kwargs.pop('decode') if kwargs.get('decode') else None
    if config.cookie:
        kwargs.setdefault('cookies',config.cookie)
    if method.upper() in ("GET","POST","options"):
        kwargs.setdefault('allow_redirects', True)
    else:
        kwargs.setdefault('allow_redirects', False)


    h = [ k.title() for k in kwargs['headers'].iterkeys() ]
    kwargs['headers'].update(dict( [ (k,v) for k,v in HEADERS.items() if k not in h ] ))
    try:
        response = requests.request(method,url,**kwargs)
        response = check_charset(response)
        if decode:
            _ = response.text
            #assert isinstance(_, unicode)
            try:
                _e = _.encode(decode)
            except UnicodeEncodeError:
                ERROR("encodePage error,charset:%s,url:%s" %(response.encoding,url))
                _e = _.encode(decode,'replace')
            #response.text = _e
            response._content = _e
        return response
    except Exception:
        ERROR("request exception,url:"+url)


def request_url(request: Any, payload: Any = None, **kwargs: Any):
    kwargs.setdefault('method', request.method)
    p = request.params if payload is None else payload
    if request.method == DEFAULT_METHOD:
        kwargs.setdefault('params', p)
    else:
        kwargs.setdefault('data', p)
    return request(request.url, **kwargs)
 
