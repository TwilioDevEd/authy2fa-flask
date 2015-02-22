from authy.api import AuthyApiClient
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, static_path="")
app.config.from_object('twofa.config')
db = SQLAlchemy(app)
authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])

from . import views, models
