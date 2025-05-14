import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestTravelRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8072/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('recommendations'))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Test registration page display
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        self.assertIn('Register', self.driver.title)
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Preferences'))
        
        # Test duplicate registration
        self.driver.get('http://localhost:8072/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertIn('Username and password required', error_message)

    # Functionality 2: User Login
    def test_user_login(self):
        # Test login page display
        self.assertIn('Login', self.driver.title)
        
        # Test successful login
        self.login('admin', 'admin123')
        self.assertIn('Recommendations', self.driver.title)
        
        # Test invalid login
        self.driver.get('http://localhost:8072/login')
        self.driver.find_element(By.NAME, 'username').send_keys('wronguser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CSS_SELECTOR, 'p[style="color: red;"]').text
        self.assertIn('Invalid credentials', error_message)

    # Functionality 3: Input Travel Preferences
    def test_input_travel_preferences(self):
        self.login('admin', 'admin123')
        
        # Navigate to preferences page
        self.driver.find_element(By.LINK_TEXT, 'Update Preferences').click()
        self.wait.until(EC.title_contains('Preferences'))
        
        # Test preferences form submission
        self.driver.find_element(By.NAME, 'budget').clear()
        self.driver.find_element(By.NAME, 'budget').send_keys('1000')
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="activities"][value="hiking"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'input[name="activities"][value="beach"]').click()
        self.driver.find_element(By.NAME, 'climate').send_keys('warm')
        self.driver.find_element(By.XPATH, '//button[text()="Save Preferences"]').click()
        self.wait.until(EC.title_contains('Recommendations'))

    # Functionality 4: Generate Travel Recommendations
    def test_generate_travel_recommendations(self):
        self.login('admin', 'admin123')
        
        # Check if recommendations are displayed
        recommendations = self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3')
        self.assertGreater(len(recommendations), 0, "No recommendations found")
        
        # Test viewing destination details
        first_rec = recommendations[0]
        destination_name = first_rec.text
        first_rec.find_element(By.XPATH, './following-sibling::a').click()
        self.wait.until(EC.title_contains('Details'))
        self.assertIn(destination_name, self.driver.page_source)

    # Functionality 5: Save Favorite Destinations
    def test_save_favorite_destinations(self):
        self.login('admin', 'admin123')
        
        # Get first recommendation
        first_rec = self.driver.find_element(By.CSS_SELECTOR, 'ul li h3')
        destination_name = first_rec.text
        
        # Go to details page and save as favorite
        first_rec.find_element(By.XPATH, './following-sibling::a').click()
        self.wait.until(EC.title_contains('Details'))
        self.driver.find_element(By.LINK_TEXT, 'Save as Favorite').click()
        
        # Verify we're back on details page
        self.wait.until(EC.title_contains('Details'))
        self.assertIn(destination_name, self.driver.page_source)

    # Functionality 6: User Logout
    def test_user_logout(self):
        self.login('admin', 'admin123')
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test access after logout
        self.driver.get('http://localhost:8072/recommendations')
        self.wait.until(EC.title_contains('Login'))

    # Functionality 7: View Detailed Information About Destinations
    def test_view_destination_details(self):
        self.login('admin', 'admin123')
        
        # Get all recommendations
        recommendations = self.driver.find_elements(By.CSS_SELECTOR, 'ul li h3')
        self.assertGreater(len(recommendations), 0, "No recommendations found")
        
        # Test viewing details for each recommendation
        for rec in recommendations:
            destination_name = rec.text
            rec.find_element(By.XPATH, './following-sibling::a').click()
            self.wait.until(EC.title_contains('Details'))
            self.assertIn(destination_name, self.driver.page_source)
            self.driver.find_element(By.LINK_TEXT, 'Back to Recommendations').click()
            self.wait.until(EC.title_contains('Recommendations'))

if __name__ == '__main__':
    unittest.main()
