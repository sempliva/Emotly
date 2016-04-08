"""
Emotly

DEED
"""
from emotly import db


class User(db.Document):
    nickname = db.StringField(regex='^[a-z0-9A-Z]+$',
                              min_length=6, max_length=15,
                              required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(min_length=8, required=True)
    salt = db.StringField(required=True)
