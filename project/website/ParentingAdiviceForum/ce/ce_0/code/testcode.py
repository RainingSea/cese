import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

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
        self.driver.get('http://localhost:8121/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/'))

    def test_1_user_login(self):
        """Test user login functionality"""
        self.login("admin", "admin123")
        
        # Verify that the Home Page has loaded
        self.assertIn("Welcome", self.driver.page_source)
        self.assertIn("admin", self.driver.page_source)

    def test_2_navigate_to_registration_page(self):
        """Test navigation to the Registration Page"""
        register_link = self.wait.until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Register here'))
        )
        register_link.click()
        
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_3_user_registration(self):
        """Test user registration functionality"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        # Generate unique username
        test_username = f"testuser{int(time.time())}"
        test_password = "testpass123"
        
        # Fill out registration form
        self.driver.find_element(By.ID, 'username').send_keys(test_username)
        self.driver.find_element(By.ID, 'password').send_keys(test_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirect to login page
        self.assertIn("Login", self.driver.title)
        
        # Verify new user can login
        self.login(test_username, test_password)
        self.assertIn("Welcome", self.driver.page_source)

    def test_4_view_home_page_after_login(self):
        """Test viewing home page after login and navigation options"""
        self.login("admin", "admin123")
        
        # Verify navigation links are present
        nav_links = ['Home', 'Forum', 'Advice', 'My Account', 'Contact Us', 'Logout']
        for link in nav_links:
            self.assertTrue(self.driver.find_element(By.LINK_TEXT, link).is_displayed())

    def test_5_navigate_to_forum_page(self):
        """Test navigation to the Forum Page"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        # Verify forum page loaded
        self.assertIn("Forum", self.driver.title)
        self.assertIn("New Thread", self.driver.page_source)

    def test_6_create_new_thread(self):
        """Test creating a new thread"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        # Click new thread link
        self.driver.find_element(By.XPATH, '//a[contains(text(), "New Thread")]').click()
        
        # Fill out thread form
        thread_title = f"Test Thread {int(time.time())}"
        thread_content = "This is a test thread created by automated tests."
        
        self.wait.until(EC.visibility_of_element_located((By.ID, 'title'))).send_keys(thread_title)
        self.driver.find_element(By.ID, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Thread"]').click()
        
        # Verify thread appears in forum
        self.assertIn(thread_title, self.driver.page_source)

    def test_7_view_specific_thread(self):
        """Test viewing a specific thread"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        # Click on first thread
        first_thread = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.thread a'))
        )
        thread_title = first_thread.text
        first_thread.click()
        
        # Verify thread details page
        self.assertIn(thread_title, self.driver.title)
        self.assertIn("Posted by", self.driver.page_source)

    def test_8_comment_on_thread(self):
        """Test commenting on a thread"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        # Click on first thread
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.thread a'))
        ).click()
        
        # Add comment
        comment_text = f"Test comment {int(time.time())}"
        self.driver.find_element(By.ID, 'comment').send_keys(comment_text)
        self.driver.find_element(By.XPATH, '//button[text()="Post Comment"]').click()
        
        # Verify comment appears
        self.assertIn(comment_text, self.driver.page_source)
        self.assertIn("admin", self.driver.page_source)

    def test_9_post_advice(self):
        """Test posting advice"""
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Advice').click()
        
        # Fill out advice form
        advice_title = f"Test Advice {int(time.time())}"
        advice_content = "This is test advice content created by automated tests."
        
        self.driver.find_element(By.ID, 'title').send_keys(advice_title)
        self.driver.find_element(By.ID, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        
        # Verify advice appears
        self.assertIn(advice_title, self.driver.page_source)
        self.assertIn(advice_content, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
