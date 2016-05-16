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

# Emotly Test Suite

import unittest
from emotly.tests.basic_tests import BasicEmotlyPageCase
from emotly.tests.user_model_tests import UserModelTestCase
from emotly.tests.token_model_tests import TokenModelTestCase
from emotly.tests.emotly_model_tests import EmotlyModelTestCase
from emotly.tests.jwt_token_tests import JWTTokenTestCases
from emotly.tests.user_registration_tests import UserRegistrationTestCase
from emotly.tests.rest_api_tests import RESTAPITestCase
from emotly.tests.user_login_tests import LoginTestCases
from emotly.tests.user_registration_api_tests import \
    UserRegistrationAPITestCase
from emotly.tests.token_related_tests import TokenTestCase

# Creating a test suites.
emotly_basic_suite = unittest.TestSuite()
emotly_model_suite = unittest.TestSuite()
emotly_controller_suite = unittest.TestSuite()

# Adding test cases to emotly basic test suite.
emotly_basic_suite.addTest(unittest.makeSuite(BasicEmotlyPageCase))

# Adding test cases to emotly model test suite.
emotly_model_suite.addTest(unittest.makeSuite(TokenModelTestCase))
emotly_model_suite.addTest(unittest.makeSuite(UserModelTestCase))
emotly_model_suite.addTest(unittest.makeSuite(EmotlyModelTestCase))

# Adding test cases to emotly controller test suite.
emotly_controller_suite.addTest(unittest.makeSuite(UserRegistrationTestCase))
emotly_controller_suite.addTest(unittest.
                                makeSuite(UserRegistrationAPITestCase))
emotly_controller_suite.addTest(unittest.makeSuite(JWTTokenTestCases))
emotly_controller_suite.addTest(unittest.makeSuite(LoginTestCases))
emotly_controller_suite.addTest(unittest.makeSuite(RESTAPITestCase))
emotly_controller_suite.addTest(unittest.makeSuite(TokenTestCase))

if __name__ == '__main__':
    unittest.main()
