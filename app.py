import os
from flask import Flask, render_template


ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')

app = Flask(__name__, static_path="")


@app.route('/')
def signin():
    return render_template("index.html")


if __name__ == '__main__':
    # first attempt to get the PORT environment variable, 
    # otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)

