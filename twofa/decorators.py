from collections import OrderedDict
from flask import abort, current_app, flash, redirect, request, session, url_for
from functools import wraps
from urllib import quote

import copy
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

# 'approval_request[expiration_timestamp]=1445713508&approval_request[logos]=&approval_request[transaction][created_at_time]=1445627108&approval_request[transaction][customer_uuid]=5ccf0040-ed25-0132-5987-0e67b818e6fb&approval_request[transaction][details][Email+Address]=jarodreyes+test13@gmail.com&approval_request[transaction][device_details]=&approval_request[transaction][device_geolocation]=&approval_request[transaction][device_signing_time]=0&approval_request[transaction][encrypted]=false&approval_request[transaction][flagged]=false&approval_request[transaction][message]=Request+to+Login+to+Twilio+demo+app&approval_request[transaction][reason]=&approval_request[transaction][requester_details]=&approval_request[transaction][status]=approved&approval_request[transaction][uuid]=e6afff60-5be6-0133-766e-0e67b818e6fb&authy_id=5588010&callback_action=approval_request_status&device_uuid=5c56ece0-5406-0133-7210-0e67b818e6fb&signature=N/mUjlBcRtIaLnFjF4kLgtQLtWmmK4FgtA8QXiHqjy9lroRUUbPfPXsEYrXyC5MA8VWKoEiU7euHacRcxrQ10utfO2ATYL/TwSdigys9ngkB3sxz7dndDM5BzS9ih/Fn2x+LziNhykTaGS4ceC7L7nB0F5Rc13gyvje9Tqiee0sWeJB9FvVWi3Qk8d7vbXqCBwPcxS4Ru8F9CipvUPQZUlHy4T710kz8fNZlnTOhWsPs2fDk0Adpecr185NWJRt5OSIpHEJLc6ztkyXkMpmhvqE8IS+OUPY25YbQt+kSzxNgRbatv/lbfk0FdHcqiSV10qKFW3F8AeozDo3bF/d9dQ==&status=approved&uuid=e6afff60-5be6-0133-766e-0e67b818e6fb'

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
            flattened_item = sort_dict(value, flattened_key)
        else:
            flattened_item = '{0}={1}'.format(flattened_key, value)

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
        encoded_data = quote(sorted_data)

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

        import pdb; pdb.set_trace()

        if digest_in_base64 == authy_signature:
            # The two signatures match - this request is authentic
            return f(*args, **kwargs)

        # The signatures didn't match - abort this request
        return abort(400)
    return decorated_function
