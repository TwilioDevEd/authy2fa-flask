from flask import abort, current_app, flash, redirect, request, session, url_for
from functools import wraps
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
        url = request.url
        nonce = request.headers['X-Authy-Signature-Nonce']

        # Get a string that concatenates all the POST data in case-sensitive
        # order by key
        sorted_data = sort_dict(request.json)
        encoded_data = quote_plus(sorted_data, safe='/=+&%')

        # Concatenate the url and the sorted parameters
        data = nonce + '|' + request.method + '|' + url + '|' + encoded_data

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
