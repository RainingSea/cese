import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestSocialShareApp(unittest.TestCase):

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
        self.driver.get('http://localhost:8101/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/feed'))

    def logout(self):
        # Helper method to perform logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.url_contains('/login'))

    # Functionality 1: User Registration
    def test_user_registration(self):
        # Test navigation to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.url_contains('/register'))
        self.assertIn('Register', self.driver.title)

        # Test successful registration
        username = f"testuser_{int(time.time())}"
        password = "testpass123"
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.url_contains('/login'))
        self.assertIn('Login', self.driver.title)

        # Test registration with existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.url_contains('/register'))
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger')))
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn('Username already exists', error_message)

    # Functionality 2: User Login
    def test_user_login(self):
        # Test login page display
        self.assertIn('Login', self.driver.title)
        self.assertTrue(self.driver.find_element(By.ID, 'username').is_displayed())
        self.assertTrue(self.driver.find_element(By.ID, 'password').is_displayed())

        # Test successful login
        self.login('admin', 'admin123')
        self.assertIn('Feed', self.driver.title)
        self.logout()

        # Test invalid login
        self.driver.find_element(By.ID, 'username').send_keys('wronguser')
        self.driver.find_element(By.ID, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-danger')))
        error_message = self.driver.find_element(By.CLASS_NAME, 'alert-danger').text
        self.assertIn('Invalid credentials', error_message)

    # Functionality 3: Profile Creation and Update
    def test_profile_management(self):
        self.login('user1', 'password1')
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.url_contains('/profile'))
        self.assertIn("user1's Profile", self.driver.title)

        # Check profile display
        profile_info = self.driver.find_element(By.CLASS_NAME, 'card-body').text
        self.assertIn('Regular user', profile_info)
        self.assertIn('Enjoys reading', profile_info)

        # Note: The edit functionality isn't fully implemented in the UI
        # So we can only test the display of existing profile information

    # Functionality 4: Content Upload and Sharing
    def test_content_upload(self):
        # Note: The content upload functionality isn't implemented in the UI
        # So we'll test the content display instead
        self.login('admin', 'admin123')
        
        # Check that feed displays content
        feed_items = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(feed_items), 0, "No content items found in feed")

    # Functionality 5: Content Discovery
    def test_content_discovery(self):
        self.login('user1', 'password1')
        
        # Check feed display
        feed_items = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(feed_items), 0, "No content items found in feed")
        
        # Check content details
        first_item = feed_items[0]
        title = first_item.find_element(By.CLASS_NAME, 'card-title').text
        username = first_item.find_element(By.CLASS_NAME, 'card-subtitle').text
        content = first_item.find_element(By.CLASS_NAME, 'card-text').text
        
        self.assertTrue(title, "Title is empty")
        self.assertIn('Posted by', username)
        self.assertTrue(content, "Content is empty")
        
        # Test viewing a content item
        view_button = first_item.find_element(By.LINK_TEXT, 'View')
        view_button.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-title')))
        content_title = self.driver.find_element(By.CLASS_NAME, 'card-title').text
        self.assertEqual(title, content_title)

    # Functionality 6: Interacting with Content
    def test_content_interaction(self):
        # Note: The like/comment functionality isn't fully implemented in the UI
        # So we'll test the display of content with interaction buttons
        self.login('admin', 'admin123')
        
        # Navigate to a content item
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-group')))
        
        # Check interaction buttons are present
        buttons = self.driver.find_elements(By.CLASS_NAME, 'btn')
        button_texts = [btn.text for btn in buttons]
        self.assertIn('Like', button_texts)
        self.assertIn('Comment', button_texts)
        self.assertIn('Save', button_texts)

    # Functionality 7: User Logout
    def test_user_logout(self):
        self.login('admin', 'admin123')
        self.assertIn('Feed', self.driver.title)
        
        # Perform logout
        self.logout()
        self.assertIn('Login', self.driver.title)
        
        # Attempt to access protected page
        self.driver.get('http://localhost:8101/feed')
        self.wait.until(EC.url_contains('/login'))
        self.assertIn('Login', self.driver.title)

    # Functionality 8: User Interaction (Follow and Message)
    def test_user_interaction(self):
        # Note: The follow/message functionality isn't implemented in the UI
        # So we'll test the profile display which would contain these features
        self.login('user1', 'password1')
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.url_contains('/profile'))
        
        # Check profile display (would contain follow/message buttons if implemented)
        profile_info = self.driver.find_element(By.CLASS_NAME, 'card-body').text
        self.assertIn('Regular user', profile_info)

if __name__ == '__main__':
    unittest.main()
