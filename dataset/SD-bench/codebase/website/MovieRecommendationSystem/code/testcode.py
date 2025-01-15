import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8651/')

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
        # Functionalities 2: User Login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the recommendations page
        self.assertIn("Movie Recommendations", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: View Movie Recommendations
        self.login("admin", "admin123")

        # Verify that the recommendations page displays a list of movies
        movies = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(movies), 0, "No movie recommendations found.")

    def test_search_for_movies(self):
        # Functionalities 4: Search for Movies
        self.login("admin", "admin123")

        # Search for a movie
        self.driver.find_element(By.NAME, 'query').send_keys("Inception")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        # Verify that the search results contain the movie
        self.assertIn("Inception", self.driver.page_source)

    def test_view_movie_details(self):
        # Functionalities 5: View Movie Details
        self.login("admin", "admin123")

        # Click on a movie to view details
        self.driver.find_element(By.LINK_TEXT, 'Inception').click()
        time.sleep(1)  # Wait for the movie details page to load

        # Verify that the movie details are displayed
        self.assertIn("Inception", self.driver.page_source)

    def test_add_movies_to_favorites(self):
        # Functionalities 6: Add Movies to Favorites
        self.login("admin", "admin123")

        # Add a movie to favorites
        self.driver.find_element(By.LINK_TEXT, 'Add to Favorites').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the movie is added to favorites
        self.driver.find_element(By.LINK_TEXT, 'Your Favorites').click()
        time.sleep(1)  # Wait for the favorites page to load
        self.assertIn("Inception", self.driver.page_source)

    def test_view_favorites_list(self):
        # Functionalities 7: View Favorites List
        self.login("admin", "admin123")

        # Navigate to the favorites list
        self.driver.find_element(By.LINK_TEXT, 'Your Favorites').click()
        time.sleep(1)  # Wait for the favorites page to load

        # Verify that the favorites list shows all added movies
        self.assertIn("Inception", self.driver.page_source)

    def test_remove_movies_from_favorites(self):
        # Functionalities 8: Remove Movies from Favorites
        self.login("admin", "admin123")

        # Remove a movie from favorites
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify that the movie is removed from favorites
        self.assertNotIn("Inception", self.driver.page_source)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Data Storage and Retrieval
        # This test point is not directly testable via UI, so we assume it's implemented correctly.
        self.fail("Data storage and retrieval test not implemented in UI")

if __name__ == '__main__':
    unittest.main()
