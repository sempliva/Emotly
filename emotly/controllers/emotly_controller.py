"""
Emotly

DEED
"""
import json
from flask import Blueprint, request, flash
from emotly import constants as CONSTANTS
from flask.ext.mongoengine import MongoEngine
from functools import wraps
from emotly.models import User, Emotly, MOOD
from mongoengine import DoesNotExist
from emotly.controllers.user_controller import get_user_from_jwt_token
from emotly.controllers.user_controller import is_user_confirmed
from emotly.utils import verify_jwt_token, valid_json, response_handler


# Emotly Controller
emotly_controller = Blueprint('emotly_controller', __name__)


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


# Retrieve the emotlies list, desc ordered by creation date.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + 'emotlies',
                         methods=['GET'])
def list_emotlies():
    try:
        emotlies = Emotly.objects.all().order_by('-created_at')
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    # At the moment serialize mood, creation date of the mood
    # and user nickname.
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Retrieve the current user's emotlies list, desc ordered by creation date.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + 'emotlies/own',
                         methods=['GET'])
@require_token
def list_own_emotlies(**kwargs):
    try:
        user = kwargs['user']
        emotlies = Emotly.objects(user=user.id).only("mood", "created_at").\
            order_by('-created_at')
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Create a new emotly for the current user.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + 'emotlies/new',
                         methods=['POST'])
@require_token
@valid_json
def post_new_emotly(**kwargs):
    try:
        user = kwargs['user']
        data = kwargs['data']
        if 'mood' not in data:
            return response_handler(500, CONSTANTS.INVALID_JSON_DATA)

        emotly = Emotly(mood=data['mood'])
        emotly.user = user
        emotly.save()
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, emotly.serialize(), 'emotly')


# Retrieve a specific emotly.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX +
                         'emotlies/show/<emotly_id>', methods=['GET'])
@require_token
def get_emotly(emotly_id, **kwargs):
    try:
        emotly = Emotly.objects.only("mood", "created_at").get(id=emotly_id)
    except DoesNotExist:
        return response_handler(404, CONSTANTS.EMOTLY_DOES_NOT_EXIST)
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, emotly.serialize(), 'emotly')


# Retrieve the list of moods.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + 'moods', methods=['GET'])
def list_moods():
    try:
        formatted_mood = [{"id": k, "value": v} for k, v in MOOD.items()]
        moods = response_handler(200, formatted_mood, 'moods')
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return moods
