from functools import wraps
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_current_user, create_access_token, create_refresh_token, get_jwt
from .errors import AuthFailed, InvalidTokenError, ExpiredTokenError

jwt = JWTManager()
blacklist = set()

def require_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            __check_is_active(current_user)
            if current_user.get('scope') != access_level:
                raise AuthFailed(msg='insufficient permissions')
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        token = get_jwt()
        if token['jti'] in blacklist:
            raise InvalidTokenError(msg='Token has been revoked')
        __check_is_active(current_user=get_current_user())
        return f(*args, **kwargs)
    return wrapper

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

@jwt.expired_token_loader
def expired_token_loader_callback():
    return ExpiredTokenError()

@jwt.user_identity_loader
def user_identity_loader_callback(identity):
    return {
            'uuid': identity['uuid'],
            'scope': identity['scope']
    }

def generate_access_token(user, scope, expires_delta=None):
    if not expires_delta:
        expires_delta = timedelta(minutes=30)
    identity = {
        'uuid': user.id,
        'scope': scope
    }
    access_token = create_access_token(identity=identity, expires_delta=expires_delta)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token

def revoke_token(jti):
    blacklist.add(jti)

def __check_is_active(current_user):
    if not current_user or not current_user.get('is_active'):
        raise AuthFailed(msg='user is not active')

# 为了向后兼容，添加generate_token作为generate_access_token的别名
generate_token = generate_access_token
