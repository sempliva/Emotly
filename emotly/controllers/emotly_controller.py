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

import json
from flask import Blueprint, request, flash
from emotly import constants as CONSTANTS
from flask.ext.mongoengine import MongoEngine
from emotly.models import User, Emotly, MOOD, Location
from mongoengine import DoesNotExist
from emotly.utils import get_user_from_jwt_token, response_handler
from emotly.utils import require_token, valid_json, require_https


# Emotly Controller
emotly_controller = Blueprint('emotly_controller', __name__)


# Retrieve the emotlies list.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies',
                         methods=['GET'])
@require_https
def list_emotlies():
    try:
        emotlies = Emotly.objects.only("user",
                                       "created_at",
                                       "mood",
                                       "geodata").all()
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    # At the moment serialize mood, creation date of the mood
    # and user nickname.
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Retrieve the current user's emotlies list.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies/own',
                         methods=['GET'])
@require_https
@require_token
def list_own_emotlies(**kwargs):
    try:
        user = kwargs['user']
        emotlies = Emotly.objects(user=user.id).only("mood",
                                                     "created_at",
                                                     "geodata")
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, [e.serialize() for e in emotlies], 'emotlies')


# Create a new emotly for the current user.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/emotlies/new',
                         methods=['POST'])
@require_https
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
        if 'geodata' in data:
            location = Location()
            location.coord = data['geodata']['coord']
            if 'accuracy' in data['geodata']:
                location.accuracy = data['geodata']['accuracy']
            if 'location_name' in data['geodata']:
                location.location_name = data['geodata']['location_name']
            emotly.geodata = location
        emotly.save()
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, emotly.serialize(), 'emotly')


# Retrieve a specific emotly.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX +
                         '/emotlies/show/<emotly_id>', methods=['GET'])
@require_https
@require_token
def get_emotly(emotly_id, **kwargs):
    try:
        emotly = Emotly.objects.only("mood",
                                     "created_at",
                                     "geodata",
                                     "user").get(id=emotly_id)
    except DoesNotExist:
        return response_handler(CONSTANTS.CODE_EMOTLY_NONEXISTENT)
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, emotly.serialize(), 'emotly')


# Retrieve the last emotly of a specific user.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/user/<nickname>',
                         methods=['GET'])
@require_https
def get_user_details_last_emotly(nickname, **kwargs):
    try:
        u = User.objects.get(nickname__iexact=nickname)
        emotly = Emotly.objects(user=u.id).order_by("-created_at")\
            .only("user", "created_at", "mood", "geodata").first()
        if emotly is None:
            return response_handler(CONSTANTS.CODE_EMOTLY_NONEXISTENT)
    except DoesNotExist:
        return response_handler(CONSTANTS.CODE_USER_UNKNOW)
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return response_handler(200, emotly.serialize(), 'emotly')


# Retrieve the list of moods.
@emotly_controller.route(CONSTANTS.REST_API_PREFIX + '/moods', methods=['GET'])
@require_https
def list_moods():
    try:
        formatted_mood = [{"id": k, "value": v} for k, v in MOOD.items()]
        moods = response_handler(200, formatted_mood, 'moods')
    except Exception:
        return response_handler(500, CONSTANTS.INTERNAL_SERVER_ERROR)
    return moods
