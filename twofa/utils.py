from authy.api import AuthyApiClient
from flask import current_app


def get_authy_client():
    """ Return a configured Authy client. """
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
        return form.create_user(authy_user.id)


def send_authy_token_request(authy_user_id):
    """
    Sends a request to Authy to send a SMS verification code to a user's phone
    """
    client = get_authy_client()

    client.users.request_sms(authy_user_id)


def send_authy_one_touch_request(authy_user_id, email=None):
    """Initiates an Authy OneTouch request for a user"""
    client = get_authy_client()

    details = {}

    if email:
        details['Email'] = email

    response = client.one_touch.send_request(
        authy_user_id,
        'Request to log in to Twilio demo app',
        details=details
    )

    if response.ok():
        return response.content


def verify_authy_token(authy_user_id, user_entered_code):
    """Verifies a user-entered token with Authy"""
    client = get_authy_client()

    return client.tokens.verify(
        authy_user_id,
        user_entered_code
    )


def authy_user_has_app(authy_user_id):
    """Verifies a user has the Authy app installed"""
    client = get_authy_client()

    authy_user = client.authy_client.users.status(authy_user_id)
    try:
        return authy_user.content['status']['registered']
    except KeyError:
        return False
