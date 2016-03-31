"""
Emotly

DEED
"""
import os
import bcrypt
from flask import Flask, request, render_template, \
    abort, flash, redirect, url_for
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ['EMOTLY_DB_URI'],
    'username' : os.environ['EMOTLY_DB_USERNAME'],
    'password' : os.environ['EMOTLY_DB_PASSWORD']
}
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = MongoEngine(app)

########MODELS##########


class User(db.Document):
    nickname = db.StringField(min_length=6, unique = True)
    email = db.EmailField(required = True, unique = True)
    password = db.StringField(required = True)
    salt = db.StringField(required = True)

#######ROUTE###########


@app.route("/")
def index():
    return render_template("page-home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("page-signup.html")
    if request.method == "POST":
        return registerUser(request)

    return "Unsupported"

# @app.route('/register', methods=['POST'])
def registerUser(request):

    try:
        nickname = request.form['inputNickname']
        pwd = request.form['inputPassword'].encode('utf-8')
        email = request.form['inputEmail']
    except:
        flash("Bad request")
        return redirect(url_for('signup'))


    if len(User.objects.filter(email=email))>0:
        flash('User already exist')
        return redirect(url_for('signup'))

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pwd, salt)
    user = User(
        nickname=nickname,
        password=hash,
        salt=salt,
        email=email
    )
    try:
        user.save()
    except:
        flash('Bad parameters')
        return redirect(url_for('signup'))

    flash('Registration completed! Ceck your email :)')
    return redirect(url_for("index"))

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
