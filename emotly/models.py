"""
Emotly

DEED
"""
from emotly import db
import datetime


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
