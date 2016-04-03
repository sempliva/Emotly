"""
Emotly

DEED
"""
import os
import bcrypt
from flask import Flask, request, render_template, flash
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ['EMOTLY_DB_URI'],
    'username': os.environ['EMOTLY_DB_USERNAME'],
    'password': os.environ['EMOTLY_DB_PASSWORD']
    'DB': os.environ['EMOTLY_DB_DBNAME']
}
app.secret_key = 'SECRETKEY'
app.config['SESSION_TYPE'] = 'filesystem'

db = MongoEngine(app)

# ******MODELS******


class User(db.Document):
    nickname = db.StringField(regex='^[a-z0-9A-Z]+$', min_length=6, max_length=15, required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(min_length=8, required=True)
    salt = db.StringField(required=True)

# ******ROUTE******

@app.route("/")
def index():
    return render_template("page-home.html")


@app.route("/signup", methods=["GET", "POST"])
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

    # TODO: This defaults to 12 rounds; should we have a configuration
    # parameter?
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(req_pwd, salt)
    user = User(nickname=req_nickname, password=hash_pwd, salt=salt,
                email=req_email)

    user.save()

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
