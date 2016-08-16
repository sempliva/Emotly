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

# Token Test Case

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
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token,
                          base_url='https://localhost')
        self.assertIn(CONSTANTS.EMAIL_CONFIRMED.encode('utf-8'), rv.data)

    def test_update_at_after_confirm_email(self):
        u = User(nickname='testupdateat',
                 email='test_update_at@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token,
                          base_url='https://localhost')
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

        rv = self.app.get("/confirm_email/" + token_string,
                          base_url='https://localhost')
        self.assertIn(CONSTANTS.ERROR_IN_CONFIRMING_EMAIL.encode('utf-8'),
                      rv.data)

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
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token,
                          base_url='https://localhost')
        self.assertIn(CONSTANTS.ERROR_IN_CONFIRMING_EMAIL.encode('utf-8'),
                      rv.data)

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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
        data = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(data["error_code"],
                         CONSTANTS.CODE_TOKEN_CONFIRMATION_ALREADY_SENT)

    def test_cannot_resend_token_confirmation_user_email_not_exists(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        data = {'user_id': u.email}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
        data = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(data["error_code"], CONSTANTS.CODE_USER_UNKNOW)

    def test_cannot_resend_token_confirmation_user_nickname_not_exists(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        data = {'user_id': u.nickname}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
        data = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(data["error_code"], CONSTANTS.CODE_USER_UNKNOW)

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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
        data = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(data["error_code"],
                         CONSTANTS.CODE_USER_ALREADY_CONFIRMED)

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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')

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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='https://localhost')
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
                          '/resend_email_confirmation',
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 500)

    # Test non-secure requests.
    def test_confirm_email_not_secure(self):
        u = User(nickname='test12345678910',
                 email='test3@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token,
                          base_url='http://localhost')

    def test_resend_token_confirmation_email_not_secure(self):
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
                          '/resend_email_confirmation', data=json.dumps(data),
                          base_url='http://localhost')
        data = json.loads(rv.data.decode("utf-8"))
        self.assertEqual(data["error_code"], CONSTANTS.CODE_REQUEST_INSECURE)
