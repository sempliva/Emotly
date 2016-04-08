"""
Emotly

DEED
"""
import os
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__, static_folder='../static',
            template_folder='../templates')
app.config["MONGODB_SETTINGS"] = {
    'host': os.environ['EMOTLY_DB_URI'],
}
app.secret_key = os.environ['EMOTLY_APP_SEC_SUPERSECRET']
app.config['SESSION_TYPE'] = 'filesystem'
db = MongoEngine(app)


@app.route("/")
def index():
    return render_template("page-home.html")

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)


# Import and register blueprints here

from Emotly.user_controller import user_controller

app.register_blueprint(user_controller)
