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

# User Registration Test Case

import unittest
from emotly import app
from emotly import constants as CONSTANTS
from emotly.models import User


# Controller: User Registration.
class UserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects(nickname="nicknametest").delete()
        User.objects(nickname="nicknametest1").delete()
        User.objects(nickname="nicknametest12").delete()
        pass

    def test_signup(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="nicknametest",
                               inputEmail="email@emailtest.com",
                               inputPassword="password"))
        self.assertIn(CONSTANTS.REGISTRATION_COMPLETED_CHECK_EMAIL.
                      encode('utf-8'), rv.data)

    def test_signup_email_is_lower(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="nicknametest12",
                               inputEmail="Email1@EMAILTEST.com",
                               inputPassword="password"))
        user = User.objects.get(nickname="nicknametest12")
        self.assertEqual(user.email, "Email1@EMAILTEST.com".lower())

    def test_signup_incomplete_request(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="incompleterequest",
                               inputPassword="password"),
                           follow_redirects=True)
        self.assertIn(CONSTANTS.INTERNAL_SERVER_ERROR.encode('utf-8'), rv.data)

    def test_signup_short_nickname(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="short",
                               inputEmail="email@short.com",
                               inputPassword="password"),
                           follow_redirects=True)
        self.assertIn(CONSTANTS.REGISTRAION_ERROR_INVALID_DATA.
                      encode('utf-8'), rv.data)

    def test_cannot_signup_space_in_nickname(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="space in nickname ",
                               inputEmail="email@spase.com",
                               inputPassword="password"),
                           follow_redirects=True)
        self.assertIn(CONSTANTS.REGISTRAION_ERROR_INVALID_DATA.
                      encode('utf-8'), rv.data)

    def test_cannot_signup_space_in_email(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="spaceinemail",
                               inputEmail="email@spase.com ",
                               inputPassword="password"),
                           follow_redirects=True)
        self.assertIn(CONSTANTS.REGISTRAION_ERROR_INVALID_DATA.
                      encode('utf-8'), rv.data)

    def test_signup_user_exist(self):
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"),
                           follow_redirects=True)
        rv = self.app.post('/signup',
                           base_url='https://localhost',
                           data=dict(
                               inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"),
                           follow_redirects=True)
        self.assertIn(CONSTANTS.REGISTRAION_ERROR_USER_EXISTS.
                      encode('utf-8'), rv.data)

    # Test non-secure requests.
    def test_signup_non_secure(self):
        rv = self.app.post('/signup',
                           base_url='http://localhost',
                           data=dict(
                               inputNickname="nicknametest",
                               inputEmail="email@emailtest.com",
                               inputPassword="password"))
        self.assertIn(CONSTANTS.NOT_HTTPS_REQUEST.encode('utf-8'), rv.data)
