from authy.api import AuthyApiClient
from flask import current_app

from . import db
from .models import User


def create_user(form):
    authy_client = AuthyApiClient(current_app.config['AUTHY_API_KEY'])

    authy_user = authy_client.users.create(form.email.data,
                                           form.phone_number.data,
                                           form.country_code.data)
    if authy_user.ok():
        user = User(form.email.data, form.password.data, form.name.data,
                    form.country_code.data, form.phone_number.data,
                    authy_user.id)
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user
