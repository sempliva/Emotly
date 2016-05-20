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

# Emotly Model Test Case

import unittest
import datetime
import time
from mongoengine import ValidationError
from emotly import app
from emotly.models import User, Emotly, MOOD


# Model: Emotly.
class EmotlyModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_create_emotly(self):
        u = User(nickname='testemotly',
                 email='test_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly(mood=1)
        emotly.user = u
        self.assertTrue(emotly.save())

    def test_create_3_emotly(self):
        u = User(nickname='testemotly',
                 email='test_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now,
                 salt="salt")
        u.save()

        emotly = Emotly(mood=1)
        emotly.user = u
        emotly.save()
        time.sleep(1)  # sleep time in seconds

        emotly1 = Emotly(mood=2)
        emotly1.user = u
        emotly1.save()
        time.sleep(1)  # sleep time in seconds

        emotly2 = Emotly(mood=3)
        emotly2.user = u
        emotly2.save()
        self.assertNotEqual(emotly.created_at, emotly1.created_at)
        self.assertNotEqual(emotly1.created_at, emotly2.created_at)

    def test_cannot_create_emotly_whitout_user(self):
        emotly = Emotly(mood=2)
        with self.assertRaises(ValidationError):
            emotly.save()

    def test_cannot_create_emotly_whitout_mood(self):
        u = User(nickname='testmood',
                 email='test_mood@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly()
        emotly.user = u
        with self.assertRaises(ValidationError):
            emotly.save()

    def test_cannot_create_emotly_mood_not_valid(self):
        u = User(nickname='testinvalid',
                 email='test_mood_invalid@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly(mood=len(MOOD) + 1)
        emotly.user = u
        with self.assertRaises(ValidationError):
            emotly.save()
