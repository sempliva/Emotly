"""
Emotly

DEED
"""
from flask import Flask, request
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)

@app.route("/")
def index():
    return "Ok"

# Gunicorn
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
    app.run(debug=True)
