import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestMovieRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8004/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Home'))

    def test_user_registration(self):
        """Functionalities 1: User Registration"""
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[@name="register"]').click()
        
        # Verify we're back on login page
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    def test_user_login(self):
        """Functionalities 2: User Login"""
        self.login("user1", "password1")
        self.assertIn('Welcome', self.driver.page_source)
        self.assertIn('user1', self.driver.page_source)

    def test_view_movie_recommendations(self):
        """Functionalities 3: View Movie Recommendations"""
        self.login("user1", "password1")
        
        # Check if recommendations are displayed
        movies = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(movies), 0, "No recommendations displayed")

    def test_search_movies(self):
        """Functionalities 4: Search for Movies"""
        self.login("user1", "password1")
        
        # Search by full title
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("The Shawshank Redemption")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        self.wait.until(EC.title_contains('Search'))
        results = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertEqual(len(results), 1)
        self.assertIn("The Shawshank Redemption", self.driver.page_source)
        
        # Search by partial title
        self.driver.find_element(By.NAME, 'query').clear()
        self.driver.find_element(By.NAME, 'query').send_keys("The")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        results = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(results), 1)

    def test_view_movie_details(self):
        """Functionalities 5: View Movie Details"""
        self.login("user1", "password1")
        
        # Click on first movie in recommendations
        movie_link = self.driver.find_element(By.XPATH, '//ul/li/a')
        movie_title = movie_link.text
        movie_link.click()
        
        self.wait.until(EC.title_contains(movie_title))
        self.assertIn(movie_title, self.driver.page_source)
        self.assertIn('Rating', self.driver.page_source)
        self.assertIn('Genres', self.driver.page_source)

    def test_add_movie_to_favorites(self):
        """Functionalities 6: Add Movies to Favorites"""
        self.login("user1", "password1")
        
        # Go to movie details page
        movie_link = self.driver.find_element(By.XPATH, '//ul/li/a')
        movie_title = movie_link.text
        movie_link.click()
        
        # Add to favorites
        self.driver.find_element(By.XPATH, '//button[text()="Add to Favorites"]').click()
        
        # Verify button changed (if implemented) or check favorites list
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        self.assertIn(movie_title, self.driver.page_source)

    def test_view_favorites_list(self):
        """Functionalities 7: View Favorites List"""
        self.login("user1", "password1")
        
        # Go to favorites page
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        
        # Check if favorites are displayed
        favorites = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(favorites), 0, "No favorites displayed")

    def test_remove_movie_from_favorites(self):
        """Functionalities 8: Remove Movies from Favorites"""
        self.login("user1", "password1")
        
        # Go to favorites page
        self.driver.find_element(By.LINK_TEXT, 'View Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        
        # Get initial count of favorites
        initial_favorites = self.driver.find_elements(By.XPATH, '//ul/li')
        
        # Remove first favorite
        if len(initial_favorites) > 0:
            remove_btn = self.driver.find_element(By.XPATH, '//button[text()="Remove"]')
            movie_title = self.driver.find_element(By.XPATH, '//ul/li/a').text
            remove_btn.click()
            
            # Verify removed
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, f'//a[text()="{movie_title}"]')))
            current_favorites = self.driver.find_elements(By.XPATH, '//ul/li')
            self.assertEqual(len(current_favorites), len(initial_favorites) - 1)

    def test_data_storage_and_retrieval(self):
        """Functionalities 9: Data Storage and Retrieval"""
        # This would typically involve checking the files directly,
        # but since we're doing black box testing, we'll verify through the UI
        
        self.login("user1", "password1")
        
        # Verify displayed data matches expected from files
        movie_link = self.driver.find_element(By.XPATH, '//ul/li/a')
        movie_title = movie_link.text
        movie_link.click()
        
        # Check details match expected format
        rating = self.driver.find_element(By.XPATH, '//p[contains(., "Rating:")]').text
        genres = self.driver.find_element(By.XPATH, '//p[contains(., "Genres:")]').text
        description = self.driver.find_element(By.XPATH, '//p[not(contains(., "Rating:")) and not(contains(., "Genres:"))]').text
        
        self.assertTrue(rating.startswith('Rating: '))
        self.assertTrue(genres.startswith('Genres: '))
        self.assertTrue(len(description) > 0)

if __name__ == '__main__':
    unittest.main()
