"""
Emotly

DEED
"""
import os
import bcrypt
import hashlib
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
