import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/') 

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_registration(self):
        # Functionalities 1: User Registration
        self.driver.get('http://localhost:8000/register')
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
        self.login("user1", "user123")

        # Verify that the recommendations page has loaded
        self.assertIn("Recommendations", self.driver.title)

    def test_view_recommendations(self):
        # Functionalities 3: View Movie Recommendations
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/recommendations')

        # Verify that the recommendations are displayed
        self.assertIn("Movie Recommendations", self.driver.page_source)

    def test_search_movies(self):
        # Functionalities 4: Search for Movies
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/search?query=Inception')

        # Verify that the search results contain the movie
        self.assertIn("Inception", self.driver.page_source)

    def test_view_movie_details(self):
        # Functionalities 5: View Movie Details
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/movie_details?title=Inception')

        # Verify that the movie details are displayed
        self.assertIn("Inception", self.driver.page_source)
        self.assertIn("A thief who steals corporate secrets", self.driver.page_source)

    def test_add_to_favorites(self):
        # Functionalities 6: Add Movies to Favorites
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/movie_details?title=Inception')
        self.driver.find_element(By.XPATH, '//button[text()="Add to Favorites"]').click()

        # Verify that the movie is added to favorites
        self.driver.get('http://localhost:8000/favorites')
        self.assertIn("Inception", self.driver.page_source)

    def test_view_favorites(self):
        # Functionalities 7: View Favorites List
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/favorites')

        # Verify that the favorites list is displayed
        self.assertIn("Your Favorite Movies", self.driver.page_source)

    def test_remove_from_favorites(self):
        # Functionalities 8: Remove Movies from Favorites
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/movie_details?title=Inception')
        self.driver.find_element(By.XPATH, '//button[text()="Remove from Favorites"]').click()

        # Verify that the movie is removed from favorites
        self.driver.get('http://localhost:8000/favorites')
        self.assertNotIn("Inception", self.driver.page_source)

    def test_data_storage(self):
        # Functionalities 9: Data Storage and Retrieval
        # Verify the structure of the local text files used for storing data
        with open('users.txt', 'r') as file:
            users = file.readlines()
            self.assertGreater(len(users), 0, "Users file is empty.")

        with open('movies.txt', 'r') as file:
            movies = file.readlines()
            self.assertGreater(len(movies), 0, "Movies file is empty.")

        with open('favorites.txt', 'r') as file:
            favorites = file.readlines()
            self.assertGreater(len(favorites), 0, "Favorites file is empty.")

if __name__ == '__main__':
    unittest.main()
