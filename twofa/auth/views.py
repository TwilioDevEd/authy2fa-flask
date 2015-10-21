from authy import AuthyApiException
from flask import flash, redirect, render_template, request, session, url_for

from . import auth
from .forms import LoginForm, SignUpForm, VerifyForm
from ..models import User
from ..utils import create_user, send_authy_sms_request, verify_authy_token

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        try:
            user = create_user(form)
            session['user_id'] = user.id

            return redirect(url_for('auth.account'))

        except AuthyApiException:
            form.errors['Authy API'] = ['Unable to send SMS token at this time']

    return render_template('signup.html', form=form)

@auth.route('/account')
def account():
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@auth.route('/login', methods=['GET', 'POST'])
def log_in():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session['user_id'] = user.id
            send_authy_sms_request(user.authy_id)
            return redirect(url_for('auth.verify'))
        else:
            form.errors['Invalid credentials'] = ['Invalid username or password']

    return render_template('login.html', form=form)

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerifyForm(request.form)

    if form.validate_on_submit():
        user_entered_code = form.verification_code.data
        user = User.query.get(session['user_id'])

        verified = verify_authy_token(user.authy_id, str(user_entered_code))
        if verified.ok():
            session['verified'] = True
            flash("You're logged in! Thanks for using two factor verification.", 'success')
            return redirect(url_for('auth.account'))
        else:
            form.errors['verification_code'] = ['Code invalid - please try again.']

    return render_template('verify.html', form=form)

@auth.route('/resend', methods=['POST'])
# @login_required
def resend():
    user = User.query.get(session.get('user_id'))
    send_authy_sms_request(user.authy_id)
    flash('I just re-sent your verification code - enter it below.', 'info')
    return redirect(url_for('auth.verify'))

@auth.route('/logout')
def log_out():
    # purge user session and second factor verification (if exists)
    session.pop('user_id', None)
    session.pop(request.headers.get('X-API-TOKEN', ''), None)
    flash("You're now logged out! Thanks for visiting.", 'info')
    return redirect(url_for('main.home'))
