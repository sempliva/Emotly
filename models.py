from emotly import db

class User(db.Document):
    nickname = db.StringField(min_length=6, unique = True)
    email = db.EmailField(required = True, unique = True)
    password = db.StringField(required = True)
    salt = db.StringField(required = True)