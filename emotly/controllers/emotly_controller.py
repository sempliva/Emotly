"""
Emotly

DEED
"""
import json
from flask import Blueprint, request, flash
from emotly import constants as CONSTANTS
from flask.ext.mongoengine import MongoEngine
from emotly.models import User, Emotly, MOOD
from mongoengine import DoesNotExist
from emotly.utils import get_user_from_jwt_token, response_handler
from emotly.utils import require_token, valid_json


# Emotly Controller
emotly_controller = Blueprint('emotly_controller', __name__)


# Retrieve the emotlies list.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies',
                         methods=['GET'])
def list_emotlies():
    try:
        emotlies = Emotly.objects.all()
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    # At the moment serialize mood, creation date of the mood
    # and user nickname.
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Retrieve the current user's emotlies list.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies/own',
                         methods=['GET'])
@require_token
def list_own_emotlies(**kwargs):
    try:
        user = kwargs['user']
        emotlies = Emotly.objects(user=user.id).only("mood", "created_at")
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Create a new emotly for the current user.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies/new',
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
                         '/emotlies/show/<emotly_id>', methods=['GET'])
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
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/moods', methods=['GET'])
def list_moods():
    try:
        formatted_mood = [{"id": k, "value": v} for k, v in MOOD.items()]
        moods = response_handler(200, formatted_mood, 'moods')
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return moods
