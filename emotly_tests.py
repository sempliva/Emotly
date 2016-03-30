"""
Emotly Test Suite

Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest, emotly

# Simple page existance tests.
class  BasicEmotlyPageCase(unittest.TestCase):

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

    def  test_emotly_signup(self):
        rv = self.app.get('/signup')
        assert b'Signup' in rv.data

# TODO: User Registration tests.
class EmotlyUserRegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_signup(self):
        rv=self.app.post('/signup',
                      data=dict(
                          inputNickname="nickname",
                          inputEmail="email@emailtest.com",
                          inputPassword="password"
                      )
                    )
        assert b'Registration completed!' in rv.data
if __name__ == '__main__':
    unittest.main()
