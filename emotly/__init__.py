"""
Emotly

DEED
"""
import os
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine


# Define the WSGI application object.
app = Flask(__name__)

# Load the global configuration.
app.config.from_object('config')

# Start MongoEngine and bind it to app.
db = MongoEngine(app)


@app.route("/")
def index():
    return render_template("page-home.html")

# Gunicorn support.
app.wsgi_app = ProxyFix(app.wsgi_app)

# Blueprints registration.
#
# Register all the new blueprints here.
#
# The module is being imported here because of the way 'db' is
# declared at the beginning of this file.
#
from emotly.controllers.user_controller import user_controller

app.register_blueprint(user_controller)
# app.register_blueprint(yuppy_blueprint)
