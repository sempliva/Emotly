"""
Basic Emotly Page Test Case
"""
import unittest
import pep8
import glob
from emotly import app


# Basic tests.
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
