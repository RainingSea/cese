import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestTravelTipperApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8066/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get('http://localhost:8066/login')
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def logout(self):
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Test duplicate username registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        self.driver.find_element(By.ID, 'username').send_keys('user1')
        self.driver.find_element(By.ID, 'password').send_keys('password1')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn('Username already exists', error_message)

    # Functionality 2: User Login
    def test_user_login(self):
        # Test successful login
        self.login('user1', 'password1')
        self.assertIn('Dashboard', self.driver.title)
        self.logout()
        
        # Test invalid login
        self.driver.find_element(By.ID, 'username').send_keys('invalid')
        self.driver.find_element(By.ID, 'password').send_keys('invalid')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertIn('Invalid credentials', error_message)

    # Functionality 3: Input Travel Details
    def test_input_travel_details(self):
        self.login('user1', 'password1')
        
        # Navigate to tips page via form submission
        destination = "Paris"
        interests = "Food"
        self.driver.find_element(By.ID, 'destination').send_keys(destination)
        self.driver.find_element(By.ID, 'interests').send_keys(interests)
        self.driver.find_element(By.XPATH, '//button[text()="Get Travel Tips"]').click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Verify tips are displayed
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip')
        self.assertGreater(len(tips), 0)
        
        # Test incomplete form submission
        self.driver.get('http://localhost:8066/dashboard')
        self.driver.find_element(By.XPATH, '//button[text()="Get Travel Tips"]').click()
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip')
        self.assertGreater(len(tips), 0)  # Should show all tips when no filters

    # Functionality 4: View Recommendations
    def test_view_recommendations(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Verify recommendations are displayed
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip')
        self.assertGreater(len(tips), 0)
        
        # Refresh and verify recommendations remain
        self.driver.refresh()
        self.wait.until(EC.title_contains('Tips'))
        refreshed_tips = self.driver.find_elements(By.CLASS_NAME, 'tip')
        self.assertEqual(len(tips), len(refreshed_tips))

    # Functionality 5: Search for Tips
    def test_search_tips(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Test search with existing term
        search_input = self.driver.find_element(By.NAME, 'search')
        search_input.send_keys('croissants')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        tips = self.driver.find_elements(By.CLASS_NAME, 'tip')
        self.assertGreater(len(tips), 0)
        
        # Test search with non-existent term
        search_input = self.driver.find_element(By.NAME, 'search')
        search_input.clear()
        search_input.send_keys('nonexistentterm')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        no_tips_message = self.driver.find_element(By.XPATH, '//p[contains(text(), "No tips found")]').text
        self.assertIn('No tips found', no_tips_message)

    # Functionality 6: Save Favorite Travel Tips
    def test_save_favorite_tips(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Save a favorite
        save_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Save to Favorites"]')
        save_buttons[0].click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Verify favorite was saved
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        favorites = self.driver.find_elements(By.CLASS_NAME, 'favorite')
        self.assertGreater(len(favorites), 0)
        
        # Try to save the same tip again
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.wait.until(EC.title_contains('Tips'))
        save_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Save to Favorites"]')
        save_buttons[0].click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Check favorites count remains the same (no duplicates)
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        updated_favorites = self.driver.find_elements(By.CLASS_NAME, 'favorite')
        self.assertEqual(len(favorites), len(updated_favorites))

    # Functionality 7: User Logout
    def test_user_logout(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        
        # Try to access dashboard after logout
        self.driver.get('http://localhost:8066/dashboard')
        self.wait.until(EC.title_contains('Login'))

    # Functionality 8: Navigate Back to Dashboard
    def test_navigate_back_to_dashboard(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Tips').click()
        self.wait.until(EC.title_contains('Tips'))
        
        # Navigate back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Dashboard').click()
        self.wait.until(EC.title_contains('Dashboard'))
        
        # Verify form is present
        form = self.driver.find_element(By.TAG_NAME, 'form')
        self.assertIsNotNone(form)

    # Functionality 9: View Saved Travel Tips
    def test_view_saved_tips(self):
        self.login('user1', 'password1')
        self.driver.find_element(By.LINK_TEXT, 'Favorites').click()
        self.wait.until(EC.title_contains('Favorites'))
        
        # Verify favorites are displayed
        favorites = self.driver.find_elements(By.CLASS_NAME, 'favorite')
        self.assertGreater(len(favorites), 0)
        
        # Test removing a favorite
        remove_button = favorites[0].find_element(By.XPATH, './/button[text()="Remove"]')
        remove_button.click()
        self.wait.until(EC.title_contains('Favorites'))
        updated_favorites = self.driver.find_elements(By.CLASS_NAME, 'favorite')
        self.assertLess(len(updated_favorites), len(favorites))

if __name__ == '__main__':
    unittest.main()
