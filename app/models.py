from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from . import app, db

class User(UserMixin, db.Model):
    """
        Represents a single user in the system.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    authy_id = db.Column(db.Integer)

    def __init__(self, email, password, authy_id):
        self.email = email
        self.password = password
        self.authy_id = authy_id

    def generate_api_token(self, expiration=1200):
        serializer = Serializer(app.config['SECRET_KEY'],
                                expires_in=expiration)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_api_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            # token is valid but it has expired
            return None
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
            'email': self.email,
        }
        return json_user

    def __repr__(self):
        return '<User %r>' % self.email
