from flask import abort, current_app, flash, redirect, request, session, url_for
from functools import wraps

import hmac
import hashlib
import base64

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

def login_verified(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        verified = session.get('verified', False)
        if verified:
            return f(*args, **kwargs)

        flash('You must complete your login before accessing that page.', 'info')
        return redirect(url_for('auth.log_in'))
    return decorated_function

def verify_authy_request(f):
    """
    Verifies that a OneTouch callback request came from Authy
    See https://docs.authy.com/new_doc/authy_onetouch_api#authenticating-callbacks-from-authy-onetouch
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the request URL without the parameters
        url = request.url

        # Get a string that concatenates all the POST data in case-sensitive
        # order by key
        sorted_keys = sorted(request.form.keys())
        sorted_params = ''
        for key in sorted_keys:
            sorted_params += '{0}={1}'.format(key, request.form[key])

        # Concatenate the url and the sorted parameters
        data = url + sorted_params

        # Hash it using HMAC-SHA256 and our Authy API key
        digest = hmac.new(current_app.config['AUTHY_API_KEY'], msg=data,
                          digestmod=hashlib.sha256).digest()

        # Encode the digest in base64
        digest_in_base64 = base64.b64encode(digest).decode()

        # Confirm that our digest_in_base64 matches the one in the request's
        # X-Authy-Signature header
        authy_signature = request.headers['X-Authy-Signature']
        if digest_in_base64 == authy_signature:
            # The two signatures match - this request is authentic
            return f(*args, **kwargs)

        # The signatures didn't match - abort this request
        return abort(400)
    return decorated_function
