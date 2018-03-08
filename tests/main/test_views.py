import unittest

from twofa import create_app, db
from twofa.models import User


class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home(self):
        # Act
        resp = self.client.get('/')

        # Assert
        self.assertEqual(resp.status_code, 200)

    def test_account_as_anon(self):
        # Act
        resp = self.client.get('/account')

        # Assert
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/login')

    def test_account_as_logged_in(self):
        # Arrange
        user = User(
            'example@example.com',
            'fakepassword',
            'Alice',
            33,
            600112233,
            123,
            authy_status='unverified'
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Act
        resp = self.client.get('/account')

        # Assert
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.location, 'http://localhost/login')

    def test_account_as_authentified(self):
        # Arrange
        user = User(
            'example@example.com',
            'fakepassword',
            'Alice',
            33,
            600112233,
            123,
            authy_status='approved'
        )
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
        with self.client.session_transaction() as sess:
            sess['user_id'] = user.id

        # Act
        resp = self.client.get('/account')

        # Assert
        self.assertEqual(resp.status_code, 302)
