"""
Emotly

DEED
"""
import os
from flask import Flask, request, render_templatei, abort
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine
import bcrypt


app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': os.environ['EMOTLY_DB_NAME']}
db = MongoEngine(app)

########MODELS##########


class User(db.Document):
    nickname = db.StringField(min_length=6)
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
    # TODO: Deal with the actual registration here?
    return "Unsupported"

@app.route('/singup', methods=['POST'])
def signUp():

    try:
        nickname = request.form['username']
        pwd = request.form['pwd'].encode('utf-8')
        email = request.form['email']
    except:
        abort(401)

    if len(User.objects.filter(email=email))>0:
        return 'user already exist'

    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(pwd, salt)
    user = User(
        nickname=nickname,
        password=hash,
        salt=salt,
        email=email
    )
    user.save()
    return 'OK'
# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
