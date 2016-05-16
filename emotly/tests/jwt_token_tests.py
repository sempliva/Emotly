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


# TODO: Add more coverage for JWT.
class JWTTokenTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_gen_JWT_token(self):
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token = generate_jwt_token(u)
        assert token is not None

    def test_verify_JWT_valid_token(self):
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token = generate_jwt_token(u)
        assert verify_jwt_token(str(token))

    def test_verify_JWT_invalid_token(self):
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        token = generate_jwt_token(u)
        token = json.loads(token)
        token["payload"]["nickname"] = "iwanttohack"
        token = json.dumps(token)
        assert not verify_jwt_token(str(token))

    def test_verify_JWT_expired_token(self):
        expired_time = datetime.datetime.now() - datetime.timedelta(hours=1000)
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 last_login=expired_time,
                 salt="salt")
        token = generate_jwt_token(u)
        assert not verify_jwt_token(str(token))
