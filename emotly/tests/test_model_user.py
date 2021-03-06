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

# User Model Test Case

import unittest
import datetime
import time
from mongoengine import ValidationError, NotUniqueError
from emotly import app
from emotly import constants as CONSTANTS
from emotly.models import User


# Model: User.
class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_create_user(self):
        u = User(nickname='testcreateuser',
                 email='test_create_user@example.com',
                 password="FakeUserPassword123", salt="salt")
        self.assertTrue(u.save())

    def test_create_3_user(self):
        u = User(nickname='testemotly',
                 email='test_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        time.sleep(1)  # sleep time in seconds
        u1 = User(nickname='testemotly1',
                  email='test_emotly1@example.com',
                  password="FakeUserPassword123",
                  confirmed_email=True,
                  last_login=datetime.datetime.now(),
                  salt="salt")
        u1.save()
        time.sleep(1)  # sleep time in seconds
        u2 = User(nickname='testemotly2',
                  email='test_emotly2@example.com',
                  password="FakeUserPassword123",
                  confirmed_email=True,
                  last_login=datetime.datetime.now(),
                  salt="salt")
        u2.save()
        self.assertNotEqual(u.created_at, u1.created_at)
        self.assertNotEqual(u1.created_at, u2.created_at)

    def test_cannot_create_user_nickname_too_long(self):
        u = User(nickname='VeryLongNicknameThatIsTooLong',
                 email='test@example.com',
                 password="FakeUserPassword123", salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_no_nickname(self):
        u = User(email='testnickname@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_too_short(self):
        u = User(nickname='test',
                 email='test_nickname_short@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex(self):
        u = User(nickname='test&@1235',
                 email='test_@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex2(self):
        u = User(nickname='^^^$$$$$!!',
                 email='testvalidation@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_password(self):
        u = User(nickname='testnopsw',
                 email='testnopassword@example.com',
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_salt(self):
        u = User(nickname='testnosalt',
                 email='testnosalt@example.com',
                 password="FakeUserPassword123")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_email(self):
        u = User(nickname='testnomail',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_not_valid(self):
        u = User(nickname='testmailnovalid',
                 email='test_duplicateexample.com',
                 password="FakeUserPassword123",
                 salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_duplicate_key(self):
        u = User(nickname='testuser',
                 email='test_duplicate@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        u2 = User(nickname='testuser2',
                  email='test_duplicate@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u.save()
        self.assertRaises(NotUniqueError, u2.save)

    def test_cannot_create_user_nickname_duplicate_key(self):
        u = User(nickname='testnickname',
                 email='test_nickname@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        u2 = User(nickname='testnickname',
                  email='test_nickname2@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u.save()
        self.assertRaises(NotUniqueError, u2.save)
