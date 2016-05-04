"""
Token Model Test Case
"""
import unittest
import datetime
from mongoengine import NotUniqueError
from emotly import app
from emotly.models import User, Token

from emotly.utils import generate_confirmation_token
from emotly.controllers.user_controller import confirm_registration_email
from emotly import constants as CONSTANTS


# Model: Token.
class TokenModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_create_token(self):
        u = User(nickname='test12345',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        token = Token(token=token_string)
        u.confirmation_token = token
        self.assertTrue(u.save())

    def test_cannot_create_token_not_unique(self):
        u = User(nickname='testZ123456',
                 email='test_fake@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()

        # Try to save an user with a token string already used
        u2 = User(nickname='testZY123456',
                  email='test_fake2@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u2.confirmation_token = Token(token=token_string)
        self.assertRaises(NotUniqueError, u2.save)

    def test_confirm_email(self):
        u = User(nickname='test12345678910',
                 email='test3@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Email Confirmed' in rv.data

    def test_update_at_after_confirm_email(self):
        u = User(nickname='testupdateat',
                 email='test_update_at@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        user = User.objects.only("update_at").get(pk=u.id)
        self.assertTrue(user.update_at)

    def test_cannot_confirm_email_already_active(self):
        u = User(nickname='alreadyActive',
                 email='test_active@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        confirm_registration_email(u.confirmation_token.token)

        rv = self.app.get("/confirm_email/" + token_string)
        assert b'Error in confirming email.' in rv.data

    def test_cannot_confirm_email_token_too_old(self):
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now() -
                                     datetime.timedelta(days=2))
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Error in confirming email' in rv.data
