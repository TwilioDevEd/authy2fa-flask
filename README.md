# Two-Factor Authentication with Authy OneTouch

This example application demonstrates how to implement Two-Factor Authentication
in a Python Flask application using [Authy OneTouch](https://www.authy.com/developers/).

**Full Tutorial:** https://www.twilio.com/docs/howto/walkthrough/two-factor-authentication/python/flask

## Quickstart

### Create an Authy app

Create a free [Authy account](https://www.authy.com/developers/) if you haven't
already and then connect it to your Twilio account.

*NEED TO ADD MORE INSTRUCTIONS HERE*

### Deploying on Heroku

To get up and running quickly, you can deploy this app for free using Heroku:

<<<<<<< HEAD
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/TwilioDevEd/authy2fa-flask)

### Local development
=======
1. Clone repository at https://github.com/TwilioDevEd/authy2fa-flask

        git clone git@github.com:TwilioDevEd/authy2fa-flask
>>>>>>> origin/master

This project is built using the [Flask](http://flask.pocoo.org/) web framework.
For now, it only runs on Python 2.7 (not 3.4+).

<<<<<<< HEAD
To run the app locally, first clone this repository and `cd` into its directory. Then:
=======
        cd authy2fa-flask
>>>>>>> origin/master

1. Create a new virtual environment:
    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv authy2fa-flask
        ```

1. Install the requirements:

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env_example` file to `.env`, and edit it to include your [Authy API key](https://dashboard.authy.com)

1. Run `source .env` to apply the environment variables (or even better, use [autoenv](https://github.com/kennethreitz/autoenv))

1. Start a local PostgreSQL database and create a database called `2fa_flask`:
    - If on a Mac, we recommend [Postgres.app](http://postgresapp.com/). After install, open psql and run `CREATE DATABASE 2fa_flask;`
    - If Postgres is already installed locally, you can just run `createdb 2fa_flask` from a terminal

1. Run the migrations with:

    ```
    python manage.py db upgrade
    ```

1. Start the development server

    ```
    python manage.py runserver
    ```

To actually process OneTouch authentication requests, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).

## Run the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Create the test database with either `CREATE DATABASE 2fa_flask_test;` or `createdb 2fa_flask_test`

1. Run the tests:

    ```
    $ coverage run manage.py test
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.
