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

# Login Test Case

import unittest
import json
from emotly import app
from emotly import constants as CONSTANTS
from emotly.models import User
from emotly.utils import get_salt
from emotly.utils import verify_jwt_token, hash_password


# Controller: User Login.
class LoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_login_email_success(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_last_login_date_updated(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        user = User.objects.get(email=u.email)

        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        user2 = User.objects.get(email=u.email)

        self.assertNotEqual(user.last_login, user2.last_login)

    def test_login_nickname_success(self):
        salt = get_salt()
        u = User(nickname='testnickname',
                 email='email2@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'testnickname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_nickname_case_insensitive_success(self):
        salt = get_salt()
        u = User(nickname='testnickname',
                 email='email2@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'TESTNICKname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_nickname_case_insensitive2_success(self):
        salt = get_salt()
        u = User(nickname='TESTnickname',
                 email='email2@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'testnickname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_email_case_insensitive_success(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='Email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_email_case_insensitive2_success(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'EMail@emailTEST.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_space_in_nickname(self):
        salt = get_salt()
        u = User(nickname='testnickname',
                 email='email2@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'testnickname ',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

        user_data = {'user_id': 'testn  ickname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

        user_data = {'user_id': '  testnickname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_space_in_email(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com ',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

        user_data = {'user_id': 'email@emailtest. com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

        user_data = {'user_id': 'email @emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_non_secure(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_login_email_fail(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtestwrong.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'email@emailtestwrong.com',
                     'password': 'passwordwrong'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_nickname_fail(self):
        salt = get_salt()
        u = User(nickname='testnfail',
                 email='email22@emailtestwrong.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'testnfail',
                     'password': 'passwordwrong'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_user_not_registered(self):
        user_data = {'user_id': 'santaclaus@lostisland.com',
                     'password': 'hohoho'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 404)

    def test_login_email_not_confirmed(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@notconfirmed.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=False,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'email@notconfirmed.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_missing_data(self):
        user_data = {'password': 'passwordwrong'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 500)
