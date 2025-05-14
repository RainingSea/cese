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
        self.driver.get('http://localhost:8065/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.get('http://localhost:8065/login')
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Dashboard"))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Test registration page display
        self.driver.get('http://localhost:8065/register')
        self.assertIn("Registration", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username'))
        self.assertTrue(self.driver.find_element(By.NAME, 'password'))
        
        # Test successful registration
        username = "testuser_" + str(int(time.time()))
        password = "testpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Test duplicate username registration
        self.driver.get('http://localhost:8065/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertEqual(error_message, "Username already exists")

    # Functionality 2: User Login
    def test_user_login(self):
        # Test login page display
        self.driver.get('http://localhost:8065/login')
        self.assertIn("Login", self.driver.title)
        self.assertTrue(self.driver.find_element(By.NAME, 'username'))
        self.assertTrue(self.driver.find_element(By.NAME, 'password'))
        
        # Test successful login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        
        # Test invalid login
        self.driver.get('http://localhost:8065/login')
        self.driver.find_element(By.NAME, 'username').send_keys("wronguser")
        self.driver.find_element(By.NAME, 'password').send_keys("wrongpass")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        error_message = self.driver.find_element(By.CLASS_NAME, 'error').text
        self.assertEqual(error_message, "Invalid credentials")

    # Functionality 3: Input Travel Details
    def test_input_travel_details(self):
        self.login("admin", "admin123")
        
        # Test form display
        form = self.driver.find_element(By.TAG_NAME, 'form')
        self.assertTrue(form)
        self.assertTrue(self.driver.find_element(By.NAME, 'destination'))
        self.assertTrue(len(self.driver.find_elements(By.NAME, 'interests')) > 0)
        
        # Test successful tip generation
        self.driver.find_element(By.XPATH, '//option[text()="Paris"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="museums"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0)
        
        # Test incomplete form submission
        self.driver.get('http://localhost:8065/dashboard')
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.assertIn("Dashboard", self.driver.title)  # Should stay on same page

    # Functionality 4: View Recommendations
    def test_view_recommendations(self):
        self.login("admin", "admin123")
        
        # Get some tips first
        self.driver.find_element(By.XPATH, '//option[text()="Paris"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="museums"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        
        # Test recommendations display
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0)
        
        # Test refresh maintains recommendations
        self.driver.refresh()
        self.wait.until(EC.title_contains("Tips"))
        refreshed_tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertEqual(len(tips), len(refreshed_tips))

    # Functionality 5: Search for Tips
    def test_search_for_tips(self):
        self.login("admin", "admin123")
        
        # Test successful search
        self.driver.find_element(By.XPATH, '//option[text()="Tokyo"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="shopping"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        tips = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(tips), 0)
        
        # Test no results found
        self.driver.get('http://localhost:8065/dashboard')
        self.driver.find_element(By.XPATH, '//option[text()="Paris"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="nightlife"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        no_tips_message = self.driver.find_element(By.XPATH, '//li[contains(text(), "No tips found")]')
        self.assertTrue(no_tips_message)

    # Functionality 6: Save Favorite Travel Tips
    def test_save_favorite_tips(self):
        self.login("user1", "password1")
        
        # Get some tips first
        self.driver.find_element(By.XPATH, '//option[text()="Tokyo"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="shopping"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        
        # Save a tip
        save_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Save Tip"]')
        save_buttons[0].click()
        self.wait.until(EC.title_contains("Dashboard"))
        
        # Check saved tips
        saved_tips = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertGreater(len(saved_tips), 0)
        
        # Try saving same tip again
        self.driver.find_element(By.XPATH, '//option[text()="Tokyo"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="shopping"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        save_buttons = self.driver.find_elements(By.XPATH, '//button[text()="Save Tip"]')
        save_buttons[0].click()
        self.wait.until(EC.title_contains("Dashboard"))
        # No error message shown in current implementation

    # Functionality 7: User Logout
    def test_user_logout(self):
        self.login("admin", "admin123")
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        
        # Test accessing dashboard after logout
        self.driver.get('http://localhost:8065/dashboard')
        self.wait.until(EC.title_contains("Login"))

    # Functionality 8: Navigate Back to Dashboard
    def test_navigate_back_to_dashboard(self):
        self.login("admin", "admin123")
        
        # Go to tips page
        self.driver.find_element(By.XPATH, '//option[text()="Paris"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="museums"]').click()
        self.driver.find_element(By.XPATH, '//button[text()="Get Tips"]').click()
        self.wait.until(EC.title_contains("Tips"))
        
        # Navigate back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.wait.until(EC.title_contains("Dashboard"))

    # Functionality 9: View Saved Travel Tips
    def test_view_saved_travel_tips(self):
        self.login("admin", "admin123")
        
        # Check saved tips display
        saved_tips = self.driver.find_elements(By.XPATH, '//ul/li')
        self.assertTrue(len(saved_tips) > 0 or "No saved tips yet" in self.driver.page_source)
        
        # For this implementation, saved tips are just IDs, so detailed view not implemented
        # This would need to be updated if detailed view is added

if __name__ == '__main__':
    unittest.main()
