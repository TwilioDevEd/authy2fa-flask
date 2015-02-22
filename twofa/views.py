from authy import AuthyApiException
from flask import jsonify, render_template, request, Response, session

from . import app, authy_api
from .decorators import login_required
from .models import User
from .utils import validate_sign_up_form, create_user


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/user', methods=['GET'])
@login_required
def handle_user():
    user = User.query.get(session['user_id'])
    return jsonify(user.to_json())


@app.route('/user', methods=['POST'])
def sign_up():
    form_valid, validation_errors = validate_sign_up_form(request.form)
    if form_valid:
        try:
            user = create_user(request.form)
        except AuthyApiException:
            resp = jsonify({'message':
                            'Unable to send SMS token at this time.'})
            resp.status_code = 503
            return resp
        token = user.generate_api_token()
        session['user_id'] = user.id
        return jsonify({'token': token.decode('ascii')})
    else:
        resp = jsonify({'message': validation_errors})
        resp.status_code = 409
        return resp


@app.route('/session', methods=['POST'])
def sign_in():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    user = User.query.filter_by(email=email).first()
    if user is not None and user.verify_password(password):
        session['user_id'] = user.id
        token = user.generate_api_token()
        sms = authy_api.users.request_sms(user.authy_id)
        return jsonify({'token': token.decode('ascii')})
    else:
        resp = jsonify({'message': 'Invalid username or password.'})
        resp.status_code = 403
        return resp


@app.route('/session', methods=['DELETE'])
def sign_out():
    # purge user session
    session.pop('user_id', None)
    return jsonify({'message': 'User logged out.'})


@app.route('/session/verify', methods=['POST'])
@login_required
def verify():
    user_entered_code = request.form.get('code', None)
    if user_entered_code:
        user = User.query.get(session.get('user_id'))
        verified = authy_api.tokens.verify(user.authy_id, user_entered_code)
        if verified.ok():
            return jsonify({'message': 'User verified.'})
    resp = jsonify({'message': 'Invalid token.'})
    resp.status_code = 403
    return resp


@app.route('/session/resend', methods=['POST'])
@login_required
def resend():
    user = User.query.get(session.get('user_id'))
    sms = authy_api.users.request_sms(user.authy_id)
    return jsonify({'message': 'Code re-sent!'})

