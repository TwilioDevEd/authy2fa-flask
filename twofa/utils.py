from authy.api import AuthyApiClient
from flask import current_app

from . import db
from .models import User


def get_authy_client():
    """Returns an AuthyApiClient"""
    return AuthyApiClient(current_app.config['AUTHY_API_KEY'])

def create_user(form):
    """Creates an Authy user and then creates a database User"""
    client = get_authy_client()

    # Create a new Authy user with the data from our form
    authy_user = client.users.create(form.email.data,
                                     form.phone_number.data,
                                     form.country_code.data)

    # If the Authy user was created successfully, create a local User
    # with the same information + the Authy user's id
    if authy_user.ok():
        user = User(form.email.data, form.password.data, form.name.data,
                    form.country_code.data, form.phone_number.data,
                    authy_user.id)

        # Save the user
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user

def send_authy_token_request(authy_user_id):
    """
    Sends a request to Authy to send a SMS verification code to a user's phone
    """
    client = get_authy_client()

    client.users.request_sms(authy_user_id)

def verify_authy_token(authy_user_id, user_entered_code):
    """Verifies a user-entered token with Authy"""
    client = get_authy_client()

    return client.tokens.verify(authy_user_id, user_entered_code)
