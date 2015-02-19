from flask import jsonify, render_template, request, Response

from flask.ext.login import login_user, logout_user, login_required, \
                            current_user
from . import app, db, models, authy_api


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user', methods=['GET', 'POST'])
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
        db.session.refresh(new_user)
        token = new_user.generate_api_token()
        return jsonify({'token': token.decode('ascii')})
    return Response('Error', status=500, mimetype='application/json')


@app.route('/session', methods=['POST'])
@login_required
def session():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    return Response('', status=200, mimetype='application/json')


@app.route('/session/verify', methods=['POST'])
def verify():
    return 'ok'


@app.route('/session/resend', methods=['POST'])
def resend():
    return 'ok'

