"""
JWT Token Test Case
"""
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
