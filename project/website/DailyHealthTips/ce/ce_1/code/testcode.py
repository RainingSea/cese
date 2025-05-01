import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

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
        self.driver.get('http://localhost:8571/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'h1'))
        )

    def test_login(self):
        """Functionalities 1: Test user login with valid credentials"""
        self.login("admin", "admin123")
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_navigate_to_registration(self):
        """Functionalities 2: Test navigation to registration page"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        WebDriverWait(self.driver, 5).until(
            EC.title_contains("Register")
        )
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        """Functionalities 3: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        
        # Generate unique username to avoid conflicts
        username = f"testuser{int(time.time())}"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys('testpass123')
        self.driver.find_element(By.ID, 'email').send_keys(f'{username}@test.com')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        WebDriverWait(self.driver, 5).until(
            EC.title_contains("Login")
        )
        self.assertIn("Login", self.driver.title)

    def test_view_current_tip(self):
        """Functionalities 4: Test viewing current daily health tip"""
        self.login("admin", "admin123")
        tip_element = self.driver.find_element(By.XPATH, '//div[contains(text(), "Exercise for 30 minutes daily")]')
        self.assertTrue(tip_element.is_displayed())

    def test_navigate_tips(self):
        """Functionalities 5: Test navigating between tips"""
        # Note: This functionality is not implemented in the codebase
        self.login("admin", "admin123")
        buttons = self.driver.find_elements(By.TAG_NAME, 'button')
        self.assertEqual(len(buttons), 2, "Expected Previous/Next buttons not found")
        
        # Since the functionality isn't implemented, we'll mark this as a failure
        self.fail("Tip navigation functionality not implemented")

    def test_view_archive(self):
        """Functionalities 6: Test viewing historical tips archive"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Archive').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'li'))
        )
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreaterEqual(len(tips), 3, "Expected at least 3 tips in archive")

    def test_search_tips(self):
        """Functionalities 7: Test searching tips"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Archive').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'query'))
        )
        
        search_input = self.driver.find_element(By.NAME, 'query')
        search_input.send_keys('water')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'li'))
        )
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreaterEqual(len(tips), 1, "Expected at least 1 matching tip")

    def test_submit_feedback(self):
        """Functionalities 8: Test submitting feedback"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Feedback').click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'tip_id').send_keys('1')
        self.driver.find_element(By.ID, 'rating').send_keys('5')
        self.driver.find_element(By.ID, 'comment').send_keys('Great tip!')
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Today\'s Health Tip")]'))
        )
        self.assertIn("Today's Health Tip", self.driver.page_source)

    def test_data_storage(self):
        """Functionalities 9: Test data storage and retrieval"""
        # This is partially tested in other test cases
        # We'll verify the tips file exists and has content
        try:
            with open('tips.txt', 'r') as f:
                content = f.read()
                self.assertGreater(len(content), 0, "Tips file should not be empty")
        except FileNotFoundError:
            self.fail("Tips data file not found")

    def test_logout(self):
        """Functionalities 10: Test logging out"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        WebDriverWait(self.driver, 5).until(
            EC.title_contains("Login")
        )
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
