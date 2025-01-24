class BaseConfig(object):
    MODE = False
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    JWT_SECRET_KEY = 'jwt-secret-key-here'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时


class Developments(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.db'
    SQLALCHEMY_ECHO = True


class Productions(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/kiwifruit'
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20


class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    WTF_CSRF_ENABLED = False


configs = {
        'dev': Developments(),
        'prod': Productions(),
        'test': TestConfig(),
}
