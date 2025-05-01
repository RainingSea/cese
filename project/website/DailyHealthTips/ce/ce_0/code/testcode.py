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
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8570/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password):
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/main'))

    # Functionalities 1: User Login
    def test_login_functionality(self):
        """Test valid user login"""
        self.login("admin", "admin123")
        self.assertIn("Daily Health Tips", self.driver.title)
        self.assertTrue(self.driver.find_element(By.XPATH, "//h1[contains(text(), 'Welcome')]").is_displayed())

    # Functionalities 2: Navigate to Registration Page
    def test_navigate_to_registration(self):
        """Test navigation to registration page"""
        register_link = self.wait.until(EC.presence_of_element_located(
            (By.LINK_TEXT, 'Register here')))
        register_link.click()
        self.wait.until(EC.title_contains("Register"))
        self.assertIn("Register", self.driver.title)

    # Functionalities 3: User Registration
    def test_user_registration(self):
        """Test new user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains("Register"))
        
        # Generate unique username to avoid conflicts
        username = f"testuser{int(time.time())}"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys("testpass123")
        self.driver.find_element(By.NAME, 'email').send_keys(f"{username}@example.com")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

    # Functionalities 4: View Current Daily Health Tip
    def test_view_current_tip(self):
        """Test viewing current health tip"""
        self.login("admin", "admin123")
        tip_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[contains(., 'Drink at least') or contains(., '30-minute walk') or contains(., 'balanced breakfast')]")))
        self.assertTrue(tip_element.is_displayed())

    # Functionalities 5: Navigate to Previous or Next Tips
    def test_navigate_tips(self):
        """Test navigation between tips"""
        self.login("admin", "admin123")
        
        # Get initial tip
        initial_tip = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[contains(., 'Drink at least') or contains(., '30-minute walk') or contains(., 'balanced breakfast')]"))).text
        
        # Click next tip
        self.driver.find_element(By.LINK_TEXT, 'Next Tip').click()
        self.wait.until(EC.staleness_of(self.driver.find_element(By.XPATH, "//p")))
        next_tip = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[contains(., 'Drink at least') or contains(., '30-minute walk') or contains(., 'balanced breakfast')]"))).text
        self.assertNotEqual(initial_tip, next_tip)
        
        # Click previous tip
        self.driver.find_element(By.LINK_TEXT, 'Previous Tip').click()
        self.wait.until(EC.staleness_of(self.driver.find_element(By.XPATH, "//p")))
        prev_tip = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[contains(., 'Drink at least') or contains(., '30-minute walk') or contains(., 'balanced breakfast')]"))).text
        self.assertEqual(initial_tip, prev_tip)

    # Functionalities 6: View Historical Daily Health Tips Archive
    def test_view_archive(self):
        """Test viewing tips archive"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.wait.until(EC.title_contains("Tips Archive"))
        
        tips = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//ul/li")))
        self.assertGreater(len(tips), 0, "No tips found in archive")

    # Functionalities 7: Search for Specific Tips from the Tips Archive
    def test_search_tips(self):
        """Test searching tips in archive"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.wait.until(EC.title_contains("Tips Archive"))
        
        search_input = self.driver.find_element(By.NAME, 'search')
        search_input.send_keys("hydration")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        tips = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//ul/li[contains(., 'hydration')]")))
        self.assertGreater(len(tips), 0, "No matching tips found")

    # Functionalities 8: Submit Feedback on Daily Health Tips
    def test_submit_feedback(self):
        """Test submitting feedback"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        self.wait.until(EC.title_contains("Submit Feedback"))
        
        feedback_text = "This is a test feedback message"
        self.driver.find_element(By.NAME, 'feedback').send_keys(feedback_text)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        
        self.wait.until(EC.url_contains('/main'))
        self.assertIn("Daily Health Tips", self.driver.title)

    # Functionalities 9: Data Storage and Retrieval
    def test_data_storage(self):
        """Test data storage and retrieval"""
        self.login("admin", "admin123")
        
        # Check if current tip is displayed (retrieved from storage)
        tip_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//p[contains(., 'Drink at least') or contains(., '30-minute walk') or contains(., 'balanced breakfast')]")))
        self.assertTrue(tip_element.is_displayed())
        
        # Check archive data
        self.driver.find_element(By.LINK_TEXT, 'View Archive').click()
        self.wait.until(EC.title_contains("Tips Archive"))
        tips = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//ul/li")))
        self.assertGreater(len(tips), 0, "No tips found in archive")

    # Functionalities 10: Application State Management
    def test_logout(self):
        """Test logout functionality"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)
        
        # Try to access main page without login
        self.driver.get('http://localhost:8570/main')
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
