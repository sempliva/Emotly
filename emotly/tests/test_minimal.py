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
        self.assertTrue(True)

    def test_emotly_index(self):
        rv = self.app.get('/')
        self.assertIn(b'Your life, your emotions', rv.data)

    def test_emotly_signup(self):
        rv = self.app.get('/signup', base_url='https://localhost')
        self.assertIn(b'Signup', rv.data)
