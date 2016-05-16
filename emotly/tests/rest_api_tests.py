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

# REST API Test Case

import unittest
import datetime
import json
from emotly import app
from emotly import constants as CONSTANTS
from emotly.models import User, Emotly, MOOD
from emotly.utils import generate_jwt_token


# Tests for Emotly REST API.
class RESTAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        User.objects.delete()
        Emotly.objects.delete()

    def test_get_moods(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/moods",
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_moods_size(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/moods",
                          base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(len(data['moods']), len(MOOD))

    def test_moods_type(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/moods",
                          base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        for mood in data['moods']:
            self.assertEqual(type(mood['id']), int)
            self.assertEqual(type(mood['value']), str)

    # Unauthorized access.
    def test_cannot_get_emotlies_unauthorized(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_cannot_get_emotly_unauthorized(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/show/1",
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_cannot_get_post_emotly_unauthorized(self):
        m = {'mood': 1}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           data=json.dumps(m), base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    # Json data checks.
    def test_post_emotly_json_data_not_contains_mood(self):
        u = User(nickname='testpost1',
                 email='test_post_emotly1@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        m = {'this_is_not_mood': 1}
        token = generate_jwt_token(u)
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data=json.dumps(m),
                           base_url='https://localhost')
        assert (CONSTANTS.INVALID_JSON_DATA).encode('utf-8') in rv.data

    def test_post_emotly_json_data_not_valid(self):
        u = User(nickname='testpost2',
                 email='test_post_emotly2@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        token = generate_jwt_token(u)
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data="this is not json",
                           base_url='https://localhost')
        assert (CONSTANTS.INTERNAL_SERVER_ERROR).encode('utf-8') in rv.data

    def test_post_emotly_no_json_data(self):
        u = User(nickname='testpost3',
                 email='test_post_emotly3@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        token = generate_jwt_token(u)
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, base_url='https://localhost')
        assert (CONSTANTS.INVALID_JSON_DATA).encode('utf-8') in rv.data

    # Success tests.
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
                   'X-Emotly-Auth-Token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data=json.dumps(m),
                           base_url='https://localhost')
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          headers=headers, base_url='https://localhost')
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
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies",
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_get_user_details_last_emotly(self):
        u = User(nickname='testgetlast',
                 email='test_get_emotly_last@example.com',
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

        emotly = Emotly(mood=3)
        emotly.user = u
        emotly.save()

        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/user/' + u.nickname,
                          headers=headers, base_url='https://localhost')
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/emotlies/show/' +
                          str(emotly.id), headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    def test_get_empty_list_emotlies(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies",
                          base_url='https://localhost')
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 200)

    # Non existing emotly.
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/show/" +
                          str(emotly.id), headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    def test_get_non_existing_last_emotly_for_user(self):
        u = User(nickname='testgetempty',
                 email='test_get_emotlies_own_empty@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/user/' + u.nickname,
                          headers=headers, base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    # Non existing user.
    def test_non_existing_user_get_emotlies(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX +
                          "/emotlies/own", headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    def test_non_existing_user_get_emotly(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/show/" +
                          str(len(MOOD)), headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    def test_non_existing_user_post_emotly(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        m = {'mood': 1}
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data=json.dumps(m),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    def test_non_existing_user_get_last_emotly(self):
        u = User(nickname='fake',
                 email='fake@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/user/' + u.nickname,
                          headers=headers, base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    def test_get_user_details_last_emotly_nickname_non_existent(self):
        u = User(nickname='userdet',
                 email='fake@example.com',
                 confirmed_email=True,
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/user/' + "fakenick",
                          headers=headers, base_url='https://localhost')
        self.assertEqual(rv.status_code, 404)

    # User not confirmed.
    def test_not_confirmed_user_post_emotly(self):
        u = User(nickname='testpostnc',
                 email='test_post_e_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        m = {'mood': 1}
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data=json.dumps(m),
                           base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_not_confirmed_user_get_emotlies(self):
        u = User(nickname='testgetnc',
                 email='tlies_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          headers=headers, base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_response_list_emotlies(self):
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
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies",
                          base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertIsNotNone(data["emotlies"][0]["nickname"])
        self.assertIsNotNone(data["emotlies"][0]["mood"])
        self.assertIsNotNone(data["emotlies"][0]["created_at"])

    def test_response_get_emotlies(self):
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          headers=headers, base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertIsNotNone(data["emotlies"][0]["mood"])
        self.assertIsNotNone(data["emotlies"][0]["created_at"])

    def test_response_get_emotly(self):
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/emotlies/show/' +
                          str(emotly.id), headers=headers,
                          base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertIsNotNone(data["emotly"]["mood"])
        self.assertIsNotNone(data["emotly"]["created_at"])

    def test_not_confirmed_user_get_emotly(self):
        u = User(nickname='testgetsinglenc',
                 email='test_get_e_nc@example.com',
                 password="FakeUserPassword123",
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/show/" +
                          str(len(MOOD)), headers=headers,
                          base_url='https://localhost')
        self.assertEqual(rv.status_code, 403)

    # Test non-secure requests.
    def test_get_own_emotlies_non_secure(self):
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
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies/own",
                          headers=headers, base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_get_emotly_non_secure(self):
        u = User(nickname='getsingleins',
                 email='test_get_emotly_not_secure@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        emotly = Emotly(mood=2)
        emotly.user = u
        emotly.save()
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}

        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/emotlies/show/' +
                          str(emotly.id), headers=headers,
                          base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_post_emotly_non_secure(self):
        u = User(nickname='postnotsecure',
                 email='test_post_emotly_not_secure@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        m = {'mood': 1}
        token = generate_jwt_token(u)
        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': token}
        rv = self.app.post(CONSTANTS.REST_API_PREFIX + "/emotlies/new",
                           headers=headers, data=json.dumps(m),
                           base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_get_moods_non_secure(self):
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/moods",
                          base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_get_emotlies_non_secure(self):
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
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + "/emotlies",
                          base_url='http://localhost')
        self.assertEqual(rv.status_code, 403)

    def test_response_details_last_emotly(self):
        u = User(nickname='testgetlast',
                 email='test_get_emotly_last@example.com',
                 password="FakeUserPassword123",
                 confirmed_email=True,
                 last_login=datetime.datetime.now(),
                 salt="salt")
        u.save()
        e = Emotly(mood=1)
        e.user = u
        e.save()

        headers = {'content-type': 'application/json',
                   'X-Emotly-Auth-Token': generate_jwt_token(u)}
        rv = self.app.get(CONSTANTS.REST_API_PREFIX + '/user/' + u.nickname,
                          headers=headers, base_url='https://localhost')
        data = json.loads(rv.data.decode('utf-8'))
        self.assertEqual(data["emotly"]["nickname"], u.nickname)
        self.assertEqual(data["emotly"]["mood"], MOOD[1])
        self.assertEqual(data["emotly"]["created_at"],
                         e.created_at.strftime(CONSTANTS.DATE_FORMAT))
