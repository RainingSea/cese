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
        self.driver.get('http://localhost:8539/')

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
        # Functionalities 1: Test user registration
        self.driver.get('http://localhost:8539/register')
        new_username = "testuser"
        new_password = "testpass"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the home page
        self.assertIn("Home", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: Test viewing movie recommendations
        self.login("admin", "admin123")

        # Verify that the recommendations are displayed
        recommendations = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(recommendations), 0, "No movie recommendations found.")

    def test_search_for_movies(self):
        # Functionalities 4: Test searching for movies
        self.login("admin", "admin123")
        search_query = "Inception"

        # Perform search
        self.driver.get(f'http://localhost:8539/movie/{search_query}')
        time.sleep(1)  # Wait for the search results to load

        # Verify that the correct movie is displayed
        movie_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn(search_query, movie_title)

    def test_view_movie_details(self):
        # Functionalities 5: Test viewing movie details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8539/movie/Inception')
        time.sleep(1)  # Wait for the movie details to load

        # Verify that the movie details are displayed correctly
        movie_details = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Inception", movie_details)
        self.assertIn("A thief who steals corporate secrets", movie_details)

    def test_add_movies_to_favorites(self):
        # Functionalities 6: Test adding movies to favorites
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8539/add_favorite/Inception')
        time.sleep(1)  # Wait for the action to complete

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:8539/favorites')
        favorites = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Inception", favorites)

    def test_view_favorites_list(self):
        # Functionalities 7: Test viewing favorites list
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8539/favorites')
        time.sleep(1)  # Wait for the favorites list to load

        # Verify that the favorites list is displayed correctly
        favorites = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertIn("Inception", favorites)

    def test_remove_movies_from_favorites(self):
        # Functionalities 8: Test removing movies from favorites
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8539/remove_favorite/Inception')
        time.sleep(1)  # Wait for the action to complete

        # Verify that the movie is removed from favorites
        self.driver.get('http://localhost:8539/favorites')
        favorites = self.driver.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn("Inception", favorites)

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Test data storage and retrieval
        # Verify the structure of the local text files
        with open('users.txt', 'r') as file:
            users_data = file.read()
            self.assertIn("admin|admin123", users_data)

        with open('movies.txt', 'r') as file:
            movies_data = file.read()
            self.assertIn("Inception|A thief who steals corporate secrets", movies_data)

if __name__ == '__main__':
    unittest.main()
