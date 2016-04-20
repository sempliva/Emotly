"""
Emotly

DEED
"""
import datetime
import json
from flask import Blueprint, request, render_template
from flask import flash, jsonify, make_response
from emotly.models import User, Token
from mongoengine import DoesNotExist, NotUniqueError, ValidationError
from emotly.utils import get_salt, hash_password
from emotly.utils import generate_confirmation_token
from emotly.utils import send_email_confirmation
from emotly.utils import generate_jwt_token

# User Controller
user_controller = Blueprint('user_controller', __name__)


# Verify user credential and return a JWT Token if
# the user has access to the system.
@user_controller.route("/api/1.0/login", methods=["POST"])
def login():
    if not request.is_secure:
        return make_response(jsonify({'message': 'Bad request.'}), 403)
    try:
        # Retrieve json data and user data.
        data = json.loads(request.data.decode('utf-8'))
        user = User.objects.get(email=data['email'])
    except DoesNotExist:
        # User does not exist.
        return make_response(jsonify({'message': 'Authentication error.'}),
                             404)
    except Exception:
        # No data sent by the client or there
        # was an error queryng the database.
        return make_response(jsonify({'message': 'Internal server error.'}),
                             500)
    if not user.confirmed_email:
        # User email not confirmed yet.
        return make_response(jsonify({'message': 'Unauthorized access.'}),
                             403)
    if User.verify_password(user, data['password'].encode('utf-8')):
        try:
            user.update(last_login=datetime.datetime.now())
        except Exception:
            # Error updating the user data.
            return make_response(
                jsonify({'message': 'Internal server error.'}),
                500)
        # Generate and send JWT
        return make_response(generate_jwt_token(user), 200)
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


@user_controller.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("page-signup.html")
    try:
        register_user(request)
        flash('Registration completed! Ceck your email :)')
    except ValidationError:
        flash('Registration error: \
              Please insert valid data!', 'Error')
    except NotUniqueError:
        flash('Registration error: User already exist!', 'Error')
    except Exception:
        flash('Internal server error', 'Error')
    return render_template("page-home.html")


# Use the post params to generate salt, hash password,
# confirmation token. Save the user and send the email.
# (The user is saved even if the mail is not sent).
def register_user(req):
    req_nickname = req.form['inputNickname']
    req_pwd = req.form['inputPassword'].encode('utf-8')
    req_email = req.form['inputEmail']

    salt = get_salt()
    hash_pwd = hash_password(req_pwd, salt)
    user = User(nickname=req_nickname, password=hash_pwd, salt=salt,
                email=req_email)

    token_string = generate_confirmation_token(user.email)
    user.confirmation_token = Token(token=token_string)
    user.save()
    send_email_confirmation(user.email, token_string)


# This route is used to confirm the user through the
# confirmation token received by email.
@user_controller.route("/confirm_email/<confirmation_token>", methods=['GET'])
def confirm_email(confirmation_token):
    try:
        confirm_registration_email(confirmation_token)
        flash('Email Confirmed')
    except DoesNotExist as e:
        flash('Error in confirming email.')
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


# Return the user from the jwt token
def get_user_from_jwt_token(token):
    json_format = json.loads(token)
    return User.objects.get(nickname=json_format["payload"]["nickname"])


# Return true is the user is confirmed.
def is_user_confirmed(user_id):
    if User.objects.only('confirmed_email').get(id=user_id).confirmed_email:
        return True
    return False
