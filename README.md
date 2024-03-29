# Two-Factor Authentication with Authy OneTouch
This application example demonstrates how to implement Two-Factor Authentication on a Python Flask application using [Authy OneTouch](https://www.twilio.com/authy).

![Flask](https://github.com/TwilioDevEd/authy2fa-flask/workflows/Flask/badge.svg)


[Learn more about this code in our interactive code walkthrough](https://www.twilio.com/docs/howto/walkthrough/two-factor-authentication/python/flask).

## Quickstart

### Create an Authy app
Create a free [Twilio account](https://www.twilio.com/console/authy) if you haven't already done so.

Create a new Authy application. Be sure to set the OneTouch callback endpoint to `http://your-server-here.com/authy/callback` once you've finished configuring the app.

### Local development
This project is built using the [Flask](http://flask.pocoo.org/) web framework and the SQlite3 database.

1. To run the app locally, first clone this repository and `cd` into it.

1. Create and activate a new python3 virtual environment.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

1. Install the requirements using [pip](https://pip.pypa.io/en/stable/installing/).

   ```bash
   pip install -r requirements.txt
   ```

1. Copy the `.env.example` file to `.env`, and edit it to include your **Authy Application's Production API key**. This key can be found right below the Application's name in its **Settings** menu.

   ```bash
   cp .env.example .env
   ```

1. Create the Flask app specific environment variables
   
   ```bash
   export FLASK_APP=twofa
   export FLASK_ENV=development
   ```
   
1. Initialize the development database

   ```bash
   flask db upgrade
   ```

1. Start the development server.

   ```bash
   flask run
   ```

## Expose your app in the internet
To actually process OneTouch authentication requests, your development server will need to be publicly accessible. [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html). **Note that in this tutorial only the HTTP address from ngrok will work**, so you should start it using this command:

```bash
ngrok http -bind-tls=false 5000
```

Once you have started ngrok, set your Authy app's OneTouch callback URL to use your ngrok hostname, like this:

```
http://[your ngrok subdomain].ngrok.io/authy/callback
```

## Run the tests
You can run the tests locally through [coverage](http://coverage.readthedocs.org/):

1. Run the tests.

    ```bash
    python test.py
    ```

You can then view the results with `coverage report` or build an HTML report with `coverage html`.

That's it!

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](LICENSE)
* Lovingly crafted by Twilio Developer Education.
