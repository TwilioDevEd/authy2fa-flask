# Two-Factor Authentication with Authy

This example application demonstrates how to implement 2FA in a Python Flask application.

*Note:* The authy client does *not* support Python 3 so this application only 
runs with Python 2.x.


## Running locally
Development environment requirements:

* PostgreSQL with access to create a database such as "2faf"
* Use virtualenv and pip to install dependencies


1. Create virtualenv.

        virtualenv 2faf
        source 2faf/bin/activate

1. Clone repository at https://github.com/makaimc/aquarius-python-flask

        git clone git@github.com:makaimc/aquarius-python-flask

1. Change into the new directory.

        cd aquarius-python-flask

1. Install local dependencies.

        pip install -r requirements.txt

1. Set environment variables.

        export SECRET_KEY='super secret key'
        export DATABASE_URL='postgresql://username:password@localhost/2faf'
        export AUTHY_API_KEY='authyapikey'

1. Create database and schema.

        createdb 2faf
        python create_db.py

1. Run the app.

        python run.py

1. Open web browser and head to http://localhost:5000/ to see the app.


## Deploying on Heroku
Click this button to deploy right now!

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/TwilioDevEd/authy2fa-flask)

When deploying manually, use the following commands from the root of the project directory.

    heroku create

    heroku config:set SECRET_KEY='something super secret'
    heroku config:set AUTHY_API_KEY='api key here'

    heroku addons:add heroku-postgresql

    git push heroku master

    heroku run python create_db.py
