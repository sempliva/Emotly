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
                                  datetime.datetime.now().strftime("%I:%M:%S")
                                                         .encode('utf-8') +
                                  get_salt()).hexdigest()
    return token_string


# Function use to actually send the email for the email
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


# Generate a Json Web Token from a given user.
# TODO: add support for different hash algorithms.
def generate_jwt_token(user, delta=datetime.timedelta(hours=300)):
    if user is None:
        return None
    # generate the header and the payload message
    header = {'algo': 'sha256', 'type': 'jwt'}
    payload = {'nickname': user.nickname,
               'expire': (user.last_login + delta).strftime("%Y:%m:%d %H:%M:%S")
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
                                             "%Y:%m:%d %H:%M:%S")
    if date_expire < date_today:
        return False
    signature_received = sign_jwt(json_format["header"],
                                  json_format["payload"])
    return signature_received == json_format["signature"]


# Return a cryptografic hash value used to sign
# the given message ( header + payload).
def sign_jwt(header, payload):
    str_message = str(header) + str(payload)
    # user a cryptographic hash algorithm to sing header and payload
    # this "ensure" that the token has been generated from our backend
    signature = hmac.new(app.config["HMAC_SECRET_KEY"].encode("utf-8"),
                         str_message.encode("utf-8"),
                         hashlib.sha256).digest()

    signature = base64.b64encode(signature).decode("utf-8")
    return signature
