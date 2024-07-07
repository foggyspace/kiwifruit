from app.libs.errors import APIException


class SuccessCode(APIException):
    code = 200
    msg = 'ok'
    error_code = 10000


class NotFoundCode(APIException):
    code = 404
    msg = 'not found'
    error_code = 10404


class AuthFailedCode(APIException):
    code = 401
    msg = 'auth failed'
    error_code = 10401


