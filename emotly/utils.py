"""
Emotly

DEED
"""
import os
import bcrypt
import hashlib
import hmac
import json
import base64
import datetime
from postmark import PMMail
from emotly import app
from emotly import constants as CONSTANTS
from functools import wraps
from flask import make_response, request, jsonify


# Create the salt for the user registration.
def get_salt():
    return bcrypt.gensalt(app.config['GENSALT_ROUNDS'])


# Used to hash password for user registration.
def hash_password(password, salt):
    return bcrypt.hashpw(password, salt)


# Generate a token for the email confirmation of the user.
def generate_confirmation_token(email):
    token_string = hashlib.sha224(get_salt() +
                                  email.encode('utf-8') +
                                  datetime.datetime.now()
                                  .strftime(CONSTANTS.DATE_FORMAT)
                                  .encode('utf-8') +
                                  get_salt()).hexdigest()
    return token_string


# Function used to actually send an email for the email
# confirmation of the user during the registration process.
def send_email_confirmation(email, confirmation_token):
    message = PMMail(api_key=app.config['PM_API_TOKEN'],
                     subject="Hello from Emotly.com",
                     sender=app.config['EMAIL_SENDER'],
                     to=email,
                     text_body="Welcome to Emotly.com. Please confirm your "
                               "email in the next 24 hours. Click on "
                               "https://emotly.herokuapp.com/confirm_email/" +
                               confirmation_token)
    message.send()


# Function used to actually send a welcome email with the
# link to the progressive web app.
def send_welcome_email(email, app_link):
    message = PMMail(api_key=app.config['PM_API_TOKEN'],
                     subject="Hello from Emotly.com",
                     sender=app.config['EMAIL_SENDER'],
                     to=email,
                     text_body="Welcome to Emotly.com. Thank you for "
                               "confirming your email. Start to get emotional "
                               "on " + app_link)
    message.send()


# Generate a Json Web Token from a given user.
# TODO: add support for different hash algorithms.
def generate_jwt_token(user, delta=datetime.timedelta(hours=300)):
    if user is None:
        return None
    # generate the header and the payload message
    header = {'algo': 'sha256', 'type': 'jwt'}
    starting_date = user.last_login \
        if user.last_login is not None else datetime.datetime.now()
    payload = {'nickname': user.nickname,
               'expire': (starting_date + delta)
               .strftime(CONSTANTS.DATE_FORMAT)
               }
    # sign token using a cryptografically hash algoritm
    signature = sign_jwt(header, payload)
    jwt = {'header': header, 'payload': payload, 'signature': signature}

    return json.dumps(jwt)


# Return True if a given token is valid.
def verify_jwt_token(token):
    json_format = json.loads(token)
    date_today = datetime.datetime.now()
    date_expire = datetime.datetime.strptime(json_format["payload"]["expire"],
                                             CONSTANTS.DATE_FORMAT)
    if date_expire < date_today:
        return False
    signature_received = sign_jwt(json_format["header"],
                                  json_format["payload"])
    return signature_received == json_format["signature"]


# Return a cryptografic hash value used to sign
# the given message (header + payload).
def sign_jwt(header, payload):
    # Sort and convert the dictionary in string.
    # This is necessary since Python dictionaries do not guarantee any
    # particular order.
    str_message = ''.join('{}:{} '.format(val[0], val[1])
                          for val in sorted(header.items()))
    str_message = str_message.join('{}:{} '.format(val[0], val[1])
                                   for val in sorted(payload.items()))

    # Use a cryptographic hash algorithm to sign the header and the payload;
    # this "ensure" that the token is legitimately from us.
    signature = hmac.new(app.config["HMAC_SECRET_KEY"].encode("utf-8"),
                         str_message.encode("utf-8"),
                         hashlib.sha256).digest()

    signature = base64.b64encode(signature).decode("utf-8")
    return signature


# Verify that a request has valid json data.
def valid_json(api_method):
    @wraps(api_method)
    def check_valid_json(*args, **kwargs):
        try:
            data = request.data.decode("utf-8")
            if not data:
                return response_handler(500, CONSTANTS.INVALID_JSON_DATA)
            data = json.loads(data)
            kwargs['data'] = data
        except Exception:
            return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
        return api_method(*args, **kwargs)
    return check_valid_json


# App error and response handler.
def response_handler(code, value, message=None):
    if message is None:
        message = "message"
    return make_response(jsonify({message: value}), code)
