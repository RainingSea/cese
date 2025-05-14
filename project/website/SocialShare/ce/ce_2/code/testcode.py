import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8103/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.url_contains('/feed'))

    def test_user_registration(self):
        """Test Functionality 1: User Registration"""
        # Navigate to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Test fields exist
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        self.assertTrue(username_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        
        # Test successful registration
        username_field.send_keys('newuser')
        password_field.send_keys('newpass123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.wait.until(EC.url_contains('/profile'))
        
        # Test duplicate username
        self.driver.get('http://localhost:8103/register')
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        username_field.send_keys('admin')  # existing username
        password_field.send_keys('password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertTrue('Username already exists' in self.driver.page_source)

    def test_user_login(self):
        """Test Functionality 2: User Login"""
        # Test login page elements
        username_field = self.driver.find_element(By.ID, 'username')
        password_field = self.driver.find_element(By.ID, 'password')
        self.assertTrue(username_field.is_displayed())
        self.assertTrue(password_field.is_displayed())
        
        # Test successful login
        self.login('user1', 'password1')
        self.assertTrue('Feed' in self.driver.page_source)
        
        # Test invalid login
        self.driver.get('http://localhost:8103/login')
        self.driver.find_element(By.ID, 'username').send_keys('wronguser')
        self.driver.find_element(By.ID, 'password').send_keys('wrongpass')
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.assertTrue('Invalid username or password' in self.driver.page_source)

    def test_profile_creation_update(self):
        """Test Functionality 3: Profile Creation and Update"""
        self.login('user1', 'password1')
        
        # Navigate to profile page
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.wait.until(EC.url_contains('/profile'))
        
        # Test profile page elements
        bio_field = self.driver.find_element(By.NAME, 'bio')
        self.assertTrue(bio_field.is_displayed())
        
        # Test updating profile
        new_bio = "Updated bio for testing"
        bio_field.clear()
        bio_field.send_keys(new_bio)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.wait.until(EC.text_to_be_present_in_element_value((By.NAME, 'bio'), new_bio))
        
        # Test empty bio (should be allowed according to code)
        bio_field = self.driver.find_element(By.NAME, 'bio')
        bio_field.clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.wait.until(EC.text_to_be_present_in_element_value((By.NAME, 'bio'), ''))

    def test_content_upload_sharing(self):
        """Test Functionality 4: Content Upload and Sharing"""
        self.login('user1', 'password1')
        
        # Navigate to create post page
        self.driver.find_element(By.LINK_TEXT, 'Create Post').click()
        self.wait.until(EC.url_contains('/create_post'))
        
        # Test create post form
        content_field = self.driver.find_element(By.NAME, 'content')
        self.assertTrue(content_field.is_displayed())
        
        # Test successful post creation
        test_content = "This is a test post"
        content_field.send_keys(test_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        self.wait.until(EC.url_contains('/feed'))
        self.assertTrue(test_content in self.driver.page_source)
        
        # Test empty content (should be prevented by required attribute)
        self.driver.find_element(By.LINK_TEXT, 'Create Post').click()
        self.wait.until(EC.url_contains('/create_post'))
        content_field = self.driver.find_element(By.NAME, 'content')
        content_field.clear()
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        self.assertTrue('required' in content_field.get_attribute('outerHTML'))

    def test_content_discovery(self):
        """Test Functionality 5: Content Discovery"""
        self.login('user1', 'password1')
        
        # Test feed displays posts
        posts = self.driver.find_elements(By.CLASS_NAME, 'card')
        self.assertGreater(len(posts), 0, "No posts found in feed")
        
        # Test post details are displayed
        first_post = posts[0]
        self.assertTrue(first_post.find_element(By.CLASS_NAME, 'card-title').is_displayed())
        self.assertTrue(first_post.find_element(By.CLASS_NAME, 'card-text').is_displayed())
        self.assertTrue(first_post.find_element(By.CLASS_NAME, 'text-muted').is_displayed())

    def test_interacting_with_content(self):
        """Test Functionality 6: Interacting with Content"""
        self.login('user1', 'password1')
        
        # Test like and comment buttons exist
        first_post = self.driver.find_elements(By.CLASS_NAME, 'card')[0]
        like_btn = first_post.find_element(By.XPATH, './/button[contains(text(), "Like")]')
        comment_btn = first_post.find_element(By.XPATH, './/button[contains(text(), "Comment")]')
        self.assertTrue(like_btn.is_displayed())
        self.assertTrue(comment_btn.is_displayed())
        
        # Note: Actual interaction functionality not implemented in UI
        # According to codebase, interactions are recorded in interactions.txt
        # but UI doesn't reflect this, so we can only verify buttons exist

    def test_user_logout(self):
        """Test Functionality 7: User Logout"""
        self.login('user1', 'password1')
        
        # Test logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.wait.until(EC.url_contains('/login'))
        
        # Test accessing protected page after logout
        self.driver.get('http://localhost:8103/feed')
        self.wait.until(EC.url_contains('/login'))

    def test_user_interaction(self):
        """Test Functionality 8: User Interaction (Follow and Message)"""
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented in codebase")

if __name__ == '__main__':
    unittest.main()
