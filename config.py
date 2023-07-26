class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = '3b3533dacf63f08d6fa69d8e36c89cxx'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user:pass@localhost/dbname'


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
