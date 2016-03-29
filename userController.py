from flask import Blueprint, request, abort
from flask.ext.mongoengine import MongoEngine
from models import User
import bcrypt

user_controller = Blueprint('user_controller', __name__)

@user_controller.route('/singup', methods=['POST'])
def signUp():
    try:
        nickname = request.form['username']
        pwd = request.form['pwd']
        email = request.form['email']
    except:
        abort(401)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password, salt)
    user = User(
        nickname = nickname,
        password = hash,
        salt = salt,
        email = email
    )
