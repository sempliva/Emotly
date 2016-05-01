"""
Emotly

DEED
"""
from emotly import constants as CONSTANTS
import datetime
import json
from flask import Blueprint, request, render_template
from flask import flash, make_response
from emotly.models import User, Token
from mongoengine import DoesNotExist, NotUniqueError, ValidationError
from emotly.utils import get_salt, hash_password
from emotly.utils import generate_confirmation_token
from emotly.utils import send_email_confirmation, send_welcome_email
from emotly.utils import generate_jwt_token
from emotly.utils import response_handler

# User Controller
user_controller = Blueprint('user_controller', __name__)


# Verify user credential and return a JWT Token if
# the user has access to the system.
@user_controller.route(CONSTANTS.REST_API_PREFIX + "/login", methods=["POST"])
def login():
    if not request.is_secure:
        return response_handler(403, CONSTANTS.NOT_HTTPS_REQUEST)
    try:
        # Retrieve json data and user data.
        data = json.loads(request.data.decode('utf-8'))
        if '@' in data['user_id']:
            user = User.objects.get(email__iexact=data['user_id'])
        else:
            user = User.objects.get(nickname__iexact=data['user_id'])
    except DoesNotExist:
        # User does not exist.
        return response_handler(404, CONSTANTS.USER_DOES_NOT_EXIST)
    except Exception:
        # No data sent by the client or there
        # was an error queryng the database.
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    if not user.confirmed_email:
        # User email not confirmed yet.
        return response_handler(403, CONSTANTS.USER_NOT_CONFIRMED)
    if User.verify_password(user, data['password'].encode('utf-8')):
        try:
            user.update(last_login=datetime.datetime.now())
        except Exception:
            # Error updating the user data.
            return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
        # Generate and send JWT
        return make_response(generate_jwt_token(user), 200)
    return response_handler(403, CONSTANTS.UNAUTHORIZED)


@user_controller.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("page-signup.html")
    try:
        register_user(request)
        flash(CONSTANTS.REGISTRATION_COMPLETED_CHECK_EMAIL)
    except ValidationError:
        flash(CONSTANTS.REGISTRAION_ERROR_INVALID_DATA, 'Error')
    except NotUniqueError:
        flash(CONSTANTS.REGISTRAION_ERROR_USER_EXISTS, 'Error')
    except Exception:
        flash(CONSTANTS.INTERNAL_SERVER_ERROR, 'Error')
    return render_template("page-home.html")


# Registration endpoint. It allows the user to create an account.
# Accepts JSON data containing nickname, email and password.
# TODO: Add security check (number of call?).
@user_controller.route(CONSTANTS.REST_API_PREFIX + "/signup", methods=["POST"])
def signup_api():
    try:
        register_user(request)
        return response_handler(200,
                                CONSTANTS.REGISTRATION_COMPLETED_CHECK_EMAIL)
    except ValidationError:
        return response_handler(400, CONSTANTS.REGISTRAION_ERROR_INVALID_DATA)
    except NotUniqueError:
        return response_handler(400, CONSTANTS.REGISTRAION_ERROR_USER_EXISTS)
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)


# Use the post params to generate salt, hash password,
# confirmation token. Save the user and send the email.
# (The user is saved even if the mail is not sent).
def register_user(req):
    if req.headers['content-type'] == 'application/json':
        data = json.loads(req.data.decode('utf-8'))
        req_nickname = data['inputNickname']
        req_pwd = data['inputPassword'].encode('utf-8')
        req_email = data['inputEmail']
    else:
        req_nickname = req.form['inputNickname']
        req_pwd = req.form['inputPassword'].encode('utf-8')
        req_email = req.form['inputEmail']

    # Normalize email.
    req_email = req_email.lower()
    salt = get_salt()
    hash_pwd = hash_password(req_pwd, salt)
    user = User(nickname=req_nickname, password=hash_pwd, salt=salt,
                email=req_email)

    token_string = generate_confirmation_token(user.email)
    user.confirmation_token = Token(token=token_string)
    user.save()
    send_email_confirmation(user.email, token_string)


# This route is used to confirm the user through the
# confirmation token received by email and send a welcome email
# with the link to the progressive web app.
@user_controller.route("/confirm_email/<confirmation_token>", methods=['GET'])
def confirm_email(confirmation_token):
    try:
        confirm_registration_email(confirmation_token)
        flash(CONSTANTS.EMAIL_CONFIRMED)
    except DoesNotExist as e:
        flash(CONSTANTS.ERROR_IN_CONFIRMING_EMAIL)
    except Exception:
        flash(CONSTANTS.INTERNAL_SERVER_ERROR, 'Error')
    return render_template("page-home.html")


# Check if the confirmation token is still valid (received in the last 24
# hours). Activate the user, delete the token, update the update_at user field.
def confirm_registration_email(confirmation_token):
    time_range = datetime.datetime.now() - datetime.timedelta(days=1)
    user = User.objects.get(confirmation_token__token=confirmation_token,
                            confirmation_token__created_at__gte=time_range)
    User.objects.get(pk=user.id).update(confirmed_email=True,
                                        unset__confirmation_token=1,
                                        update_at=datetime.datetime.now())
    send_welcome_email(user.email, CONSTANTS.APP_LINK)


# Return the user from the jwt token
def get_user_from_jwt_token(token):
    json_format = json.loads(token)
    return User.objects.get(nickname=json_format["payload"]["nickname"])


# Return true is the user is confirmed.
def is_user_confirmed(user_id):
    if User.objects.only('confirmed_email').get(id=user_id).confirmed_email:
        return True
    return False
