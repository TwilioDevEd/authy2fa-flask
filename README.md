# Two-Factor Authentication with Authy OneTouch

This application example demonstrates how to implement Two-Factor Authentication on a Python Flask application using [Authy OneTouch](https://www.twilio.com/authy).

[![Build Status](https://travis-ci.org/TwilioDevEd/authy2fa-flask.svg?branch=master)](https://travis-ci.org/TwilioDevEd/authy2fa-flask)


[Learn more about this code in our interactive code walkthrough](https://www.twilio.com/docs/howto/walkthrough/two-factor-authentication/python/flask).

## Quickstart

### Create an Authy app

Create a free [Twilio account](https://www.twilio.com/console/authy) if you haven't
already done so.

Create a new Authy application. Be sure to set the OneTouch callback
endpoint to `http://your-server-here.com/authy/callback` once you've finished
configuring the app.

### Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework
and the SQlite3 database.

1. To run the app locally, first clone this repository and `cd` into it.

1. Create a new virtual environment.

    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```
        mkvirtualenv authy2fa-flask
        ```

1. Install the requirements.

    ```
    pip install -r requirements.txt
    ```

1. Copy the `.env_example` file to `.env`, and edit it to include your Authy App's Production API key

1. Run the migrations.

    ```
    ./manage.py db upgrade
    ```

1. Start the development server.

    ```
    ./manage.py runserver
    ```

To actually process OneTouch authentication requests, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).

Once you have started ngrok, set your Authy app's OneTouch callback URL to use your ngrok hostname, like this:

```
http://88b37ada.ngrok.io/authy/callback
```

## Run the tests

You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Optionally create a separate test database and update your `DATABASE_URL` environment variable if you don't want your development data overwritten.

1. Run the tests.

    ```
    $ coverage run manage.py test
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.

That's it!

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.
