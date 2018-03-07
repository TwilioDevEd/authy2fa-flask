import unittest

from twofa import create_app, db
from twofa.models import User
from unittest.mock import patch, MagicMock, PropertyMock


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_sign_up(self):
        # Arrange
        fake_authy_user = MagicMock()
        fake_authy_user.ok.return_value = True
        type(fake_authy_user).id = PropertyMock(return_value=1234)
        fake_client = MagicMock()
        fake_client.users.create.return_value = fake_authy_user

        # Act
        with patch('twofa.utils.get_authy_client', return_value=fake_client):
            resp = self.client.post('/sign-up', data={
                'name': 'test',
                'email': 'test@example.com',
                'password': 'fakepassword',
                'country_code': 33,
                'phone_number': '611223344'
            })

        # Assert
        fake_client.users.create.assert_called()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/account')
        print(User.query.all())

        user = User.query.filter_by(email='test@example.com').first()
        self.assertEqual(user.full_name, 'test')
        self.assertEqual(user.country_code, 33)
        self.assertEqual(user.phone_number, '611223344')
