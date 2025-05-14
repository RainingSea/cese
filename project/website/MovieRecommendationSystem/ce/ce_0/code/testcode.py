import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestMovieRecommendationSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8002/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Movie App"))

    def test_01_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains("Movie App"))
        
        # Register new user
        username = "testuser"
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirected to login page
        self.wait.until(EC.title_contains("Movie App"))
        self.assertIn("Login", self.driver.title)

    def test_02_user_login(self):
        """Test user login functionality"""
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        welcome_text = self.driver.find_element(By.CLASS_NAME, 'navbar-text').text
        self.assertIn("admin", welcome_text)

    def test_03_view_movie_recommendations(self):
        """Test viewing movie recommendations"""
        self.login("admin", "admin123")
        
        # Check recommendations are displayed
        recommendations = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(recommendations), 0)
        
        # Verify they are sorted by rating (highest first)
        ratings = [float(card.find_element(By.CLASS_NAME, 'badge').text.split()[-1]) 
                  for card in recommendations]
        self.assertEqual(ratings, sorted(ratings, reverse=True))

    def test_04_search_for_movies(self):
        """Test movie search functionality"""
        self.login("admin", "admin123")
        
        # Go to search page
        self.driver.find_element(By.LINK_TEXT, 'Search').click()
        self.wait.until(EC.title_contains("Movie App"))
        
        # Search for exact title
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys("The Shawshank Redemption")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify result
        results = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(results), 1)
        self.assertIn("The Shawshank Redemption", results[0].text)
        
        # Search with partial title
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.clear()
        search_input.send_keys("The")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify multiple results
        results = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(results), 1)

    def test_05_view_movie_details(self):
        """Test viewing movie details"""
        self.login("admin", "admin123")
        
        # Click on first recommendation's details button
        first_movie = self.driver.find_element(By.CLASS_NAME, 'card')
        movie_title = first_movie.find_element(By.CLASS_NAME, 'card-title').text
        first_movie.find_element(By.LINK_TEXT, 'Details').click()
        
        # Verify details page
        self.wait.until(EC.title_contains("Movie App"))
        details_title = self.driver.find_element(By.CLASS_NAME, 'card-title').text
        self.assertEqual(movie_title, details_title)
        
        # Check all details are present
        description = self.driver.find_element(By.CLASS_NAME, 'card-text').text
        self.assertGreater(len(description), 0)
        rating = self.driver.find_element(By.CSS_SELECTOR, '.card-text strong').text
        self.assertIn("Rating", rating)

    def test_06_add_movies_to_favorites(self):
        """Test adding movies to favorites"""
        self.login("admin", "admin123")
        
        # Go to first movie's details
        first_movie = self.driver.find_element(By.CLASS_NAME, 'card')
        first_movie.find_element(By.LINK_TEXT, 'Details').click()
        self.wait.until(EC.title_contains("Movie App"))
        
        # Add to favorites
        add_button = self.driver.find_element(By.LINK_TEXT, 'Add Favorite')
        movie_title = self.driver.find_element(By.CLASS_NAME, 'card-title').text
        add_button.click()
        
        # Verify button changes to Remove Favorite
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Remove Favorite')))

    def test_07_view_favorites_list(self):
        """Test viewing favorites list"""
        self.login("admin", "admin123")
        
        # Go to favorites page
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains("Movie App"))
        
        # Check favorites are displayed (admin has 2 favorites according to favorites.txt)
        favorites = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(favorites), 2)
        
        # Verify the expected movies are present
        page_text = self.driver.page_source
        self.assertIn("The Shawshank Redemption", page_text)
        self.assertIn("The Godfather", page_text)

    def test_08_remove_movies_from_favorites(self):
        """Test removing movies from favorites"""
        self.login("admin", "admin123")
        
        # Go to favorites page
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains("Movie App"))
        
        # Remove first favorite
        first_favorite = self.driver.find_element(By.CLASS_NAME, 'card')
        movie_title = first_favorite.find_element(By.CLASS_NAME, 'card-title').text
        first_favorite.find_element(By.LINK_TEXT, 'Remove').click()
        
        # Verify favorite is removed
        self.wait.until(EC.title_contains("Movie App"))
        remaining_favorites = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(remaining_favorites), 1)
        self.assertNotIn(movie_title, self.driver.page_source)

    def test_09_data_storage_and_retrieval(self):
        """Test data storage and retrieval"""
        # This would normally require file access checks, but we'll verify through UI
        self.login("admin", "admin123")
        
        # Verify recommendations match movies.txt data
        recommendations = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(recommendations), 5)  # Top 5 rated movies
        
        # Verify favorites match favorites.txt data
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        favorites = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertEqual(len(favorites), 2)  # admin has 2 favorites in favorites.txt

if __name__ == '__main__':
    unittest.main()
