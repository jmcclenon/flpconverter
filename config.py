class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'this-should-be-changed'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/dbname'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
