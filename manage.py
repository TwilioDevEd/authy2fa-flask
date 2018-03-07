#!/usr/bin/env python

from flask_script import Manager, Shell

import os

from twofa import create_app, db
from twofa.models import User

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import sys, unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)

    if not result.wasSuccessful():
        sys.exit(1)

if __name__ == "__main__":
    manager.run()
