"""
Emotly

DEED
"""
from emotly import db
import datetime
import bcrypt
from emotly import constants as CONSTANTS


class Token(db.EmbeddedDocument):
    token = db.StringField(unique=True, sparse=True)
    created_at = db.DateTimeField(default=datetime.datetime.now())


class User(db.Document):
    nickname = db.StringField(regex='^[a-z0-9A-Z]+$',
                              min_length=6, max_length=15,
                              required=True, unique=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(min_length=8, required=True)
    salt = db.StringField(required=True)
    confirmed_email = db.BooleanField(default=False)
    created_at = db.DateTimeField(default=datetime.datetime.now())
    update_at = db.DateTimeField()
    last_login = db.DateTimeField()
    confirmation_token = db.EmbeddedDocumentField(Token)

    # Return true if a given password match with user password.
    @staticmethod
    def verify_password(user, password):
        enc_password = user.password.encode('utf-8')
        return bcrypt.hashpw(password, enc_password) == enc_password

    # Used to format user's data in a more readable fashion.
    def serialize(self):
        return {'nickname': self.nickname}

MOOD = {1: "sad", 2: "happy", 3: "proud", 4: "tired", 5: "hopeful",
        6: "in love", 7: "surprised", 8: "fascinated", 9: "amazed"}


class Emotly(db.Document):
    mood = db.IntField(required=True, choices=list(MOOD))
    user = db.ReferenceField(User, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now())

    # TODO Change in something better.
    # Serialize object formatting date and mood and user if present.
    def serialize(self):
        if self.user:
            return {'mood': MOOD[self.mood],
                    'created_at': self.created_at
                    .strftime(CONSTANTS.DATE_FORMAT),
                    'user': self.user.serialize()}
        return {'mood': MOOD[self.mood],
                'created_at': self.created_at
                .strftime(CONSTANTS.DATE_FORMAT)}
