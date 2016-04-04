import os
import bcrypt
from flask import Blueprint, request, render_template, flash
from Emotly.models import User


user_controller = Blueprint('user_controller',
                            __name__)


@user_controller.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("page-signup.html")
    try:
        register_user(request)
        flash('Registration completed! Ceck your email :)')
    # TODO: Emotly-specific exception for human readable errors.
    # TODO: DO _NOT_ forget to update the negative test cases!
    except Exception as e:
        flash('Registration error: %s' % e)
    return render_template("page-home.html")


def register_user(req):
    req_nickname = req.form['inputNickname']
    req_pwd = req.form['inputPassword'].encode('utf-8')
    req_email = req.form['inputEmail']

    rnds = int(os.environ['EMOTLY_APP_SEC_ROUNDS']) if\
        'EMOTLY_APP_SEC_ROUNDS' in os.environ else 12
    salt = bcrypt.gensalt(rnds)
    hash_pwd = bcrypt.hashpw(req_pwd, salt)
    user = User(nickname=req_nickname, password=hash_pwd, salt=salt,
                email=req_email)

    user.save()
