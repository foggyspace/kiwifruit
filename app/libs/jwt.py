from functools import wraps

from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, create_access_token, create_refresh_token
from .errors import AuthFailed, InvalidTokenError, ExpiredTokenError


jwt = JWTManager()

identity = dict(uid=0, scop='admin')


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        __check_is_active(current_user=get_current_user())
        return f(*args, **kwargs)
    return wrapper


@jwt.expired_token_loader
def expired_token_loader_callback():
    return ExpiredTokenError()


@jwt.user_identity_loader
def user_identity_loader_callback(identity):
    return {
            'uuid': identity['uuid'],
            'scope': identity['scope']
    }


def generate_access_token(user, scope, expires_delta):
    identity['uuid'] = user.id
    identity['scope'] = scope
    access_token = create_access_token(identity=identity, expires_delta=expires_delta)
    return access_token


def __verify_token():
    from flask import request
    from flask_jwt_extended.config import config
    from flask_jwt_extended.view_decorators import _decode_jwt_from_cookies as decode


def __check_is_active(current_user):
    if not current_user.is_active:
        raise AuthFailed(msg='user is not active')
