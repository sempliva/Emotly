"""
Emotly

DEED
"""
import json
from flask import Blueprint, request, flash, jsonify, make_response
from flask.ext.mongoengine import MongoEngine
from functools import wraps
from emotly.models import User, Emotly, MOOD
from mongoengine import DoesNotExist
from emotly.controllers.user_controller import get_user_from_jwt_token
from emotly.controllers.user_controller import is_user_confirmed
from emotly.utils import verify_jwt_token


# Emotly Controller
emotly_controller = Blueprint('emotly_controller', __name__)


# Decorator used to check user and token for emotlies api
# and return the user to the original fn.
def require_token(api_method):
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        auth_token = request.headers.get('auth_token')
        if auth_token and verify_jwt_token(auth_token):
            try:
                user = get_user_from_jwt_token(auth_token)
                # Check if user is confirmed, return 403 if does not exist.
                user_confirmed = is_user_confirmed(user.id)
                if user_confirmed:
                    # Pass user as in the  kwargs to the original fn.
                    kwargs['user'] = user
                    return api_method(*args, **kwargs)
                return make_response(jsonify({'message': 'User error.'}),
                                     403)
            # If does not exist return 404.
            except DoesNotExist:
                return make_response(jsonify({'message':
                                              'Authentication error.'}),
                                     404)
        # If the request has no user token or it is not valid 403.
        return make_response(jsonify({'message': 'Unauthorized access.'}),
                             403)
    return check_api_key


# Retrieve the emotlies list.
@emotly_controller.route('/api/1.0/emotlies', methods=['GET'])
def list_emotlies():
    try:
        emotlies = Emotly.objects.all()
    except Exception:
        return make_response(jsonify({'message': 'Internal server error'}),
                             500)
    # At the moment serialize mood, creation date of the mood
    # and user nickname.
    return make_response(jsonify({'emotlies':
                                  [e.serialize() for e in emotlies]}), 200)


# Retrieve the current user's emotlies list.
@emotly_controller.route('/api/1.0/emotlies/own', methods=['GET'])
@require_token
def list_own_emotlies(**kwargs):
    try:
        user = kwargs['user']
        emotlies = Emotly.objects(user=user.id).only("mood", "created_at")
    except Exception:
        return make_response(jsonify({'message': 'Internal server error'}),
                             500)
    return make_response(jsonify({'emotlies':
                                  [e.serialize() for e in emotlies]}), 200)


# Create a new emotly for the current user.
@emotly_controller.route('/api/1.0/emotlies/new', methods=['POST'])
@require_token
def post_new_emotly(**kwargs):
    try:
        user = kwargs['user']
        data = json.loads(request.data.decode('utf-8'))
        emotly = Emotly(mood=data['mood'])
        emotly.user = user
        emotly.save()
    except Exception:
        return make_response(jsonify({'message': 'Internal server error'}),
                             500)
    return make_response(jsonify({'emotly': emotly.serialize()}), 200)


# Retrieve a specific emotly.
@emotly_controller.route('/api/1.0/emotlies/show/<emotly_id>', methods=['GET'])
@require_token
def get_emotly(emotly_id, **kwargs):
    try:
        emotly = Emotly.objects.only("mood", "created_at").get(id=emotly_id)
    except DoesNotExist:
        return make_response(jsonify({'message': 'Emotly error.'}), 404)
    except Exception:
        return make_response(jsonify({'message': 'Internal server error'}),
                             500)
    return make_response(jsonify({'emotly': emotly.serialize()}), 200)


# Retrieve the list of moods.
@emotly_controller.route('/api/1.0/moods', methods=['GET'])
def list_moods():
    try:
        formatted_mood = [{"id": k, "value": v}
                          for k, v in MOOD.items()]
        moods = make_response(jsonify({'moods': formatted_mood}), 200)
    except Exception:
        return make_response(jsonify({'message': 'Internal server error'}),
                             500)
    return moods
