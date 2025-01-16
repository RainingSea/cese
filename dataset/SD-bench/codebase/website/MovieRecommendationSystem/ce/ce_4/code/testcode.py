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
        self.driver.get('http://localhost:8650/')  # Access the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Functionalities 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the Recommendations Page has loaded
        self.assertIn("Movie Recommendations", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: View Movie Recommendations
        self.login("admin", "admin123")

        # Verify that the Recommendations Page shows movies
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No movie recommendations found.")

    def test_search_for_movies(self):
        # Functionalities 4: Search for Movies
        self.fail("Search functionality not implemented")

    def test_view_movie_details(self):
        # Functionalities 5: View Movie Details
        self.login("admin", "admin123")

        # Click on the first movie link
        movie_link = self.driver.find_element(By.TAG_NAME, 'a')
        movie_link.click()
        time.sleep(1)  # Wait for the movie detail page to load

        # Verify that the movie details are displayed
        self.assertIn("Rating:", self.driver.page_source)

    def test_add_movies_to_favorites(self):
        # Functionalities 6: Add Movies to Favorites
        self.fail("Add to favorites functionality not implemented")

    def test_view_favorites_list(self):
        # Functionalities 7: View Favorites List
        self.login("admin", "admin123")

        # Navigate to the favorites page
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        time.sleep(1)  # Wait for the favorites page to load

        # Verify that the favorites list is displayed
        self.assertIn("Your Favorite Movies", self.driver.page_source)

    def test_remove_movies_from_favorites(self):
        # Functionalities 8: Remove Movies from Favorites
        self.fail("Remove from favorites functionality not implemented")

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Data Storage and Retrieval
        self.fail("Data storage and retrieval functionality not implemented")

if __name__ == '__main__':
    unittest.main()
