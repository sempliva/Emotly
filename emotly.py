"""
Emotly

DEED
"""
import os
from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': os.environ['EMOTLY_DB_NAME']}
db = MongoEngine(app)

@app.route("/")
def index():
    return render_template("page-home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("page-signup.html")
    # TODO: Deal with the actual registration here?
    return "Unsupported"

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
