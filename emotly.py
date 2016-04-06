"""
Emotly

DEED
"""
import os
import bcrypt
import hashlib, datetime
from flask import Flask, request, render_template, flash
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine
from postmark import PMMail
from mongoengine import DoesNotExist

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ['EMOTLY_DB_URI'],
}
app.secret_key = os.environ['EMOTLY_APP_SEC_SUPERSECRET']
app.config['SESSION_TYPE'] = 'filesystem'

db = MongoEngine(app)


# ******MODELS******

class Token(db.EmbeddedDocument):
    token = db.StringField(unique=True, sparse=True)
    created_at = db.DateTimeField(required=True)


class User(db.Document):
    nickname = db.StringField(regex='^[a-z0-9A-Z]+$',
                              min_length=6, max_length=15,
                              required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(min_length=8, required=True)
    salt = db.StringField(required=True)
    confirmed_email = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    update_at = db.DateTimeField()
    last_login = db.DateTimeField()
    confirmation_token = db.EmbeddedDocumentField(Token)


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

    rnds = int(os.environ['EMOTLY_APP_SEC_ROUNDS']) if\
            'EMOTLY_APP_SEC_ROUNDS' in os.environ else 12
    salt = bcrypt.gensalt(rnds)
    hash_pwd = bcrypt.hashpw(req_pwd, salt)
    user = User(nickname=req_nickname, password=hash_pwd, salt=salt,
                email=req_email)

    token_string = generate_token(user.email)
    user.confirmation_token = Token(token=token_string,
                                    created_at=datetime.datetime.now())
    user.save()
    send_email_confirmation(user.email, token_string)


@app.route("/confirm_email/<confirmation_token>")
def confirm_email(confirmation_token):
    try:
        confirm_registration_email(confirmation_token)
        flash('Email Confirmed')
    except DoesNotExist as e:
        flash('Error in confirmating email. Please, Log In and check if you '
              'are already confirmed or resend a confirmation email. %s' % e)
    return render_template("page-home.html")


def generate_token(email):
    token_string = hashlib.sha224(bcrypt.gensalt(12) + email.encode('utf-8') +
                                  datetime.datetime.now().strftime("%I:%M:%S")
                                                         .encode('utf-8') +
                                  bcrypt.gensalt(12)).hexdigest()
    return token_string


def send_email_confirmation(email, confirmation_token):
    message = PMMail(api_key=os.environ['POSTMARK_API_TOKEN'],
                     subject="Hello from Emotly.com",
                     sender=os.environ['POSTMARK_SENDER'],
                     to=email,
                     text_body="Welcome to Emotly.com. Please confirm your email in the next 24 hours. click on https://emotly.herokuapp.com/confirm_email/"+confirmation_token,
                     tag="hello")
    message.send()


def confirm_registration_email(confirmation_token):
    time_range = datetime.datetime.now()+datetime.timedelta(days=1)
    user = User.objects.get(confirmation_token__token=confirmation_token,
                            confirmation_token__created_at__lte=time_range)
    User.objects.get(pk=user.id).update(confirmed_email=True,
                                        unset__confirmation_token=1,
                                        update_at=datetime.datetime.now())

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug='EMOTLY_APP_DEBUG_ENABLE' in os.environ)
