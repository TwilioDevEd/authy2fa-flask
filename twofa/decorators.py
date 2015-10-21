from flask import flash, redirect, request, session, url_for
from functools import wraps

from .models import User

def login_required(f):
    """Redirects requests to /login if the user isn't authenticated"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id', None)
        if user_id:
            user = User.query.filter_by(id=user_id).one_or_none()
            if user is not None:
                return f(*args, **kwargs)

        flash('Please log in before accessing that page.', 'info')
        return redirect(url_for('auth.log_in'))
    return decorated_function


def second_factor_verified(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verified = session.get('verified', False)
        if verified:
            return f(*args, **kwargs)

        flash('You must verify your login before accessing that page.', 'info')
        return redirect(url_for('auth.verify'))
    return decorated_function
