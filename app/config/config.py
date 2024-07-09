class BaseConfig(object):
    MODE = False


class Developments(BaseConfig):
    pass


class Productions(BaseConfig):
    pass


class TestConfig(BaseConfig):
    pass


configs = {
        'dev': Productions(),
        'prod': Developments(),
        'test': TestConfig(),
}
