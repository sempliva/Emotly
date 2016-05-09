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
