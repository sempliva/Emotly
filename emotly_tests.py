"""
Emotly Test Suite

Consider adding separate TestCase instance for different features.
KISS: Keep It Stupid Simple
"""
import unittest, emotly, pep8, glob

# Simple page existance tests.
class BasicEmotlyPageCase(unittest.TestCase):

    # Runs the test client.
    def setUp(self):
        self.app = emotly.app.test_client()

    def tearDown(self):
        pass

    def test_dummy(self):
        assert True

    def test_code_style(self):
        s = pep8.StyleGuide(quiet=True)
        res = s.check_files(glob.glob('emotly*.py'))
        if res.total_errors:
            print("*** WARNING ***: found %s style errors" % res.total_errors)

        # TODO: Enforcing the PEP8 tests is currently disabled; replace the first
        # 0 with res.total_errors to enable.
        self.assertEqual(0, 0, 'Found code style errors: run '
                                              'pep8 on the files for details')

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

if __name__ == '__main__':
    unittest.main()
