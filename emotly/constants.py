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
from emotly.models import JsonError

# Few Emotly-specific constants.

# Progressive web app link
APP_LINK = 'https://emotly.herokuapp.com/static/app/pwa'

# Generic Constants
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
MINUTES_SINCE_LAST_EMAIL = 15

# Rest API prefix
REST_API_PREFIX = '/api/1.0'  # No trailing slash, please.

# Rest API response content.
MSG_INVALID_REQUEST = 'Invalid request'
MSG_EMOTLY_DOES_NOT_EXIST = 'Emotly error.'
MSG_USER_DOES_NOT_EXIST = 'User does not exist.'
MSG_USER_UNKNOW = 'Nickname or user unknown.'
MSG_EMOTLY_NONEXISTENT = 'Nonexistent Emotly.'
MSG_EMOTLY_INVALID_MISSING_DATA = 'Invalid or missing data in Emotly.'
MSG_USER_MISSING_REGISTRATION_DATA = 'Invalid or missing \
    data for registration.'
MSG_TOKEN_CONFIRMATION_ALREADY_SENT = 'Confirmation already sent.'
MSG_USER_ACCOUNT_EXISTING = 'Existing account data.'
MSG_INSECURE_REQUEST = 'Insecure request.'
MSG_USER_UNCONFIRMED = 'Unconfirmed account.'
MSG_USER_MUST_AUTHENTICATE = 'Must be authenticated.'
MSG_USER_ALREADY_CONFIRMED = 'User already confirmed.'
UNKNOW_ERROR = 'Unknow error.'


UNAUTHORIZED = 'Unauthorized access.'
INTERNAL_SERVER_ERROR = 'Internal server error.'
INVALID_JSON_DATA = 'Bad request data.'
NOT_HTTPS_REQUEST = 'Invalid request.'

# Success Flash messages.
REGISTRATION_COMPLETED_CHECK_EMAIL = 'Registration completed! Check your email'
CONFIRMATION_EMAIL_SENT = 'Confirmation email sent. Check your email'
CONFIRMATION_EMAIL_ALREADY_SENT = 'Confirmation email has alredy been sent' + \
                                  ' in the last ' + \
                                  str(MINUTES_SINCE_LAST_EMAIL) + \
                                  ' minutes. Please check your email'
EMAIL_CONFIRMED = 'Email Confirmed.'

# Error Flash sessages.
REGISTRATION_ERROR_INVALID_DATA = 'Registration error: ' + \
                                  'Please insert valid data'
REGISTRATION_ERROR_USER_EXISTS = 'Registration error: User already exist!'
ERROR_IN_CONFIRMING_EMAIL = 'Error in confirming email.'

CODE_DATA_INVALUD_REQUEST = -101
CODE_USER_UNKNOW = -204
CODE_EMOTLY_NONEXISTENT = -304
CODE_EMOTLY_INVALID_MISSING_DATA = -301
CODE_TOKEN_CONFIRMATION_ALREADY_SENT = -229
CODE_USER_MISSING_REGISTRATION_DATA = -201
CODE_USER_ACCOUNT_ALREADY_EXISTS = -203
CODE_USER_ALREADY_CONFIRMED = -208
CODE_REQUEST_INSECURE = -103
CODE_USER_UNCONFIRMED = -205
CODE_REQUEST_MUST_AUTHENTICATE = -206
CODE_REQUEST_UNAUTHORIZED = -207
CODE_UNKNOW_ERROR = -199

ERRORS_TABLE = {
    CODE_DATA_INVALUD_REQUEST:
        JsonError(400, MSG_INVALID_REQUEST),
    CODE_USER_UNKNOW:
        JsonError(404, MSG_USER_UNKNOW),
    CODE_EMOTLY_NONEXISTENT:
        JsonError(404, MSG_EMOTLY_NONEXISTENT),
    CODE_EMOTLY_INVALID_MISSING_DATA:
        JsonError(400, MSG_EMOTLY_INVALID_MISSING_DATA),
    CODE_TOKEN_CONFIRMATION_ALREADY_SENT:
        JsonError(429, MSG_TOKEN_CONFIRMATION_ALREADY_SENT),
    CODE_USER_MISSING_REGISTRATION_DATA:
        JsonError(400, MSG_USER_MISSING_REGISTRATION_DATA),
    CODE_USER_ACCOUNT_ALREADY_EXISTS:
        JsonError(400, MSG_USER_ACCOUNT_EXISTING),
    CODE_USER_ALREADY_CONFIRMED:
        JsonError(400, MSG_USER_ALREADY_CONFIRMED),
    CODE_REQUEST_INSECURE:
        JsonError(403, MSG_INSECURE_REQUEST),
    CODE_USER_UNCONFIRMED:
        JsonError(403, MSG_USER_UNCONFIRMED),
    CODE_REQUEST_MUST_AUTHENTICATE:
        JsonError(403, MSG_USER_MUST_AUTHENTICATE),
    CODE_REQUEST_UNAUTHORIZED:
        JsonError(403, UNAUTHORIZED),
    CODE_UNKNOW_ERROR:
        JsonError(400, UNKNOW_ERROR)
}
