import gevent
from gevent import monkey
monkey.patch_socket()


ADDRESSES = ("127.0.0.1", 9527)


def send_request(name: str, headers: dict) -> None:
    sockfd = gevent._socket3.socket()
    sockfd.connect(ADDRESSES)
    headers["module"] = name
    h = [f"{k}:{v}" for k, v in headers.items()]
    h.append("\n")
    request = "\n".join(h)

    sockfd.send(request)
    sockfd.close()


