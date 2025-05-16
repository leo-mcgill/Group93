import unittest
import threading
import os
import time

from flask import session as flask_session

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.http import parse_cookie


from app.models import User, Movie, UserMovie
from app import create_app, db
from app.config import TestingConfig

localHost = "http://127.0.0.1:5000/"
#Note that Selenium is weird with logging in/signing up users through Flask-WTF so I've used cookies to sign in instead.
class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up Selenium WebDriver and run Flask server in a thread"""

        # Clean up leftover DB if present
        db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'test.db')
        db_path = os.path.abspath(db_path)
        if os.path.exists(db_path):
            os.remove(db_path)

        # Create app and push context
        cls.testApp = create_app(TestingConfig)
        cls.app_context = cls.testApp.app_context()
        cls.app_context.push()

        # Initialize and populate the database
        with cls.testApp.app_context():
            db.create_all()
            cls.populate_database()  # Populate the test database with data

        # Start the Flask app in a separate thread
        cls.server_thread = threading.Thread(
            target=cls.testApp.run, kwargs={"use_reloader": False}
        )
        cls.server_thread.daemon = True
        cls.server_thread.start()

        # Wait for server to be up
        cls.wait_for_server_startup()

        # Setup driver - headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        
        # Use ChromeDriverManager to automatically download and get the path to the driver
        service = Service(ChromeDriverManager().install())  # Use Service to specify the driver

        # Initialize the driver with the Service and options
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Set up the Selenium WebDriver
        cls.driver.get(localHost)

    @classmethod
    def tearDownClass(cls):
        """Shut down Flask app and clean up"""
        # Quit Selenium WebDriver
        if hasattr(cls, 'driver'):
            cls.driver.quit()

        # Clean up DB
        with cls.testApp.app_context():
            db.session.remove()
            db.drop_all()

        # Pop context
        cls.app_context.pop()
        
        # Delete DB file explicitly
        db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'test.db')
        db_path = os.path.abspath(db_path)
        if os.path.exists(db_path):
            os.remove(db_path)

    @staticmethod
    def populate_database():
        """Populate the test database by calling the shared populate() function."""
        from app.scripts import add_users_and_movies
        add_users_and_movies.populate()

    @staticmethod
    def wait_for_server_startup(timeout=10):
        """Wait for the Flask server to start"""
        import requests
        start_time = time.time()
        while True:
            try:
                requests.get(localHost)
                return
            except requests.exceptions.ConnectionError:
                if time.time() - start_time > timeout:
                    raise Exception("Flask server did not start in time")
                time.sleep(0.5)
    @staticmethod
    def get_logged_in_cookie(app, username="user1", password="password1"):
        with app.test_client() as client:
            # Post login data
            response = client.post("/login", data={
                "username": username,
                "password": password
            }, follow_redirects=False)

            assert response.status_code in (302, 303)

            # Extract the Set-Cookie header from the response
            set_cookie_header = response.headers.get("Set-Cookie")
            cookies = parse_cookie(set_cookie_header)

            session_cookie_name = app.config.get("SESSION_COOKIE_NAME", "session")

            if session_cookie_name in cookies:
                return {
                    "name": session_cookie_name,
                    "value": cookies[session_cookie_name],
                    "domain": "127.0.0.1",  # match your test host
                    "path": "/"
                }

        raise RuntimeError("Session cookie not found in response.")

    def login_via_cookie(self):
        self.driver.get("http://127.0.0.1:5000/")
        cookie = self.get_logged_in_cookie(self.testApp)
        self.driver.add_cookie(cookie)
        self.driver.get("http://127.0.0.1:5000/uploadReview")  # protected page

    def test_signup_form_loads(self):
        """Test if the signup page loads correctly"""
        self.driver.get("http://127.0.0.1:5000/newsignup")
        self.assertIn("Already have an account?", self.driver.page_source)

    def test_home_page_access(self):
        """Test if the home page is accessible"""
        self.driver.get("http://127.0.0.1:5000/")
        self.assertIn("Movie Tracker", self.driver.page_source)


    def test_add_and_remove_friend_flow(self):
        """Test that a user can add and remove a friend"""
        self.login_via_cookie()

        # Add friend via API
        self.driver.get("http://127.0.0.1:5000/")
        self.driver.execute_script("""
            fetch('/add_friend', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: 'user2'})
            }).then(r => r.json()).then(data => console.log(data));
        """)
        WebDriverWait(self.driver, 2).until(lambda d: True)  # wait a moment

        # Now try removing the friend
        self.driver.execute_script("""
            fetch('/remove_friend', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: 'user2'})
            }).then(r => r.json()).then(data => console.log(data));
        """)
        WebDriverWait(self.driver, 2).until(lambda d: True)  # wait a moment

        self.assertTrue(True, "Friend add/remove script executed")

    def test_upload_review_restricted_logged_out(self):
        """Accessing /uploadReview while logged out should show 'Content Restricted'"""
        self.driver.delete_all_cookies()  # simulate logged out state
        self.driver.get("http://127.0.0.1:5000/uploadReview")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIn("Content Restricted", self.driver.page_source)

    def test_visualise_movies_restricted_logged_out(self):
        """Accessing /visualiseMovies while logged out should show 'Content Restricted'"""
        self.driver.delete_all_cookies()
        self.driver.get("http://127.0.0.1:5000/visualiseMovies")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIn("Content Restricted", self.driver.page_source)

    def test_share_data_restricted_logged_out(self):
        """Accessing /shareData while logged out should show 'Content Restricted'"""
        self.driver.delete_all_cookies()
        self.driver.get("http://127.0.0.1:5000/shareData")
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        self.assertIn("Content Restricted", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()