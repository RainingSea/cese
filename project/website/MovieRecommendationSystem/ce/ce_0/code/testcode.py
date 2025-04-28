import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:8000/register')  # Navigate to registration page
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionalities 2: User Login
        self.login("user1", "user123")  # Use valid credentials

        # Verify that the user is redirected to the recommendations page
        self.assertIn("Recommended Movies", self.driver.page_source)

    def test_view_recommendations(self):
        # Functionalities 3: View Movie Recommendations
        self.login("user1", "user123")  # Log in first

        # Verify that the recommendations page displays movies
        self.assertIn("Recommended Movies", self.driver.page_source)

    def test_search_movies(self):
        # Functionalities 4: Search for Movies
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8000/search')  # Navigate to search page

        # Search for a valid movie title
        self.driver.find_element(By.NAME, 'query').send_keys("Inception")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the search results contain the movie
        self.assertIn("Inception", self.driver.page_source)

        # Search with part of a movie title
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("The")
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the search results contain the movie
        self.assertIn("The Matrix", self.driver.page_source)

    def test_view_favorites(self):
        # Functionalities 7: View Favorites List
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8000/favorites')  # Navigate to favorites page

        # Verify that the favorites page displays the user's favorites
        self.assertIn("Your Favorite Movies", self.driver.page_source)

    def test_add_to_favorites(self):
        # Functionalities 6: Add Movies to Favorites
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8000/recommendations')  # Navigate to recommendations page

        # Simulate adding a movie to favorites (assuming there's a button for it)
        self.driver.find_element(By.XPATH, '//button[text()="Add to Favorites"]').click()

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:8000/favorites')  # Navigate to favorites page
        self.assertIn("Inception", self.driver.page_source)  # Check if the movie appears in favorites

    def test_remove_from_favorites(self):
        # Functionalities 8: Remove Movies from Favorites
        self.login("user1", "user123")  # Log in first
        self.driver.get('http://localhost:8000/favorites')  # Navigate to favorites page

        # Simulate removing a movie from favorites (assuming there's a button for it)
        self.driver.find_element(By.XPATH, '//button[text()="Remove from Favorites"]').click()

        # Verify that the movie is removed from favorites
        self.assertNotIn("Inception", self.driver.page_source)  # Check if the movie is removed

    def test_data_storage(self):
        # Functionalities 9: Data Storage and Retrieval
        # Check if the users.txt file contains the expected user
        with open('users.txt', 'r') as file:
            users = file.readlines()
            self.assertIn("user1|user123\n", users)  # Check if the user exists in the file

if __name__ == '__main__':
    unittest.main()
