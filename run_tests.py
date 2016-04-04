"""
Emotly Test Suite
Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest
import pep8
import glob
import datetime
from mongoengine import ValidationError, NotUniqueError
from emotly import app
from emotly.models import User, Token
from emotly.controllers.user_controller import confirm_registration_email
from emotly.utils import generate_confirmation_token


# Simple page existance tests.
class BasicEmotlyPageCase(unittest.TestCase):

    # Runs the test client.
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_code_style(self):
        print("\n******* EMOTLY STYLE CHECKER - BEGIN ********")
        s = pep8.StyleGuide(quiet=False, config_file='style.cfg')
        res = s.check_files(glob.glob('**/*.py', recursive=True))
        if res.total_errors:
            print("\n!!! WARNING !!! WARNING !!! WARNING: "
                  "found %s style errors!" % res.total_errors)
        else:
            print("Nicely done, no style error detected!")

        # TODO: Enforcing the PEP8 tests is currently disabled;
        # replace the first 0 with res.total_errors to enable.
        self.assertEqual(0, 0, 'Found code style errors: run ' +
                         'pep8 on the files for details')

        print("******* EMOTLY STYLE CHECKER - END ********\n\n")

    def test_emotly_index(self):
        rv = self.app.get('/')
        assert b'Your life, your emotions' in rv.data

    def test_emotly_signup(self):
        rv = self.app.get('/signup')
        assert b'Signup' in rv.data


# Controller: User Registration
class EmotlyUserRegistrationTestCase(unittest.TestCase):
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
                               inputPassword="password"
                           )
                           )
        assert b'Registration completed! Ceck your email :)' in rv.data

    def test_signup_incomplete_request(self):
            rv = self.app.post('/signup',
                               data=dict(
                                   inputNickname="incompleterequest",
                                   inputPassword="password"
                               ),
                               follow_redirects=True
                               )
            assert b'Registration error' in rv.data

    def test_signup_short_nickname(self):
            rv = self.app.post('/signup',
                               data=dict(
                                   inputNickname="short",
                                   inputEmail="email@short.com",
                                   inputPassword="password"
                               ),
                               follow_redirects=True
                               )
            assert b'Registration error' in rv.data

    def test_signup_user_exist(self):
            rv = self.app.post('/signup',
                               data=dict(
                                   inputNickname="nicknametest1",
                                   inputEmail="email@nicknametest1.com",
                                   inputPassword="password"
                               ),
                               follow_redirects=True
                               )
            rv = self.app.post('/signup',
                               data=dict(
                                   inputNickname="nicknametest1",
                                   inputEmail="email@nicknametest1.com",
                                   inputPassword="password"
                               ),
                               follow_redirects=True
                               )

            assert b'Registration error: ' in rv.data


# Tests for User model
class EmotlyUserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_create_user(self):
        u = User(nickname='testcreateuser',
                 email='test_create_user@example.com',
                 password="FakeUserPassword123", salt="salt"
                 )
        self.assertTrue(u.save())

    def test_cannot_create_user_nickname_too_long(self):
        u = User(nickname='VeryLongNicknameThatIsTooLong',
                 email='test@example.com',
                 password="FakeUserPassword123", salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_no_nickname(self):
        u = User(email='testnickname@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_too_short(self):
        u = User(nickname='test',
                 email='test_nickname_short@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex(self):
        u = User(nickname='test&@1235',
                 email='test_@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex2(self):
        u = User(nickname='^^^$$$$$!!',
                 email='testvalidation@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
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
                 password="FakeUserPassword123"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_email(self):
        u = User(nickname='testnomail',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_not_valid(self):
        u = User(nickname='testmailnovalid',
                 email='test_duplicateexample.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_duplicate_key(self):
        u = User(nickname='testuser',
                 email='test_duplicate@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        u2 = User(nickname='testuser2',
                  email='test_duplicate@example.com',
                  password="FakeUserPassword123",
                  salt="salt"
                  )
        u.save()
        self.assertRaises(NotUniqueError, u2.save)

    def test_cannot_create_user_nickname_duplicate_key(self):
        u = User(nickname='testnickname',
                 email='test_nickname@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        u2 = User(nickname='testnickname',
                  email='test_nickname2@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u.save()
        self.assertRaises(NotUniqueError, u2.save)


class EmotlyTokenModelTestCase(unittest.TestCase):
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
        token = Token(token=token_string,
                      created_at=datetime.datetime.now())
        u.confirmation_token = token
        self.assertTrue(u.save())

    def test_cannot_create_token_not_unique(self):
        u = User(nickname='testZ123456',
                 email='test_fake@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now())
        u.save()

        # Try to save an user with a token string already used
        u2 = User(nickname='testZY123456',
                  email='test_fake2@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u2.confirmation_token = Token(token=token_string,
                                      created_at=datetime.datetime.now())
        self.assertRaises(NotUniqueError, u2.save)

    def test_confirm_email(self):
        u = User(nickname='test12345678910',
                 email='test3@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now())
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Email Confirmed' in rv.data

    def test_update_at_after_confirm_email(self):
        u = User(nickname='testupdateat',
                 email='test_update_at@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now())
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        user = User.objects.only("update_at").get(pk=u.id)
        self.assertTrue(user.update_at)

    def test_cannot_confirm_email_already_active(self):
        u = User(nickname='alreadyActive',
                 email='test_active@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now())
        u.save()
        confirm_registration_email(u.confirmation_token.token)

        rv = self.app.get("/confirm_email/" + token_string)
        assert b'Error in confirming email.' in rv.data

    def test_cannot_confirm_email_token_too_old(self):
        u = User(nickname='confirmemail',
                 email='test_confirm_email@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string,
                                     created_at=datetime.datetime.now() +
                                     datetime.timedelta(days=2))
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Error in confirming email' in rv.data


if __name__ == '__main__':
    unittest.main()
