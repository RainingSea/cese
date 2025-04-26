import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8187/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionalities 1: Register with a valid username and password
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionalities 2: Log in with valid credentials
        self.login("admin", "admin123")

        # Verify that the recommendations page has loaded
        self.assertIn("Movie Recommendations", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: Access the recommendations page after logging in
        self.login("admin", "admin123")
        
        # Verify that the recommendations page displays movies
        movies = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(movies), 0, "No movie recommendations found.")

    def test_search_movies(self):
        # Functionalities 4: Search for movies
        self.login("admin", "admin123")

        # Perform a search for a valid movie title
        search_query = "Inception"
        self.driver.find_element(By.NAME, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results contain the movie
        self.assertIn(search_query, self.driver.page_source)

    def test_view_favorites(self):
        # Functionalities 7: View favorites list
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()

        # Verify that the favorites page is displayed
        self.assertIn("Your Favorites", self.driver.title)

    def test_data_storage_retrieval(self):
        # Functionalities 9: Verify the structure of the local text files used for storing data
        # This is a placeholder test as we cannot directly test file structure through the web interface
        self.fail("Data storage and retrieval functionality not implemented in the web interface.")

if __name__ == '__main__':
    unittest.main()
