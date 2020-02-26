import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    APP_NAME = 'ravenscout'
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    SQLALCHEMY_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATICATIONS = False
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    PRODUCTION = True

config = {
    'development' : DevelopmentConfig,
    'testing' : TestConfig,
    'production' : ProductionConfig,
    'default' : DevelopmentConfig
}