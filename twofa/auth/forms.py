from flask_wtf import Form
from wtforms import IntegerField, PasswordField, StringField, validators

from ..models import User


def validate_unique_email(form, field):
    """Validates that an email address hasn't been registered already"""
    if User.query.filter_by(email=field.data).count() > 0:
        raise validators.ValidationError('This email address has already been registered.')

class SignUpForm(Form):
    """Form used for registering new users"""
    name = StringField('Full name', validators=[validators.InputRequired()])
    email = StringField('Email', validators=[validators.InputRequired(), validate_unique_email])
    password = PasswordField('Password', validators=[validators.InputRequired()])
    country_code = IntegerField('Country code', validators=[validators.InputRequired()])
    phone_number = StringField('Mobile phone', validators=[validators.InputRequired()])

class LoginForm(Form):
    """Form used for logging in existing users"""
    email = StringField('Email', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])

class VerifyForm(Form):
    """Form used to verify SMS two factor authentication codes"""
    verification_code = StringField('Verification code', validators=[validators.InputRequired(),
                                                                     validators.Length(min=6, max=10)])
