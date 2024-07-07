from typing import Any
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code: Any = 500
    msg: str = 'server inernal error'
    error_code: int = 10010

    def __init__(self, msg: str | None = None, code:  None = None, error_code: int = 10086, headers: Any = None) -> None:
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ: None = None) -> str:
        body = dict(
                msg=self.msg,
                error_code=self.error_code,
                request=request.method + ' ' + self.get_url_no_paramter()
            )
        text = json.dumps(body)
        return text

    def get_headers(self, environ:None = None) -> list[tuple[str, str]]:
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_paramter():
        full_path = str(request.full_path)
        root_path = full_path.split('?')
        return root_path[0]
