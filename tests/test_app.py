### Unit tests for the application. tests routes.py, app.py etc.
import pytest
import sys
import os
from flask import url_for
from flask_login import login_user
# Add the app folder to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from app import application, db
from app.models import User, Movie, UserMovie


# Fixtures
@pytest.fixture
def client():
    with application.test_client() as client:
        yield client


@pytest.fixture
def init_db():
    # Create all tables and add test data
    db.create_all()

    # Add a test user
    user = User(username="testuser", email="testuser@example.com")
    user.set_password("password")
    db.session.add(user)
    db.session.commit()

    # Add a test movie
    movie = Movie(title="Test Movie", year="2025", genre="Comedy", runtime=120)
    db.session.add(movie)
    db.session.commit()

    # Add a test UserMovie
    user_movie = UserMovie(user_id=user.id, movie_id=movie.id, user_rating=5)
    db.session.add(user_movie)
    db.session.commit()

    yield db  # This will allow tests to run

    # Cleanup
    db.drop_all()

# Test User Routes
def test_user_signup(client):
    """Test user signup."""
    response = client.post(url_for('signup_account'), json={"username": "newuser", "password": "password"})
    assert response.status_code == 200
    assert b"Signup successful" in response.data

def test_user_login(client, init_db):
    """Test user login."""
    response = client.post(url_for('login'), data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert b"Logged in successfully" in response.data

def test_user_logout(client, init_db):
    """Test user logout."""
    with client.session_transaction() as session:
        session['user_id'] = 1  # Mock user login
        
    response = client.get(url_for('logout'))
    assert response.status_code == 302
    assert b"Logged out successfully" in response.data

# Test Movie Routes
def test_movie_upload(client, init_db):
    """Test movie upload route."""
    movie_data = {
        "movie_title": "Test Movie",
        "user_rating": 5
    }
    response = client.post(url_for('upload_movie'), json=movie_data)
    assert response.status_code == 200
    assert b"Movie: Test Movie rating updated!" in response.data

def test_movie_autocomplete(client):
    """Test autocomplete movie search."""
    response = client.get(url_for('autocomplete_movie', q="Test"))
    assert response.status_code == 200
    assert b"Test Movie" in response.data

# Test Friendship Routes
def test_add_friend(client, init_db):
    """Test adding a friend."""
    response = client.post(url_for('add_friend'), json={"username": "newuser"})
    assert response.status_code == 200
    assert b"You were added as a friend" in response.data

def test_remove_friend(client, init_db):
    """Test removing a friend."""
    response = client.post(url_for('remove_friend'), json={"username": "newuser"})
    assert response.status_code == 200
    assert b"You have been removed from the friend list" in response.data

# Test Profile and User Data
def test_profile_page(client, init_db):
    """Test viewing user profile."""
    response = client.get(url_for('profile'))
    assert response.status_code == 200
    assert b"testuser" in response.data  # Check for username

def test_search_user(client, init_db):
    """Test searching for users."""
    response = client.get(url_for('search_user', username="newuser"))
    assert response.status_code == 200
    assert b"newuser" in response.data

# Test Movie Search & Autocomplete
def test_search_movies(client, init_db):
    """Test searching for movies."""
    response = client.get(url_for('search_movies', q="Test"))
    assert response.status_code == 200
    assert b"Test Movie" in response.data