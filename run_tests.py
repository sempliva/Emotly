"""
Emotly Test Suite
Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest
import pep8
import glob
import datetime
import json
from mongoengine import ValidationError, NotUniqueError
from emotly import app
from emotly.models import User, Token, Emotly, MOOD
from emotly.controllers.user_controller import confirm_registration_email
from emotly.utils import generate_confirmation_token
from emotly.utils import generate_jwt_token, verify_jwt_token, hash_password
from emotly.utils import get_salt
from emotly import constants as CONSTANTS


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
                               inputPassword="password"))
        assert (CONSTANTS.REGISTRATION_COMPLETED_CHECK_EMAIL).\
            encode('utf-8') in rv.data

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


# Tests for User model
class EmotlyUserModelTestCase(unittest.TestCase):
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
        token = Token(token=token_string)
        u.confirmation_token = token
        self.assertTrue(u.save())

    def test_cannot_create_token_not_unique(self):
        u = User(nickname='testZ123456',
                 email='test_fake@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()

        # Try to save an user with a token string already used
        u2 = User(nickname='testZY123456',
                  email='test_fake2@example.com',
                  password="FakeUserPassword123",
                  salt="salt")
        u2.confirmation_token = Token(token=token_string)
        self.assertRaises(NotUniqueError, u2.save)

    def test_confirm_email(self):
        u = User(nickname='test12345678910',
                 email='test3@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Email Confirmed' in rv.data

    def test_update_at_after_confirm_email(self):
        u = User(nickname='testupdateat',
                 email='test_update_at@example.com',
                 password="FakeUserPassword123",
                 salt="salt")
        token_string = generate_confirmation_token(u.email)
        u.confirmation_token = Token(token=token_string)
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
        u.confirmation_token = Token(token=token_string)
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
                                     created_at=datetime.datetime.now() -
                                     datetime.timedelta(days=2))
        u.save()
        rv = self.app.get("/confirm_email/" + u.confirmation_token.token)
        assert b'Error in confirming email' in rv.data


# TODO: Add more coverage for JWT.
class EmotlyJWTTokenTestCases(unittest.TestCase):
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


class EmotlyLoginTestCases(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()

    def test_login_email_success(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post('/api/1.0/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_nickname_success(self):
        salt = get_salt()
        u = User(nickname='testnickname',
                 email='email2@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'testnickname',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_login_non_secure(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtest.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()

        user_data = {'user_id': 'email@emailtest.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)


    def test_login_email_fail(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@emailtestwrong.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'email@emailtestwrong.com',
                     'password': 'passwordwrong'}
        rv = self.app.post('/api/1.0/login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_nickname_fail(self):
        salt = get_salt()
        u = User(nickname='testnfail',
                 email='email22@emailtestwrong.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=True,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'testnfail',
                     'password': 'passwordwrong'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_user_not_registered(self):
        user_data = {'user_id': 'santaclaus@lostisland.com',
                     'password': 'hohoho'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 404)


    def test_login_email_not_confirmed(self):
        salt = get_salt()
        u = User(nickname='test12345678910',
                 email='email@notconfirmed.com',
                 password=hash_password("password".encode('utf-8'), salt),
                 confirmed_email=False,
                 salt="salt")
        u.save()
        user_data = {'user_id': 'email@notconfirmed.com',
                     'password': 'password'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 403)

    def test_login_missing_data(self):
        user_data = {'password': 'passwordwrong'}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + 'login',
                           data=json.dumps(user_data),
                           base_url='https://localhost')

        self.assertEqual(rv.status_code, 500)


# Tests for Emotly model
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


# Tests for Emotly REST APIT
class EmotlyRESTAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()
        Emotly.objects.delete()

    def test_get_moods(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "moods")
        self.assertEqual(rv.status_code, 200)

    def test_moods_size(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "moods")
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(len(data['moods']), len(MOOD))

    def test_moods_type(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "moods")
        data = json.loads(rv.data.decode('utf-8'))
        for mood in data['moods']:
            self.assertEqual(type(mood['id']), int)
            self.assertEqual(type(mood['value']), str)

    def test_cannot_get_emotlies_unauthorized(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/own")
        self.assertEqual(rv.status_code, 403)

    def test_cannot_get_emotly_unauthorized(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/show/1")
        self.assertEqual(rv.status_code, 403)

    def test_cannot_get_post_emotly_unauthorized(self):
        m = {'mood': 1}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "emotlies/new",
                           data=json.dumps(m))
        self.assertEqual(rv.status_code, 403)

    def test_post_emotly(self):
        u = User(nickname='testpost',
                 email='test_post_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        m = {'mood': 1}
        token = generate_jwt_token(u)
        headers = {'content-type': 'application/json',
                   'auth_token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "emotlies/new",
                           headers=headers, data=json.dumps(m))
        self.assertEqual(rv.status_code, 200)

    def test_get_own_emotlies(self):
        u = User(nickname='testget',
                 email='test_get_emotlies@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        e = Emotly(mood=1)
        e.user = u
        e.save()

        emotly = Emotly(mood=2)
        emotly.user = u
        emotly.save()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/own",
                          headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_get_emotlies(self):
        u = User(nickname='testgetown',
                 email='test_get_emotlies_own@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        e = Emotly(mood=1)
        e.user = u
        e.save()

        u2 = User(nickname='testgetown2',
                  email='test_get_emotlies_own2@example.com',
                  password="FakeUserPassword123",
                  confirmed_email=True,
                  last_login=datetime.datetime.now(),
                  salt="salt")
        u2.save()
        emotly = Emotly(mood=2)
        emotly.user = u2
        emotly.save()
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies")
        self.assertEqual(rv.status_code, 200)

    def test_get_emotly(self):
        u = User(nickname='testgetsingle',
                 email='test_get_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly(mood=2)
        emotly.user = u
        emotly.save()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}

        rv = self.app.get("/api/1.0/emotlies/show/" + str(emotly.id),
                          headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_get_empty_list_emotlies(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies")
        self.assertEqual(rv.status_code, 200)

    def test_get_empty_own_list_emotlies(self):
        u = User(nickname='testgetempty',
                 email='test_get_emotlies_own_empty@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/own",
                          headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_get_non_existing_emotly(self):
        u = User(nickname='testnotexisting',
                 email='test_get_ne_emotly@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly(mood=2)
        emotly.user = u
        emotly.save()
        emotly.delete()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/show/" +
                          str(emotly.id), headers=headers)
        self.assertEqual(rv.status_code, 404)

    # Next 3 test non existing user access to api
    def test_non_existing_user_get_emotlies(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/user_emotlies",
                          headers=headers)
        self.assertEqual(rv.status_code, 404)

    def test_non_existing_user_get_emotly(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/show/" +
                          str(len(MOOD)), headers=headers)
        self.assertEqual(rv.status_code, 404)

    def test_non_existing_user_post_emotly(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        m = {'mood': 1}
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "emotlies/new",
                           headers=headers, data=json.dumps(m))
        self.assertEqual(rv.status_code, 404)

    # Next 3 test user not confirmed access to api
    def test_not_confirmed_user_post_emotly(self):
        u = User(nickname='testpostnc',
                 email='test_post_e_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        m = {'mood': 1}
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "emotlies/new",
                           headers=headers, data=json.dumps(m))
        self.assertEqual(rv.status_code, 403)

    def test_not_confirmed_user_get_emotlies(self):
        u = User(nickname='testgetnc',
                 email='test_get_emotlies_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/own",
                          headers=headers)
        self.assertEqual(rv.status_code, 403)

    def test_not_confirmed_user_get_emotly(self):
        u = User(nickname='testgetsinglenc',
                 email='test_get_e_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'auth_token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "emotlies/show/" +
                          str(len(MOOD)), headers=headers)
        self.assertEqual(rv.status_code, 403)

if __name__ == '__main__':
    unittest.main()
