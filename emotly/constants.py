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

# Few Emotly-specific constants.

# Progressive web app link
APP_LINK = 'https://emotly.herokuapp.com/static/app/pwa'

# Generic Constants
DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
MINUTES_SINCE_LAST_EMAIL = 15

# Rest API prefix
REST_API_PREFIX = '/api/1.0'  # No trailing slash, please.

# Rest API response content.
USER_NOT_CONFIRMED = 'User error.'
USER_DOES_NOT_EXIST = 'Authentication error.'

EMOTLY_DOES_NOT_EXIST = 'Emotly error.'

UNAUTHORIZED = 'Unauthorized access.'
INTERNAL_SERVER_ERROR = 'Internal server error.'
NOT_HTTPS_REQUEST = 'Bad request.'
INVALID_JSON_DATA = 'Bad request data.'


# Success Flash messages.
REGISTRATION_COMPLETED_CHECK_EMAIL = 'Registration completed! Check your email'
CONFIRMATION_EMAIL_SENT = 'Confirmation email sent. Check your email'
CONFIRMATION_EMAIL_ALREADY_SENT = 'Confirmation email has alredy been sent' + \
                                  ' in the last ' + \
                                  str(MINUTES_SINCE_LAST_EMAIL) + \
                                  ' minutes. Please check your email'
USER_ALREADY_CONFIRMED = 'User already Confirmed.'
EMAIL_CONFIRMED = 'Email Confirmed.'

# Error Flash sessages.
REGISTRAION_ERROR_INVALID_DATA = 'Registration error: Please insert valid data'
REGISTRAION_ERROR_USER_EXISTS = 'Registration error: User already exist!'
ERROR_IN_CONFIRMING_EMAIL = 'Error in confirming email.'
