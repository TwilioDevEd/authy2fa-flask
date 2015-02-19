from flask import render_template, request, Response

from . import app, db, models, authy_api



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
    if authy_user.ok():
        new_user = models.User(email, password, authy_user.id)
        db.session.add(new_user)
        db.session.commit()
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

