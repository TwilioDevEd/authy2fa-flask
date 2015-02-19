import os
from authy.api import AuthyApiClient
from flask import Flask, Response, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

import models, forms


AUTHY_API_KEY = os.environ.get('AUTHY_API_KEY', '')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')


app = Flask(__name__, static_path="")
db = SQLAlchemy(app)
authy_api = AuthyApiClient(AUTHY_API_KEY)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user', methods=['POST'])
def signup():
    full_name = request.form.get('fullName', '')
    country_code = request.form.get('countryCode', '')
    phone = request.form.get('phone', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    authy_user = authy_api.users.create(email, phone, country_code)
    print authy_user.ok()
    print authy_user.errors()
    if authy_user.ok():
        new_user = models.User(email, password, authy_user.id)
    return Response('', status=200, mimetype='application/json')


@app.route('/session', methods=['POST'])
def session():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    return 'ok'


@app.route('/session/verify', methods=['POST'])
def verify():
    return 'ok'


@app.route('/session/resend', methods=['POST'])
def resend():
    return 'ok'


if __name__ == '__main__':
    # first attempt to get the PORT environment variable, 
    # otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

