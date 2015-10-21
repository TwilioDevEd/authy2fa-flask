from authy import AuthyApiException
from flask import flash, redirect, render_template, request, session, url_for

from . import auth
from .forms import SignUpForm
from ..models import User
from ..utils import create_user

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm(request.form)

    if form.validate_on_submit():
        try:
            user = create_user(form)
            api_token = user.generate_api_token().decode('ascii')
            session['user_id'] = user.id
            session[api_token] = True

            return redirect(url_for('account'))

        except AuthyApiException:
            form.errors['Authy API'] = 'Unable to send SMS token at this time'

    return render_template('signup.html', form=form)

@auth.route('/account')
def account():
    user = User.query.get(session['user_id'])
    return render_template('account.html', user=user)

@auth.route('/logout')
def log_out():
    # purge user session and second factor verification (if exists)
    session.pop('user_id', None)
    session.pop(request.headers.get('X-API-TOKEN', ''), None)
    flash("You're now logged out! Thanks for visiting.", 'info')
    return redirect(url_for('main.home'))
