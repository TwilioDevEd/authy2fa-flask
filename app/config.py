import os


AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY', '')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')

