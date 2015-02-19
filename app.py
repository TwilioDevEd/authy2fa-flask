import os
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '')


app = Flask(__name__, static_path="")
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user', methods=['POST'])
def signup():
    return 'ok'


@app.route('/session', methods=['POST'])
def session():
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

