import os

from flask_dotenv import DotEnv


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'not-so-secret')
    AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY')
    db_path = os.path.join(os.path.dirname(__file__), 'authy2fa.sqlite')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        env = DotEnv()
        env.init_app(app)

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
