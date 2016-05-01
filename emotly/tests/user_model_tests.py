"""
User Model Test Case
"""
import unittest
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
