import os
from Emotly import app


if __name__ == "__main__":
    app.run(debug='EMOTLY_APP_DEBUG_ENABLE' in os.environ)
