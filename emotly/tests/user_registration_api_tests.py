"""
User Registration API Test Case
"""
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

    def test_dummy(self):
        assert True

    def test_signup(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname='nicknametest',
                               inputEmail='email@emailtest.com',
                               inputPassword='password'))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_signup_incomplete_request(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="incompleterequest",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 500)

    def test_signup_short_nickname(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="short",
                               inputEmail="email@short.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)

    def test_signup_user_exist(self):
        headers = {'content-type': 'application/json'}
        data = json.dumps(dict(inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"))
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           data=data,
                           headers=headers)
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + '/signup',
                           data=data,
                           headers=headers)
        self.assertEqual(rv.status_code, 400)
