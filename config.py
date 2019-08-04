import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    UPLOAD_FOLDER = '/tmp/'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    SECRET_KEY = "\xfd4\xa4\x08\xee,G\x92\x18c\x16\x94\xaaw\xdb\x0c\xe4\x13s \x8f'\x00/"
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
