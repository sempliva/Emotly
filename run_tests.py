"""
Emotly Test Suite
"""
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
