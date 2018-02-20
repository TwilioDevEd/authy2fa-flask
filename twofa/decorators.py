from flask import abort, current_app, flash, redirect, request, session, url_for
from functools import wraps
try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

import hmac
import hashlib
import json
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
    """
    Redirects requests if the current user has not verified their login with
    Authy
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id', False)
        if user_id:
            user = User.query.filter_by(id=user_id).one_or_none()
            if user is not None and user.authy_status == 'approved':
                return f(*args, **kwargs)

        flash('You must complete your login before accessing that page.', 'info')
        return redirect(url_for('auth.log_in'))
    return decorated_function


def sort_dict(original, parent_path=''):
    """Transforms a dict into the format Authy requires"""
    flattened_dict = ''

    for key in sorted(original):
        value = original[key]

        if parent_path:
            flattened_key = parent_path + '[{0}]'.format(key)
        else:
            flattened_key = key

        # If the value is a dict, then recurse over that
        if isinstance(value, dict):
            # If the dict is empty, skip this value
            if not value:
                continue
            else:
                flattened_item = sort_dict(value, flattened_key)
        else:
            if value is None:
                encoded_value = ''
            else:
                encoded_value = quote_plus(json.dumps(value).strip('"'))

            flattened_item = '{0}={1}'.format(flattened_key, encoded_value)

        if flattened_dict:
            flattened_dict += '&' + flattened_item
        else:
            flattened_dict = flattened_item

    return flattened_dict


def verify_authy_request(f):
    """
    Verifies that a OneTouch callback request came from Authy
    See https://docs.authy.com/new_doc/authy_onetouch_api#authenticating-callbacks-from-authy-onetouch
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the request URL without the parameters
        from .utils import get_authy_client
        client = get_authy_client()

        response = client.one_touch.validate_one_touch_signature(
            request.headers['X-Authy-Signature'],
            request.headers['X-Authy-Signature-Nonce'],
            request.method,
            request.url,
            request.json
        )
        if response:
            # The two signatures match - this request is authentic
            return f(*args, **kwargs)

        # The signatures didn't match - abort this request
        return abort(400)
    return decorated_function
