import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8352/')  # Access the login page

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
        self.driver.get('http://localhost:8352/register')  # Navigate to registration page
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login
        self.login("admin", "admin123")  # Valid credentials

        # Verify redirection to search page
        self.assertIn("Search Movies", self.driver.title)

    def test_search_movies(self):
        # Functionalities 4: Test searching for movies
        self.login("admin", "admin123")  # Log in first
        search_query = "Inception"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results contain the movie
        self.assertIn("Inception", self.driver.page_source)

    def test_view_movie_details(self):
        # Functionalities 5: Test viewing movie details
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, "Inception").click()  # Click on the movie link

        # Verify that movie details are displayed
        self.assertIn("Inception", self.driver.page_source)
        self.assertIn("A thief who steals corporate secrets", self.driver.page_source)

    def test_add_to_favorites(self):
        # Functionalities 6: Test adding a movie to favorites
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, "Inception").click()  # Click on the movie link
        self.driver.find_element(By.XPATH, '//button[text()="Add to Favorites"]').click()

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:8352/favorites')  # Navigate to favorites page
        self.assertIn("Inception", self.driver.page_source)

    def test_view_favorites(self):
        # Functionalities 7: Test viewing favorites list
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8352/favorites')  # Navigate to favorites page

        # Verify that the favorites list is displayed
        self.assertIn("Inception", self.driver.page_source)

    def test_remove_from_favorites(self):
        # Functionalities 8: Test removing a movie from favorites
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8352/favorites')  # Navigate to favorites page
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()  # Assuming a remove button exists

        # Verify that the movie is removed from favorites
        self.assertNotIn("Inception", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 9: Verify the structure of the local text files
        with open('favorites.txt', 'r') as file:
            lines = file.readlines()
            self.assertTrue(all('|' in line for line in lines), "Favorites file format is incorrect.")

        with open('users.txt', 'r') as file:
            lines = file.readlines()
            self.assertTrue(all('|' in line for line in lines), "Users file format is incorrect.")

        with open('movies.txt', 'r') as file:
            lines = file.readlines()
            self.assertTrue(all('|' in line for line in lines), "Movies file format is incorrect.")

if __name__ == '__main__':
    unittest.main()
