"""
Token Test Case
"""
import unittest
import datetime
import json
from mongoengine import NotUniqueError
from emotly import app
from emotly.models import User, Token

from emotly.utils import generate_confirmation_token, generate_jwt_token
from emotly.controllers.user_controller import confirm_registration_email
from emotly import constants as CONSTANTS


# Controller: Token.
class TokenTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    # Test confirm email
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

    # Test resend confirmation token
    def test_resend_token_confirmation_email(self):
        u = User(nickname='resendtoken',
                 email='resend_token@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(
            token=token_string, created_at=datetime.datetime.now() -
            datetime.timedelta(minutes=CONSTANTS.MINUTES_SINCE_LAST_EMAIL +
                               15))
        u.save()
        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 200)

    def test_resend_token_confirmation_nickname(self):
        u = User(nickname='resendtoken',
                 email='resend_token@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(
            token=token_string, created_at=datetime.datetime.now() -
            datetime.timedelta(minutes=CONSTANTS.MINUTES_SINCE_LAST_EMAIL +
                               15))
        u.save()
        data = {'user_id': u.nickname}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 200)

    def test_resend_token_confirmation_sent_in_the_last_x_minutes(self):
        u = User(nickname='resendtoken',
                 email='resend_token@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 400)

    def test_cannot_resend_token_confirmation_user_email_not_exists(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 404)

    def test_cannot_resend_token_confirmation_user_nickname_not_exists(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        data = {'user_id': u.nickname}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 404)

    def test_cannot_resend_token_confirmation_user_already_confirmed(self):
        u = User(nickname='resendtoken',
                 email='resend_token@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 400)

    def test_resend_token_confirmation_is_token_created_at_updated(self):
        u = User(nickname='resendtoken',
                 email='resend_token@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(
            token=token_string, created_at=datetime.datetime.now() -
            datetime.timedelta(minutes=CONSTANTS.MINUTES_SINCE_LAST_EMAIL +
                               15))
        u.save()
        user = User.objects.get(email=u.email)

        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))

        user2 = User.objects.get(email=u.email)
        self.assertNotEqual(user.confirmation_token.created_at,
                            user2.confirmation_token.created_at)

    def test_resend_token_confirmation_json_data_not_contains_user_id(self):
        u = User(nickname='testresend1',
                 email='test_resend1@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        data = {'this_is_not_user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data))
        self.assertEqual(rv.status_code, 500)

    def test_resend_token_confirmation_json_data_not_valid(self):
        u = User(nickname='testresend2',
                 email='test_resend2@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data="this isn't json")
        self.assertEqual(rv.status_code, 500)

    def test_resend_token_confirmation_no_json_data(self):
        u = User(nickname='testresend3',
                 email='test_resend3@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=False,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation')
        self.assertEqual(rv.status_code, 500)
