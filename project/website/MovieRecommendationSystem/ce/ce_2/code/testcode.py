import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_user_registration(self):
        # Functionalities 1: Test user registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.ID, 'username').send_keys(new_username)
        self.driver.find_element(By.ID, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_user_login(self):
        # Functionalities 2: Test user login
        self.login("admin", "admin123")

        # Verify that the user is redirected to the recommendations page
        self.assertIn("Recommendations", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: Test viewing movie recommendations
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/recommendations')  # Navigate to recommendations page

        # Verify that the recommendations are displayed
        self.assertIn("Inception", self.driver.page_source)
        self.assertIn("The Matrix", self.driver.page_source)

    def test_search_movies(self):
        # Functionalities 4: Test searching for movies
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/search')  # Navigate to search page

        # Search for a valid movie title
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("Inception")
        search_box.submit()

        # Verify that the correct movie is displayed
        self.assertIn("Inception", self.driver.page_source)

        # Search with part of a movie title
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.clear()
        search_box.send_keys("Matrix")
        search_box.submit()

        # Verify that the correct movie is displayed
        self.assertIn("The Matrix", self.driver.page_source)

    def test_view_movie_details(self):
        # Functionalities 5: Test viewing movie details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/movie/1')  # Navigate to movie details page

        # Verify that the movie details are displayed correctly
        self.assertIn("Inception", self.driver.page_source)
        self.assertIn("A thief who steals corporate secrets", self.driver.page_source)

    def test_add_to_favorites(self):
        # Functionalities 6: Test adding a movie to favorites
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/movie/1')  # Navigate to movie details page
        self.driver.find_element(By.XPATH, '//input[@value="Add to Favorites"]').click()

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:5000/favorites')  # Navigate to favorites page
        self.assertIn("Inception", self.driver.page_source)

    def test_remove_from_favorites(self):
        # Functionalities 8: Test removing a movie from favorites
        self.login("admin", "admin123")
        self.driver.get('http://localhost:5000/movie/1')  # Navigate to movie details page
        self.driver.find_element(By.XPATH, '//input[@value="Add to Favorites"]').click()  # Add to favorites
        self.driver.get('http://localhost:5000/favorites')  # Navigate to favorites page
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()  # Remove from favorites

        # Verify that the movie is removed from favorites
        self.assertNotIn("Inception", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 9: Test data storage and retrieval
        with open('users.txt', 'r') as file:
            users = file.readlines()
            self.assertGreater(len(users), 0, "User data file is empty.")

        with open('movies.txt', 'r') as file:
            movies = file.readlines()
            self.assertGreater(len(movies), 0, "Movies data file is empty.")

if __name__ == '__main__':
    unittest.main()
