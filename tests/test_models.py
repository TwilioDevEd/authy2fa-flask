import unittest

from twofa import create_app, db
from twofa.models import User
from unittest.mock import patch


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.user = User(
            'example@example.com',
            'fakepassword',
            'Alice',
            33,
            600112233,
            123
        )
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_has_authy_app(self):
        # Arrange

        # Act
        with patch('twofa.models.authy_user_has_app', return_value=True):
            has_authy_app = self.user.has_authy_app

        # Assert
        self.assertTrue(has_authy_app)

    def test_hasnt_authy_app(self):
        # Arrange

        # Act
        with patch('twofa.models.authy_user_has_app', return_value=False):
            has_authy_app = self.user.has_authy_app

        # Assert
        self.assertFalse(has_authy_app)

    def test_password_is_unreadable(self):
        # Arrange

        # Act / Assert
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_setter(self):
        # Arrange
        old_password_hash = self.user.password_hash
        password = 'superpassword'

        # Act
        self.user.password = password

        # Assert
        self.assertNotEqual(password, self.user.password_hash)
        self.assertNotEqual(old_password_hash, self.user.password_hash)

    def test_verify_password(self):
        # Arrange
        password = 'anothercoolpassword'
        unused_password = 'unusedpassword'
        self.user.password = password

        # Act
        ret_good_password = self.user.verify_password(password)
        ret_bad_password = self.user.verify_password(unused_password)

        # Assert
        self.assertTrue(ret_good_password)
        self.assertFalse(ret_bad_password)

    def test_send_one_touch_request(self):
        # Arrange

        # Act
        with patch('twofa.models.send_authy_one_touch_request') as fake_send:
            self.user.send_one_touch_request()

        # Assert
        fake_send.assert_called_with(self.user.authy_id, self.user.email)
