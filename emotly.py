"""
Emotly

DEED
"""
import os
from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine
from userController import user_controller

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': os.environ['EMOTLY_DB_NAME']}
db = MongoEngine(app)

app.register_blueprint(user_controller)

@app.route("/")
def index():
    return "Ok"

@app.route("/echo/<echostr>")
def echo(echostr):
    return "Hello %s" % echostr

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
