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

from emotly import db
import datetime
import bcrypt
from emotly import constants as CONSTANTS


class Token(db.EmbeddedDocument):
    token = db.StringField(unique=True, sparse=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)


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

    # Return true if a given password match with user password.
    @staticmethod
    def verify_password(user, password):
        enc_password = user.password.encode('utf-8')
        return bcrypt.hashpw(password, enc_password) == enc_password


MOOD = {1: "sad", 2: "happy", 3: "proud", 4: "tired", 5: "hopeful",
        6: "in love", 7: "surprised", 8: "fascinated", 9: "amazed",
        10: "annoyed", 11: "disappointed", 12: "emotional", 13: "relaxed",
        14: "hungry", 15: "sleepy", 16: "exhausted", 17: "depressed",
        18: "bored", 19: "lucky", 20: "inspired"}


class Location(db.EmbeddedDocument):
    coord = db.PointField(required=False)
    accuracy = db.FloatField(required=False)
    location_name = db.StringField(min_length=3, required=False)


class Emotly(db.Document):
    mood = db.IntField(required=True, choices=list(MOOD))
    user = db.ReferenceField(User, required=True)
    created_at = db.DateTimeField(default=datetime.datetime.now)
    geodata = db.EmbeddedDocumentField(Location)

    # Serialize object formatting date and mood and user if present.
    def serialize(self):
        dictionary = {'mood': MOOD[self.mood],
                      'created_at': self.created_at.strftime(
                          CONSTANTS.DATE_FORMAT)}
        if self.user:
            dictionary['nickname'] = self.user.nickname
        if self.geodata:
            dictionary['coord'] = self.geodata.to_mongo().to_dict()
        return dictionary
