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

> **Default configuration**
>
> Starting with `commit 0b27545baa1f1521d1fe244e868e0ecfeea4ea58` we have introduced a configuration file called `config.py` in the root of the project.
>
> This file contains most sensible defaults, hence you can run `python run_tests.py` without specifying anything else.
>
> You are *encouraged* to be explicit in your running commands, though.

## Environment variables
The following is a (hopefully) updated list of all the env var currently supported by the Emotly app.

* `EMOTLY_DB_URI` [**required**] URI for the Mongo database
* `EMOTLY_APP_SEC_SUPERSECRET` [**required**] A string, as complex as possible, for the secret (used for password generation)
* `EMOTLY_APP_SEC_ROUNDS` A number (not lesser than 12) for the bcrypt() rounds; defaults to 12
* `EMOTLY_APP_DEBUG_ENABLE` If specified (no matter the value), the app will be run with the `Debug` flag enabled
* `POSTMARK_API_TOKEN` Token used by Postmark API to send email. Set this to 'POSTMARK_API_TEST' to avoid actually sending mails.
* `POSTMARK_SENDER` An email used in the from field.
* `EMOTLY_APP_SEC_HMAC_SECRET` [**required**] A string, as complex as possible, for the hmac secret (used for Json Web Token generation)

## Contributing
We'd **love** to get your help! Emotly is continously updated in production, the overall process is extremely straightforward:

 1. **You** branch (*from master*)
 2. **You** work on your thing
 3. When you have something working, **you** push your branch
 4. **Our CI tool** (Travis) that will run all the tests for you and will let you know what happened
 5. If the tests succeed  **you** can go ahead and open a pull-request *against master*

Very simple. **Somebody** will then review your changes; if there is some concern *the reviewer will also help you sort things out*. As soon as you get thumbs-up from a reviewer your branch will be merged into master.
At that point, in few minutes, a new release of Emotly will be deployed in production, automatically. And you'll be our hero!

> **Please be aware**
>
> You should *always add coverage* for new features. **Always**.
>
> Also, *your code should match our coding style guidelines* (basically PEP8 for Python code); `python run_tests.py` will give you an idea whether there's something noticeably wrong with your style.
>
> Coding style checks are not currently enforced but they will be, in time.

