"""
Emotly Test Suite

Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest, emotly
from models import User
from mongoengine import ValidationError, NotUniqueError

# Simple page existance tests.
class BasicEmotlyPageCase(unittest.TestCase):

    # Runs the test client.
    def setUp(self):
        self.app = emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_emotly_index(self):
        rv = self.app.get('/')
        assert b'Your life, your emotions' in rv.data

    def test_emotly_signup(self):
        rv = self.app.get('/signup')
        assert b'Signup' in rv.data

# TODO: User Registration tests.
#class EmotlyUserRegistrationTestCase(unittest.TestCase):
#    def setUp(self):
#        self.app = emotly.app.test_client()
#
#    def tearDown(self):
#        pass
#
#    def test_dummy(self):
#        assert True
#

    # Tests for User model
    def test_create_user(self):
        u = User(nickname='test12345', email='test@example.com', password="abc", salt="salt")
        self.assertTrue(u.save())

    def test_cannot_create_user_nickname_too_short(self):
        u = User(nickname='test', email='test@example.com', password="abc", salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_password(self):
        u = User(nickname='test', email='test@example.com', salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_salt(self):
        u = User(nickname='test', email='test@example.com', password="abc")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_email(self):
        u = User(nickname='test', password="abc", salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_duplicate_key(self):
        u = User(nickname='test_user', email='test_duplicate@example.com', password="abc", salt="salt")
        u2 = User(nickname='test_user_2', email='test_duplicate@example.com', password="abc", salt="salt")
        u.save()
        self.assertRaises(NotUniqueError, u2.save)

    def test_cannot_create_user_nickname_duplicate_key(self):
        u = User(nickname='test_nickname', email='test_nickname@example.com', password="abc", salt="salt")
        u2 = User(nickname='test_nickname', email='test_nickname2@example.com', password="abc", salt="salt")
        u.save()
        self.assertRaises(NotUniqueError, u2.save)

if __name__ == '__main__':
    unittest.main()
