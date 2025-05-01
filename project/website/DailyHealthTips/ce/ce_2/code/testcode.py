import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestDailyHealthTipsApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8572/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session and stop the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains('Dashboard'))

    def test_login(self):
        """Functionalities 1: Test user login functionality"""
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        """Functionalities 2: Test navigation to the Registration Page"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        """Functionalities 3: Test user registration functionality"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))

        # Input registration details
        self.driver.find_element(By.ID, 'username').send_keys("testuser")
        self.driver.find_element(By.ID, 'password').send_keys("testpass123")
        self.driver.find_element(By.ID, 'email').send_keys("test@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains('Login'))
        self.assertIn("Login", self.driver.title)

    def test_view_current_tip(self):
        """Functionalities 4: Test viewing current daily health tip"""
        self.login("admin", "admin123")
        tip_element = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        self.assertTrue(tip_element.text.strip())

    def test_navigate_tips(self):
        """Functionalities 5: Test navigating between tips"""
        self.login("admin", "admin123")
        
        # Get initial tip
        initial_tip = self.driver.find_element(By.TAG_NAME, 'h2').text
        
        # Click next tip
        self.driver.find_element(By.LINK_TEXT, 'Next Tip').click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        next_tip = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertNotEqual(initial_tip, next_tip)
        
        # Click previous tip
        self.driver.find_element(By.LINK_TEXT, 'Previous Tip').click()
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        prev_tip = self.driver.find_element(By.TAG_NAME, 'h2').text
        self.assertEqual(initial_tip, prev_tip)

    def test_view_archive(self):
        """Functionalities 6: Test viewing historical tips archive"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Archive').click()
        self.wait.until(EC.title_contains('Archive'))
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0)

    def test_search_tips(self):
        """Functionalities 7: Test searching tips from archive"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Archive').click()
        self.wait.until(EC.title_contains('Archive'))
        
        # Search for "water" which should match the hydration tip
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys('water')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'li')))
        results = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(results), 0)

    def test_submit_feedback(self):
        """Functionalities 8: Test submitting feedback"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Feedback').click()
        self.wait.until(EC.title_contains('Feedback'))
        
        # Submit feedback
        feedback_text = "This is a test feedback message"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Feedback"]').click()
        
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn("Dashboard", self.driver.title)

    def test_data_storage(self):
        """Functionalities 9: Test data storage and retrieval"""
        # This would typically require checking the files directly
        # For this test, we'll verify that tips are loaded from storage
        self.login("admin", "admin123")
        tips = self.driver.find_elements(By.XPATH, '//main//h2')
        self.assertGreater(len(tips), 0)

    def test_logout(self):
        """Functionalities 10: Test logging out"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains('Login'))
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
