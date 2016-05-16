"""
MIT License

Copyright (c) 2016 Emotly Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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


# FIXME: Serving the WebApp Manifest in the root seems to
# be mandatory (or a bug in the implementation?), hence
# we mock the URL here (/manifest.json instead of
# /static/app/manifest.json).
# The base.html template also links /manifest.json.
@app.route("/manifest.json")
def serve_manifest():
    return app.send_static_file('app/manifest.json')


# This serves the main PWA app screen.
# We mock the URL by prepending /static to address the
# ServiceWorker's scope.
@app.route("/static/app/pwa")
def serve_app():
    return render_template("app-home.html")


@app.route("/static/app/sw.js")
def serve_sw():
    return app.send_static_file('app/js/sw.js')


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
from emotly.controllers.emotly_controller import emotly_controller

app.register_blueprint(user_controller)
app.register_blueprint(emotly_controller)
# app.register_blueprint(yuppy_blueprint)
