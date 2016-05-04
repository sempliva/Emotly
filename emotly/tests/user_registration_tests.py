"""
User Registration Test Case
"""
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
        pass

    def test_dummy(self):
        assert True

    def test_signup(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="nicknametest",
                               inputEmail="email@emailtest.com",
                               inputPassword="password"))
        assert (CONSTANTS.REGISTRATION_COMPLETED_CHECK_EMAIL).\
            encode('utf-8') in rv.data

    def test_signup_email_is_lower(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="nicknametest12",
                               inputEmail="Email1@EMAILTEST.com",
                               inputPassword="password"))
        user = User.objects.get(nickname="nicknametest12")
        self.assertEqual(user.email, "Email1@EMAILTEST.com".lower())

    def test_signup_incomplete_request(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="incompleterequest",
                               inputPassword="password"),
                           follow_redirects=True)
        assert (CONSTANTS.INTERNAL_SERVER_ERROR).encode('utf-8') in rv.data

    def test_signup_short_nickname(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="short",
                               inputEmail="email@short.com",
                               inputPassword="password"),
                           follow_redirects=True)
        assert (CONSTANTS.REGISTRAION_ERROR_INVALID_DATA).\
            encode('utf-8') in rv.data

    def test_signup_user_exist(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"),
                           follow_redirects=True)
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="nicknametest1",
                               inputEmail="email@nicknametest1.com",
                               inputPassword="password"),
                           follow_redirects=True)
        assert (CONSTANTS.REGISTRAION_ERROR_USER_EXISTS).\
            encode('utf-8') in rv.data
