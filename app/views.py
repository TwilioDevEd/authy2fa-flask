from flask import jsonify, render_template, request, Response

from flask.ext.login import login_user, logout_user, login_required, \
                            current_user

from . import app, db, models, authy_api, login_manager
from .models import User


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if current_user.verify_api_token(request.headers['X-API-TOKEN']):
            token = current_user.generate_api_token()
            return jsonify({})
    elif request.method == 'POST':
        full_name = request.form.get('fullName', '')
        country_code = request.form.get('countryCode', '')
        phone = request.form.get('phone', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        authy_user = authy_api.users.create(email, phone, country_code)
        if authy_user.ok():
            new_user = User(email, password, full_name,
                            country_code, phone, authy_user.id)
            db.session.add(new_user)
            db.session.commit()
            db.session.refresh(new_user)
            login_user(new_user)
            token = new_user.generate_api_token()
            return jsonify({'token': token.decode('ascii')})
        return Response('Error', status=500, mimetype='application/json')


@app.route('/session', methods=['POST', 'DELETE'])
def session():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            token = user.generate_api_token()
            sms = authy_api.users.request_sms(user.authy_id)
            return jsonify({'token': token.decode('ascii')})
        else:
            resp = jsonify({'message': 'Invalid username or password.'})
            resp.status_code = 403
            return resp
    elif request.method == 'DELETE':
        logout_user()
        return jsonify({})
    return Response('Error', status=403, mimetype='application/json')


@app.route('/session/verify', methods=['POST'])
@login_required
def verify():
    user_entered_code = request.form.get('code', None)
    if user_entered_code:
        verification = authy_api.tokens.verify(current_user.authy_id,
                                               user_entered_code)
        if verification.ok():
            return jsonify({})
        else:
            resp = jsonify({'message': 'Invalid token.'})
            resp.status_code = 403
            return resp
    return Response('', status=403, mimetype='application/json')


@app.route('/session/resend', methods=['POST'])
@login_required
def resend():
    if current_user.verify_api_token(request.headers['X-API-TOKEN']):
        sms = authy_api.users.request_sms(current_user.authy_id)
        return jsonify({})
    else:
        return Response('', status=403, mimetype='application/json')
