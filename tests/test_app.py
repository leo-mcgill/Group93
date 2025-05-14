import unittest
from app import create_app, db
from app.models import User, Movie, UserMovie
from app.config import TestingConfig
from flask_login import login_user

class UserAuthTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        """Set up the app and test database before any tests run."""
        self.app = create_app(TestingConfig)  # Use TestingConfig for testing
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()  # Create all tables in the test database

    @classmethod
    def tearDownClass(self):
        """Clean up the database after all tests are run."""
        with self.app.app_context():
            db.drop_all()  # Drop all tables after all tests

    def setUp(self):
        """Reset the database before each test."""
        with self.app.app_context():
            db.create_all()  # Create the tables again for each test

    def tearDown(self):
        """Clean up any post-test data."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables after each test

    def test_signup(self):
        """Test the signup route."""
        response = self.client.post('/signup_account', json={
            'username': 'testuser',
            'password': 'password123'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Signup successful", response.data)

        # Check if the user is actually added to the database
        with self.app.app_context():
            user = User.query.filter_by(username='testuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'testuser')
        
if __name__ == '__main__':
    unittest.main()