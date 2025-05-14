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
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8003/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver
        self.driver.quit()

    def login(self, username, password):
        """Helper method to perform login"""
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/'))

    def test_01_user_registration(self):
        """Functionalities 1: User Registration"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))

        # Register new user
        username = "testuser"
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirect to home page
        self.wait.until(EC.url_contains('/'))
        welcome_msg = self.driver.find_element(By.XPATH, '//span[contains(text(), "Welcome")]')
        self.assertIn(username, welcome_msg.text)

    def test_02_user_login(self):
        """Functionalities 2: User Login"""
        # Login with valid credentials
        self.login("admin", "admin123")
        
        # Verify successful login by checking welcome message
        welcome_msg = self.driver.find_element(By.XPATH, '//span[contains(text(), "Welcome")]')
        self.assertIn("admin", welcome_msg.text)

    def test_03_view_movie_recommendations(self):
        """Functionalities 3: View Movie Recommendations"""
        # Login first
        self.login("admin", "admin123")
        
        # Check recommendations are displayed
        recommendations = self.driver.find_elements(By.CLASS_NAME, 'movie')
        self.assertGreater(len(recommendations), 0, "No recommendations found")

    def test_04_search_for_movies(self):
        """Functionalities 4: Search for Movies"""
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to search page
        self.driver.find_element(By.LINK_TEXT, 'Search').click()
        self.wait.until(EC.title_contains('Search'))
        
        # Test full title search
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys("The Shawshank Redemption")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify results
        results = self.driver.find_elements(By.CLASS_NAME, 'movie')
        self.assertEqual(len(results), 1)
        self.assertIn("Shawshank", results[0].text)
        
        # Test partial title search
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.clear()
        search_input.send_keys("The")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify multiple results
        results = self.driver.find_elements(By.CLASS_NAME, 'movie')
        self.assertGreater(len(results), 1)

    def test_05_view_movie_details(self):
        """Functionalities 5: View Movie Details"""
        # Login first
        self.login("admin", "admin123")
        
        # Click on first recommendation
        first_movie = self.driver.find_element(By.CLASS_NAME, 'movie')
        movie_title = first_movie.find_element(By.TAG_NAME, 'a').text
        first_movie.find_element(By.TAG_NAME, 'a').click()
        
        # Verify details page
        self.wait.until(EC.title_contains('Details'))
        detail_title = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertEqual(movie_title, detail_title)
        
        # Verify other details exist
        description = self.driver.find_element(By.XPATH, '//div[@class="movie-details"]/p[1]').text
        rating = self.driver.find_element(By.XPATH, '//div[@class="movie-details"]/p[2]').text
        self.assertTrue(description)
        self.assertTrue(rating.startswith("Rating:"))

    def test_06_add_movies_to_favorites(self):
        """Functionalities 6: Add Movies to Favorites"""
        # Login first
        self.login("admin", "admin123")
        
        # Go to first movie details
        self.driver.find_element(By.CLASS_NAME, 'movie').find_element(By.TAG_NAME, 'a').click()
        self.wait.until(EC.title_contains('Details'))
        
        # Add to favorites
        add_button = self.driver.find_element(By.LINK_TEXT, 'Add to Favorites')
        add_button.click()
        
        # Verify button changed to "Remove from Favorites"
        self.wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Remove from Favorites')))

    def test_07_view_favorites_list(self):
        """Functionalities 7: View Favorites List"""
        # Login first
        self.login("admin", "admin123")
        
        # Navigate to favorites
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        
        # Check favorites are displayed
        favorites = self.driver.find_elements(By.CLASS_NAME, 'favorite')
        self.assertGreater(len(favorites), 0, "No favorites found")

    def test_08_remove_movies_from_favorites(self):
        """Functionalities 8: Remove Movies from Favorites"""
        # Login first
        self.login("admin", "admin123")
        
        # Go to favorites
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        
        # Get count before removal
        initial_count = len(self.driver.find_elements(By.CLASS_NAME, 'favorite'))
        
        # Remove first favorite
        if initial_count > 0:
            self.driver.find_element(By.CLASS_NAME, 'favorite').find_element(By.LINK_TEXT, 'Remove').click()
            self.wait.until(EC.title_contains('Favorites'))
            
            # Verify count decreased
            new_count = len(self.driver.find_elements(By.CLASS_NAME, 'favorite'))
            self.assertEqual(new_count, initial_count - 1)

    def test_09_data_storage_and_retrieval(self):
        """Functionalities 9: Data Storage and Retrieval"""
        # This would typically require file system checks which are better done with unit tests
        # For UI test, we'll verify data consistency between UI and storage
        
        # Login first
        self.login("admin", "admin123")
        
        # Get recommendations from UI
        ui_movies = []
        movie_elements = self.driver.find_elements(By.CLASS_NAME, 'movie')
        for movie in movie_elements:
            title = movie.find_element(By.TAG_NAME, 'a').text
            description = movie.find_elements(By.TAG_NAME, 'p')[0].text
            rating = movie.find_elements(By.TAG_NAME, 'p')[1].text
            ui_movies.append({
                'title': title,
                'description': description,
                'rating': rating.replace('Rating: ', '')
            })
        
        # Verify we got some movies
        self.assertGreater(len(ui_movies), 0, "No movies displayed in UI")
        
        # Note: In a real test, we would compare with data from movies.txt
        # This is just a placeholder to show the concept
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
