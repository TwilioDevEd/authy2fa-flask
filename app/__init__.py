import os
from authy.api import AuthyApiClient
from flask import Flask, Response, render_template, request
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__, static_path="")
app.config.from_object('app.config')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'session'
login_manager.init_app(app)
authy_api = AuthyApiClient(app.config['AUTHY_API_KEY'])


from . import views, models, forms
