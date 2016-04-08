"""
Emotly

DEED
"""

import os

# Statement for enabling the development environment.
DEBUG = 'EMOTLY_APP_DEBUG_ENABLE' in os.environ

# Define the application directory.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# MongoDB settings.
# The URI defaults to mongodb://localhost/db
MONGODB_SETTINGS = {'host': os.environ['EMOTLY_DB_URI'] if
                    'EMOTLY_DB_URI' in os.environ else
                    'mongodb://localhost/db'}

# How to store the sessions.
SESSION_TYPE = 'filesystem'

# The super secret key. Please set it in the env
# variables anyway!
SECRET_KEY = os.environ['EMOTLY_APP_SEC_SUPERSECRET'] if\
    'EMOTLY_APP_SEC_SUPERSECRET' in os.environ else\
    'DUMMYSECRET123'

# How many rounds for the salt generation; defaults to 12.
GENSALT_ROUNDS = int(os.environ['EMOTLY_APP_SEC_ROUNDS']) if\
    'EMOTLY_APP_SEC_ROUNDS' in os.environ else 12

# Postmark API token; defaults to test mode.
PM_API_TOKEN = os.environ['POSTMARK_API_TOKEN'] if\
    'POSTMARK_API_TOKEN' in os.environ else 'POSTMARK_API_TEST'

EMAIL_SENDER = os.environ['POSTMARK_SENDER'] if\
    'POSTMARK_SENDER' in os.environ else 'test@test.test'

"""
# These are few configuration parameters we might want to set
# in the future.
#
# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2
#
# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True
#
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"
"""
