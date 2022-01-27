import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    API_HOST = os.getenv('API_HOST', 'http://127.0.0.1')
    API_PORT = os.getenv('API_PORT', '5000')

    # Client Application Window Config
    TITLE = 'Doctors\' Surgery Client App'
    WIDTH = 800
    HEIGHT = 600

    # API config
    API_PREFIX = 'api'
    AUTH_API_LOGIN_RESOURCE_URL = 'auth/login'
    AUTH_API_LOGOUT_RESOURCE_URL = 'auth/logout'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
)

