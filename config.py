import os

from flask_dotenv import DotEnv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'not-so-secret')
    AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        env = DotEnv()
        env.init_app(app)

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
