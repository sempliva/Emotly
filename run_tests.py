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

# Emotly Test Runner

import glob
import pep8
import sys
import unittest
from emotly import app


def run_pep8_style_check():
    s = pep8.StyleGuide(quiet=False, config_file='style.cfg')
    res = s.check_files(glob.glob('**/*.py', recursive=True))
    if res.total_errors:
        print("\n\n*** Emotly Style Checker: found %s style errors!\n" %
              res.total_errors)


# Loads all the tests in the emotly/tests directory.
def run_emotly_tests():
    test_loader = unittest.defaultTestLoader
    tests = test_loader.discover('emotly/tests', pattern='test*.py')

    # unittest.TextTestRunner suppresses warnings by default and we have many
    # DeprecationWarnings due to MongoEngine.
    # In order to re-enable the warnings, run the TestRunner with -Wd, eg:
    # python -Wd run_tests.py
    #
    # TODO: Re-enable warnings by default by using the argument
    # warnings='default' in TextTestRunner().
    test_runner = unittest.TextTestRunner()
    result = test_runner.run(tests)
    return not result.wasSuccessful()


if __name__ == '__main__':
    assert app.debug is False, 'Don\'t run in debug mode.'

    run_pep8_style_check()
    sys.exit(run_emotly_tests())
