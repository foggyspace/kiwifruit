import json
from urllib.parse import urlparse

import gevent
from gevent import monkey
monkey.patch_socket()


ADDRESSES = ("127.0.0.1", 9527)


def dispatch_request(module_name, request_header):
    try:
        socket = gevent._socket3.socket()
        socket.connect(ADDRESSES)

        request_header["module"] = module_name

        h = [f"{k}:{v}" for k, v in request_header.items()]
        h.append('\n')
        request = '\n'.join(h)

        socket.send(request)
        content = socket.recv(8192)
        socket.close()
        return json.loads(content)
    except Exception:
        return {"success": False, "message": "send request error."}

