import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMovieRecommendationSystem(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8646/login') 

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

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

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_view_movie_recommendations(self):
        # Functionalities 3: View Movie Recommendations
        self.login("user1", "user123")

        # Verify that the Home Page shows movie recommendations
        movies = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(movies), 0, "No movie recommendations found.")

    def test_search_for_movies(self):
        # Functionalities 4: Search for Movies
        self.login("user1", "user123")

        # Search for a movie
        search_box = self.driver.find_element(By.ID, 'search')
        search_box.send_keys("Inception")
        search_box.submit()
        time.sleep(1)  # Wait for search results

        # Verify that the search results contain the movie
        self.assertIn("Inception", self.driver.page_source)

    def test_view_movie_details(self):
        # Functionalities 5: View Movie Details
        self.fail("Not implemented")

    def test_add_movies_to_favorites(self):
        # Functionalities 6: Add Movies to Favorites
        self.fail("Not implemented")

    def test_view_favorites_list(self):
        # Functionalities 7: View Favorites List
        self.fail("Not implemented")

    def test_remove_movies_from_favorites(self):
        # Functionalities 8: Remove Movies from Favorites
        self.fail("Not implemented")

    def test_data_storage_and_retrieval(self):
        # Functionalities 9: Data Storage and Retrieval
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
