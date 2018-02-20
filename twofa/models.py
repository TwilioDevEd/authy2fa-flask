from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

import requests

from . import db


class User(db.Model):
    """
    Represents a single user in the system.
    """
    __tablename__ = 'users'

    AUTHY_STATUSES = (
        'unverified',
        'onetouch',
        'sms',
        'token',
        'approved',
        'denied'
    )

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(256))
    country_code = db.Column(db.Integer)
    phone = db.Column(db.String(30))
    authy_id = db.Column(db.Integer)
    authy_status = db.Column(db.Enum(*AUTHY_STATUSES, name='authy_statuses'))

    def __init__(self, email, password, full_name, country_code,
                 phone, authy_id, authy_status='approved'):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.country_code = country_code
        self.phone = phone
        self.authy_id = authy_id
        self.authy_status = authy_status

    def __repr__(self):
        return '<User %r>' % self.email

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @property
    def has_authy_app(self):
        # Importing here to avoid circular dependency
        from .utils import get_authy_client
        client = get_authy_client()

        authy_user = client.users.status(self.authy_id)
        try:
            return authy_user.content['status']['registered']
        except KeyError:
            return False

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def send_one_touch_request(self):
        """Initiates an Authy OneTouch request for this user"""
        # Importing here to avoid circular dependency
        from .utils import get_authy_client
        client = get_authy_client()

        url = '{0}/onetouch/json/users/{1}/approval_requests'.format(client.api_uri, self.authy_id)
        data = {
            'api_key': client.api_key,
            'message': 'Request to log in to Twilio demo app',
            'details[Email]': self.email
        }
        response = requests.post(url, data=data)
        json_response = response.json()

        if 'approval_request' in json_response:
            self.authy_status = 'onetouch'
        else:
            self.authy_status = 'sms'

        db.session.add(self)
        db.session.commit()

        return json_response
