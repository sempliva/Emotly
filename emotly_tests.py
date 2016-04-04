"""
Emotly Test Suite
Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest, Emotly, pep8, glob
from Emotly.models import User
from mongoengine import ValidationError, NotUniqueError


# Simple page existance tests.
class BasicEmotlyPageCase(unittest.TestCase):

    # Runs the test client.
    def setUp(self):
        self.app = Emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_code_style(self):
        s = pep8.StyleGuide(quiet=True)
        res = s.check_files(glob.glob('Emotly/*.py'))
        if res.total_errors:
            print("*** WARNING ***: found %s style errors" % res.total_errors)

        # TODO: Enforcing the PEP8 tests is currently disabled;
        # replace the first 0 with res.total_errors to enable.
        self.assertEqual(0, 0, 'Found code style errors: run '
                         'pep8 on the files for details')

    def test_emotly_index(self):
        rv = self.app.get('/')
        assert b'Your life, your emotions' in rv.data

    def test_emotly_signup(self):
        rv = self.app.get('/signup')
        assert b'Signup' in rv.data


# Controller: User Registration
class EmotlyUserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_signup(self):
        rv = self.app.post('/signup',
                           data=dict(
                               inputNickname="nickname",
                               inputEmail="email@emailtest.com",
                               inputPassword="password"
                           )
                           )
        assert b'Registration completed!' in rv.data
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

            assert b'duplicate unique keys' in rv.data


# Tests for User model
class EmotlyUserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Emotly.app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_create_user(self):
        u = User(nickname='test12345',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        self.assertTrue(u.save())

    def test_cannot_create_user_nickname_too_long(self):
        u = User(nickname='VeryLongNicknameThatIsTooLong',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_no_nickname(self):
        u = User(email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_too_short(self):
        u = User(nickname='test',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex(self):
        u = User(nickname='test&@1235',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_nickname_not_match_validation_regex2(self):
        u = User(nickname='^^^$$$$$!!',
                 email='test@example.com',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_password(self):
        u = User(nickname='test123456', email='test@example.com', salt="salt")
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_salt(self):
        u = User(nickname='test123456',
                 email='test@example.com',
                 password="FakeUserPassword123"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_whitout_email(self):
        u = User(nickname='tesT123456',
                 password="FakeUserPassword123",
                 salt="salt"
                 )
        with self.assertRaises(ValidationError):
            u.save()

    def test_cannot_create_user_email_not_valid(self):
        u = User(nickname='test123456',
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
                  salt="salt"
                  )
        u.save()
        self.assertRaises(NotUniqueError, u2.save)

if __name__ == '__main__':
    unittest.main()
