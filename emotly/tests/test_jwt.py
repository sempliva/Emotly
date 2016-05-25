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

# JWT Token Test Case

import unittest
import datetime
import json
from emotly import app
from emotly.models import User
from emotly.utils import generate_confirmation_token
from emotly.utils import generate_jwt_token, verify_jwt_token


# TODO: Add more coverage. For example: stale token, valid
#       and invalid storek tokens, etc...
class JWTTokenTestCases(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.regular_user = User(nickname='confirmemail',
                                 email='test_confirm_email@example.com',
                                 password="FakeUserPassword123",
                                 salt="salt")
        self.regular_token = generate_jwt_token(self.regular_user)

    def tearDown(self):
        pass

    def test_generated_jwt_not_none(self):
        self.assertIsNotNone(self.regular_token)

    def test_generated_jwt_verified(self):
        self.assertTrue(verify_jwt_token(str(self.regular_token)))

    def test_hijacked_token(self):
        token = json.loads(self.regular_token)
        token["payload"]["nickname"] = "iwanttohack"
        token = json.dumps(token)

        self.assertFalse(verify_jwt_token(str(token)))

    def test_verify_JWT_expired_token(self):
        expired_time = datetime.datetime.now() - datetime.timedelta(hours=1000)
        self.regular_user.last_login = expired_time
        regenerated_token = generate_jwt_token(self.regular_user)

        self.assertFalse(verify_jwt_token(str(regenerated_token)))
