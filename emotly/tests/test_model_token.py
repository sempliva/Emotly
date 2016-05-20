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

# Token Model Test Case

import unittest
import datetime
import time
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

    def test_create_3_token(self):
        token_string = generate_confirmation_token('test@example.com')
        token = Token(token=token_string)
        time.sleep(1)  # sleep time in seconds
        token1 = Token(token=token_string)
        time.sleep(1)  # sleep time in seconds
        token2 = Token(token=token_string)
        self.assertNotEqual(token.created_at, token1.created_at)
        self.assertNotEqual(token1.created_at, token2.created_at)

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
