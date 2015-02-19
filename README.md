# aquarius-python-flask
Python / Flask back end for Authy 2FA DevEd example.

## Deploying on Heroku
When deploying manually use the following commands from the root of the
project directory.

    heroku create

    heroku config:set SECRET_KEY='something super secret'
    heroku config:set AUTHY_API_KEY='api key here'

    heroku addons:add heroku-postgresql

    heroku run python create_db.py
