from . import db, authy_api
from .models import User


def _validate_field(form, field_name, field_label, errors):
    field = form.get(field_name, None)
    if not field:
        errors.append("{0} is required.".format(field_label))


def validate_sign_up_form(form):
    errors = []
    _validate_field(form, 'fullName', 'Full name', errors)
    _validate_field(form, 'email', 'Email', errors)
    _validate_field(form, 'password', 'Password', errors)
    _validate_field(form, 'countryCode', 'Country code', errors)
    _validate_field(form, 'phone', 'Phone number', errors)
    # finally, check if email already taken
    if User.query.filter_by(email=form.get('email', '')).count() > 0:
        errors.append("Email address already taken.")
    if not errors:
        return True, ""
    return False, ' '.join(errors)


def create_user(form):
    full_name = form.get('fullName', '')
    country_code = form.get('countryCode', '')
    phone = form.get('phone', '')
    email = form.get('email', '')
    password = form.get('password', '')
    authy_user = authy_api.users.create(email, phone, country_code)
    if authy_user.ok():
        user = User(email, password, full_name, country_code, phone,
                    authy_user.id)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user
