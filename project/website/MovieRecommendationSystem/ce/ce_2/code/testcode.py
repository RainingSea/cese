import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8648/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_view_movie_recommendations(self):
        # Test viewing movie recommendations after logging in
        self.login("admin", "admin123")

        # Verify that the Home Page shows recommendations
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No movie recommendations found.")

    def test_view_movie_details(self):
        # Test viewing movie details
        self.login("admin", "admin123")

        # Click on a movie link
        self.driver.find_element(By.LINK_TEXT, 'Movie A').click()
        time.sleep(1)  # Wait for the movie detail page to load

        # Verify that the movie details are displayed
        self.assertIn("Movie A", self.driver.title)
        self.assertIn("A thrilling adventure.", self.driver.page_source)

    def test_add_movies_to_favorites(self):
        # Test adding a movie to the favorites list
        self.login("admin", "admin123")

        # Navigate to movie detail and add to favorites
        self.driver.find_element(By.LINK_TEXT, 'Movie A').click()
        time.sleep(1)  # Wait for the movie detail page to load

        # Simulate adding to favorites (not implemented in UI)
        # This is a placeholder for actual implementation
        self.fail("Add to favorites functionality not implemented in UI")

    def test_view_favorites_list(self):
        # Test viewing the favorites list
        self.login("admin", "admin123")

        # Navigate to favorites page
        self.driver.find_element(By.LINK_TEXT, 'My Favorites').click()
        time.sleep(1)  # Wait for the favorites page to load

        # Verify that the favorites list is displayed
        favorites = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(favorites), 0, "No favorites found.")

    def test_remove_movies_from_favorites(self):
        # Test removing a movie from the favorites list
        self.login("admin", "admin123")

        # Navigate to favorites page
        self.driver.find_element(By.LINK_TEXT, 'My Favorites').click()
        time.sleep(1)  # Wait for the favorites page to load

        # Simulate removing from favorites (not implemented in UI)
        # This is a placeholder for actual implementation
        self.fail("Remove from favorites functionality not implemented in UI")

    def test_data_storage_and_retrieval(self):
        # Test data storage and retrieval
        with open('users.txt', 'r') as file:
            users_data = file.read()
        self.assertIn("admin|admin123", users_data)

        with open('movies.txt', 'r') as file:
            movies_data = file.read()
        self.assertIn("Movie A|A thrilling adventure.|8.5", movies_data)

if __name__ == '__main__':
    unittest.main()
