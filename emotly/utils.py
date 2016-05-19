"""
MIT License

Copyright (c) 2016 Emotly Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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

from emotly.models import User
from functools import wraps
from mongoengine import DoesNotExist
from flask import request
from urllib.parse import urlparse


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


# App error and response handler.
def response_handler(code, value, message=None):
    message = message or "message"
    return make_response(jsonify({message: value}), code)


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


# Decorator used to check user and token for emotlies api
# and return the user to the original fn.
def require_token(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        auth_token = request.headers.get('X-Emotly-Auth-Token')
        if auth_token and verify_jwt_token(auth_token):
            try:
                user = get_user_from_jwt_token(auth_token)
                # Check if user is confirmed, return 403 if does not exist.
                user_confirmed = is_user_confirmed(user.id)
                if user_confirmed:
                    # Pass user as in the  kwargs to the original fn.
                    kwargs['user'] = user
                    return api_method(*args, **kwargs)
                return response_handler(403, CONSTANTS.USER_NOT_CONFIRMED)
            # If does not exist return 404.
            except DoesNotExist:
                return response_handler(404, CONSTANTS.USER_DOES_NOT_EXIST)
        # If the request has no user token or it is not valid 403.
        return response_handler(403, CONSTANTS.UNAUTHORIZED)
    return check_api_key


# Decorator used to require HTTPS.
# If the app is in DEBUG mode and the hostaname is localhost the
# request is considere secure.
def require_https(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        url = urlparse(request.url)
        if app.config['DEBUG'] and (url.hostname == "localhost" or
                                    url.hostname == "127.0.0.1"):
            return api_method(*args, **kwargs)
        if not request.is_secure:
            return response_handler(403, CONSTANTS.NOT_HTTPS_REQUEST)
        return api_method(*args, **kwargs)
    return check_api_key


# This function is gonna be used to determine whether we're running in a
# SECURE and LOCAL environment while in DEBUG. Mostly used during development.
def should_override_security_restrictions(url):
    if app.debug is False:
        return False
    if url.hostname != 'localhost' or url.hostname != '127.0.0.1':
        return False

    return True


# Return the user from the jwt token.
def get_user_from_jwt_token(token):
    json_format = json.loads(token)
    return User.objects.get(nickname=json_format["payload"]["nickname"])


# Return true is the user is confirmed.
def is_user_confirmed(user_id):
    if User.objects.only('confirmed_email').get(id=user_id).confirmed_email:
        return True
    return False
