# aquarius-python-flask
Python / Flask back end for Authy 2FA DevEd example.

Note: The authy client does *not* support Python 3 so this application only 
runs with Python 2.x.


## Running locally
You'll need PostgreSQL installed as the database on your local system.

1. Create virtualenv.

1. Create database and schema.

    python create_db.py

1. Run the app.

    python run.py


## Deploying on Heroku
When deploying manually use the following commands from the root of the
project directory.

    heroku create

    heroku config:set SECRET_KEY='something super secret'
    heroku config:set AUTHY_API_KEY='api key here'

    heroku addons:add heroku-postgresql

    heroku run python create_db.py
