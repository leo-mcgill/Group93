import unittest
from app import create_app, db
from app.models import User, Movie, UserMovie
from app.config import TestingConfig
from flask_login import login_user


class UserAuthTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the app and test database before any tests run."""
        cls.app = create_app(TestingConfig)  # Use TestingConfig for testing
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after all tests are run."""
        with cls.app.app_context():
            db.drop_all()  # Drop all tables after all tests

    def setUp(self):
        """Reset the database before each test."""
        with self.app.app_context():
            db.create_all()  # Create all tables before each test

            # Clear out the User and Movie tables to avoid UNIQUE constraint failure
            db.session.query(User).delete()
            db.session.query(Movie).delete()
            db.session.commit()

            # Create a test user and a user to be added as a friend
            user = User(username="movieuser")
            user.set_password("password1")
            frienduser = User(username="frienduser")
            frienduser.set_password("password1")
            db.session.add(user)
            db.session.add(frienduser)
            db.session.commit()

            # Create a movie in the database
            movie = Movie(
                id=6,
                title="The Avengers",
                year="2012",
                rated="PG-13",
                released="04 May 2012",
                runtime="143 min",
                genre="Action, Sci-Fi",
                director="Joss Whedon",
                writer="Joss Whedon, Zak Penn",
                actors="Robert Downey Jr., Chris Evans, Scarlett Johansson",
                language="English, Russian",
                country="United States",
                imdb_rating=8.0,
                rt_rating="91%",
                metascore=69,
                box_office="$623,357,910",
                poster_url="https://m.media-amazon.com/images/M/MV5BNGE0YTVjNzUtNzJjOS00NGNlLTgxMzctZTY4YTE1Y2Y1ZTU4XkEyXkFqcGc@._V1_SX300.jpg"
            )
            db.session.add(movie)
            db.session.commit()



    def tearDown(self):
        """Clean up any post-test data."""
        with self.app.app_context():
            db.session.remove()  # Remove the session
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

    def test_login(self):
        """Test login Route"""
        # Signup first
        self.client.post('/signup_account', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        
        # Then try login
        response = self.client.post('/login', data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        
        self.assertEqual(response.request.path, '/')

        # Check for successful status code and redirect
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to our Movie Tracker Platform', response.data.decode())
    
    def test_upload_movie(self):
        """Testing that a user can (login)->(Upload a movie): """
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()  # Retrieve the test user
            self.client.post('/login', data={
                'username': user.username,
                'password': "password1"  # Ensure the password is correct
            }, follow_redirects=True)
        
        # Send POST request to add "The Avengers" to the user's movie list
        response = self.client.post('/upload_movie', json={
            'movie_title': 'The Avengers',
            'user_rating': 8.0
        })

        # Assert that the response code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the success message is returned
        result = response.get_json()
        self.assertEqual(result['message'], 'Movie: The Avengers added to your list!')

        # Check that the movie has been added to the UserMovie table
        with self.app.app_context():
            user_movie = UserMovie.query.filter_by(user_id=1, movie_id=6).first()
            self.assertIsNotNone(user_movie)
            self.assertEqual(user_movie.user_rating, 8.0)


    def test_share_with_user_user_not_found(self):
        """Test that the route returns an error when trying to share with a non-existing user."""
        with self.client as client:
            # Log in
            client.post('/login', data={
                'username': 'movieuser',
                'password': 'password1'
            }, follow_redirects=True)

            # Post to the correct new route
            response = client.post('/share_with_user', json={
                'username': 'nonexistentuser'
            })

            self.assertEqual(response.status_code, 404)
            result = response.get_json()
            self.assertIsNotNone(result)
            self.assertEqual(result['error'], "User not found")

    def test_share_user_with_self(self):
        """Test that the route returns an error when trying to add yourself as a friend."""
        #login first
        with self.client as client:
            client.post('/login', data={
                'username': 'movieuser',
                'password': 'password1'
            }, follow_redirects=True)

            response = client.post('/share_with_user', json={
                'username': 'movieuser'
            })

            self.assertEqual(response.status_code, 400)
            result = response.get_json()
            self.assertIsNotNone(result)
            self.assertEqual(result['error'], "Cannot add yourself as a friend")

    def test_share_with_user_already_shared(self):
        """Test that sharing with an already-friended user returns 400."""
        with self.client as client:
            client.post('/login', data={
                'username': 'movieuser',
                'password': 'password1'
            }, follow_redirects=True)

            # First share attempt
            response1 = client.post('/share_with_user', json={
                'username': 'frienduser'
            })
            self.assertEqual(response1.status_code, 200)

            # Second share attempt — should fail
            response2 = client.post('/share_with_user', json={
                'username': 'frienduser'
            })

            self.assertEqual(response2.status_code, 400)
            result = response2.get_json()
            self.assertIsNotNone(result)
            self.assertEqual(result['error'], "Already in their friend list")
        
    def test_update_bio(self):
        """Test that a user can update their bio."""
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()  # Retrieve the test user
            self.client.post('/login', data={
                'username': user.username,
                'password': "password1"
            }, follow_redirects=True)
    
            new_bio = "This is my new bio!"  # A valid bio
            response = self.client.post('/update_bio', json={'bio': new_bio})

            # Assert the status code is 200 (OK)
            self.assertEqual(response.status_code, 200)

            # Assert the success message is returned
            result = response.get_json()
            self.assertTrue(result['success'])

            # Check that the bio is updated in the database

            user = User.query.filter_by(username="movieuser").first()
            self.assertEqual(user.bio, new_bio)

    def test_update_bio_exceeds_length(self):
        """Test that a user cannot update their bio beyond the maximum length."""
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()  # Retrieve the test user
            self.client.post('/login', data={
                'username': user.username,
                'password': "password1"
            }, follow_redirects=True)
        
            long_bio = "A" * 1000  # A bio longer than 500 characters
            response = self.client.post('/update_bio', json={'bio': long_bio})

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the success message is returned
        result = response.get_json()
        self.assertTrue(result['success'])

        # Check that the bio is truncated to 500 characters in the database
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()
            self.assertEqual(len(user.bio), 500)  # Ensure the bio is truncated to 500 characters

    def test_update_bio_empty(self):
        """Test that the bio can be updated to an empty string."""
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()  # Retrieve the test user
            self.client.post('/login', data={
                'username': user.username,
                'password': "password1"
            }, follow_redirects=True)
        
            response = self.client.post('/update_bio', json={'bio': ''})

        # Assert the status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert the success message is returned
        result = response.get_json()
        self.assertTrue(result['success'])

        # Check that the bio is updated to an empty string in the database
        with self.app.app_context():
            user = User.query.filter_by(username="movieuser").first()
            self.assertEqual(user.bio, '')
            
            
                

if __name__ == '__main__':
    unittest.main()
