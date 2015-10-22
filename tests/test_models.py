import unittest
from datetime import datetime
from twofa import create_app, db
from twofa.models import User


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_setter(self):
        pass