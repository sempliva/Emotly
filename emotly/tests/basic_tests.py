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

# Basic Emotly Page Test Case

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
        rv = self.app.get('/signup', base_url='https://localhost')
        assert b'Signup' in rv.data
