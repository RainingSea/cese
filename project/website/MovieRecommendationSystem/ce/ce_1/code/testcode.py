import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8351/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionalities 1: Test user registration
        self.driver.get('http://localhost:8351/register')  # Navigate to registration page
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login
        self.login("admin", "admin123")  # Use valid credentials

        # Verify redirection to the recommendations page
        self.assertIn("Movie Recommendations", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: Test viewing movie recommendations
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8351/recommendations')  # Navigate to recommendations page

        # Check if recommendations are displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No recommendations found.")

    def test_search_movies(self):
        # Functionalities 4: Test searching for movies
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8351/search')  # Navigate to search page

        # Search for a valid movie title
        self.driver.find_element(By.NAME, 'query').send_keys("Inception")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results are displayed
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0, "No search results found for 'Inception'.")

    def test_add_to_favorites(self):
        # Functionalities 6: Test adding a movie to favorites
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8351/search')  # Navigate to search page

        # Search for a movie and add to favorites
        self.driver.find_element(By.NAME, 'query').send_keys("Inception")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Inception")]/following-sibling::button[text()="Add to Favorites"]').click()

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:8351/favorites')  # Navigate to favorites page
        favorites = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("Inception", [fav.text for fav in favorites], "Inception was not found in favorites.")

    def test_view_favorites(self):
        # Functionalities 7: Test viewing favorites list
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8351/favorites')  # Navigate to favorites page

        # Verify that the favorites list is displayed
        favorites = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(favorites), 0, "Favorites list is empty.")

    def test_remove_from_favorites(self):
        # Functionalities 8: Test removing a movie from favorites
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8351/favorites')  # Navigate to favorites page

        # Remove a movie from favorites
        self.driver.find_element(By.XPATH, '//li[contains(text(), "Inception")]/following-sibling::button[text()="Remove from Favorites"]').click()

        # Verify that the movie is removed from favorites
        favorites = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertNotIn("Inception", [fav.text for fav in favorites], "Inception was not removed from favorites.")

if __name__ == '__main__':
    unittest.main()
