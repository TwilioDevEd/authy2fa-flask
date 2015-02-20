from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import JSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature

from . import app, db

class User(db.Model):
    """
        Represents a single user in the system.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(256))
    country_code = db.Column(db.Integer)
    phone = db.Column(db.String(30))
    authy_id = db.Column(db.Integer)

    def __init__(self, email, password, full_name, country_code,
                 phone, authy_id):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.country_code = country_code
        self.phone = phone
        self.authy_id = authy_id

    def generate_api_token(self):
        serializer = Serializer(app.config['SECRET_KEY'])
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_api_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except BadSignature:
            # token is invalid
            return None
        return User.query.get(data['id'])

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_user = {
            'fullName': self.full_name,
            'phone': str(self.country_code) + ' ' + self.phone,
            'email': self.email,
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.email
