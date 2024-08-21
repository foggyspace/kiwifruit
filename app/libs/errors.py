from typing import Any
from flask import request, json
from flask.ctx import AppContext
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

    def get_body(self, environ: Any = None) -> str:
        body = dict(
                msg=self.msg,
                error_code=self.error_code,
                request=request.method + ' ' + self.get_url_no_paramter()
            )
        text = json.dumps(body)
        return text

    def get_headers(self, environ:Any = None) -> list[tuple[str, str]]:
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_paramter():
        full_path = str(request.full_path)
        root_path = full_path.split('?')
        return root_path[0]


class Success(APIException):
    code = 200
    msg = 'success'
    error_code = 0


class Failed(APIException):
    code = 400
    msg = 'failed'
    error_code = 1


class AuthFailed(APIException):
    code = 401
    msg = 'auth failed'
    error_code = 2


class Forbidden(APIException):
    code = 401
    msg = 'forbidden'
    error_code = 3


class NotFound(APIException):
    code = 404
    msg = 'not found'
    error_code = 4


class ParameterError(APIException):
    code = 400
    msg = 'paramter error'
    error_code = 5


class InvalidTokenError(APIException):
    code = 401
    msg = 'invalid token error'
    error_code = 6


class ExpiredTokenError(APIException):
    code = 422
    msg = 'expirerd token error'
    error_code = 7

