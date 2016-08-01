import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_APP=app.py
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = ';\xc6w=]\xb8\x04\xad\x08\xc2\x97\xc9\x131\x91\xb44c$\x8b\xee\x8a\xb5('

class ProductionConfig(Config):
    DEBUG = False

class DevelopConfig(Config):
    DEBUG = True
    DEVELOPMENT = True


class TestingConfig(Config):
    TESTING = True

