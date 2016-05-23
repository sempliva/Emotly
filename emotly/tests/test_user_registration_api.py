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

# User Registration API Test Case

import unittest
import json
from emotly import app
from emotly import constants as CONSTANTS
from emotly.models import User


# Controller: User Registration REST API
class UserRegistrationAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()
        pass

    def test_signup(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname='nicknametest',
                               inputEmail='email@emailtest.com',
                               inputPassword='password'))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_signup_email_is_lower(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname='nicknametest12',
                               inputEmail='Email1@EMAILTEST.com',
                               inputPassword='password'))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        user = User.objects.get(nickname="nicknametest12")
        self.assertEqual(user.email, "Email1@EMAILTEST.com".lower())

    def test_signup_incomplete_request(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="incompleterequest",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 500)

    def test_signup_short_nickname(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="short",
                               inputEmail="email@short.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

    def test_cannot_signup_space_in_nickname(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="space in nickname ",
                               inputEmail="email@short.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

    def test_cannot_signup_space_in_email(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="spaceinemail",
                               inputEmail="email@short.com ",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

        data = json.dumps(dict(inputNickname="spaceinemail",
                               inputEmail="email@short .com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

        data = json.dumps(dict(inputNickname="spaceinemail",
                               inputEmail="email @short.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

    def test_signup_user_exist(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='https://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

    # Test non-secure requests.
    def test_signup_non_secure(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname='nicknametest',
                               inputEmail='email@emailtest.com',
                               inputPassword='password'))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           base_url='http://localhost', data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 403)
