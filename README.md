# Emotly

## Requirements

The whole thing is a Python application meant to run as a service, at least that's the idea. The *suggested* setup is pretty straightforward:

- **Python 3.5** (*or at least something that resembles Python3*)
- **Pip** (*usually already part of the Python package*)
- **Virtualenvwrapper**, which should help you to not hate your life; just run `pip install virtualenvwrapper`
- **MongoDB** is our backend; check your platform packaging system for info on how to install it

> **Notes**
> We didn't find any problem *yet* with our choice of targeting Python 3.5.
> Please let us know if you find some issue.

## Setup

The following is a *one-minute* tutorial to setup your environment to run Emotly on your local machine. Be sure to have all the requirements installed already.

First, make sure you've all the requirements in place, then create your environment by issuing:

```
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv -p python3 py3emotly
$ workon py3emotly
```

The path to `virtualenvwrapper.sh` depends on your OS, of course. `mkvirtualenv` needs to be issued just once.

Every time you plan to run or work on Emotly you should `source` the virtualenvwrapper.sh (*or include it in your shell configuration file*) and issue the `workon` command, to be sure that whatever Python related command happens within the specified environemnt. **That's it**.

## Running

Once you have everything nicely set up, just clone the repo and install the relevant dependencies (*if you haven't already*):
```
$ pip install -r requirements.txt
```
Then, the gloriously run everything with:
```
$ gunicorn emotly:app
```
Nothing else to do, unless contributing your juicy grey matter.

## Running Tests

When running test class locally evironment variable "EMOTLY_DB_URI" **must be** specified. Local collections are automatically deleted after tests execution.
```
EMOTLY_DB_URI="mongodb://localhost/something" python emotly_tests.py
```

## Environment variables
The following is a (hopefully) updated list of all the env var currently supported by the Emotly app.

* `EMOTLY_DB_URI` [**required**] URI for the Mongo database
* `EMOTLY_APP_SEC_SUPERSECRET` [**required**] A string, as complex as possible, for the secret (used for password generation)
* `EMOTLY_APP_SEC_ROUNDS` A number (not lesser than 12) for the bcrypt() rounds; defaults to 12
* `EMOTLY_APP_DEBUG_ENABLE` If specified (no matter the value), the app will be run with the `Debug` flag enabled
* `POSTMARK_API_TOKEN` Token used by Postmark API to send email. Set this to 'POSTMARK_API_TEST' to avoid actually sending mails.
* `POSTMARK_SENDER` An email used in the from field.

## Contributing

TODO

