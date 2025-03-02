from typing import Any, Optional
from flask import request, json
from werkzeug.exceptions import HTTPException
from app.libs.error_codes import ErrorCode


class APIException(HTTPException):
    code: int = 500
    msg: str = 'server internal error'
    error_code: int = 10010

    def __init__(self, error_code: ErrorCode = None, msg: Optional[str] = None, code: Optional[int] = None, headers: Any = None, lang: str = 'zh') -> None:
        if error_code:
            self.code = error_code.http_code
            self.error_code = error_code.error_code
            self.msg = error_code.zh_msg if lang == 'zh' else error_code.en_msg
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ: Any = None, scope: Any = None) -> str:
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_parameter()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ: Any = None, scope: Any = None) -> list[tuple[str, str]]:
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_parameter() -> str:
        full_path = str(request.full_path)
        root_path = full_path.split('?')
        return root_path[0]


class Success(APIException):
    def __init__(self, msg: Optional[str] = None, data: Any = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.SUCCESS, msg=msg, headers=headers, lang=lang)
        self.data = data

    def get_body(self, environ: Any = None, scope: Any = None) -> str:
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_parameter()
        )
        if self.data is not None:
            body['data'] = self.data
        text = json.dumps(body)
        return text


class Failed(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.FAILED, msg=msg, headers=headers, lang=lang)


class AuthFailed(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.AUTH_FAILED, msg=msg, headers=headers, lang=lang)


class Forbidden(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.FORBIDDEN, msg=msg, headers=headers, lang=lang)


class NotFound(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.NOT_FOUND, msg=msg, headers=headers, lang=lang)


class ParameterError(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.PARAMETER_ERROR, msg=msg, headers=headers, lang=lang)


class InvalidTokenError(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.INVALID_TOKEN, msg=msg, headers=headers, lang=lang)


class ExpiredTokenError(APIException):
    def __init__(self, msg: Optional[str] = None, headers: Any = None, lang: str = 'zh') -> None:
        super().__init__(error_code=ErrorCode.EXPIRED_TOKEN, msg=msg, headers=headers, lang=lang)

