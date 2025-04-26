import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8246/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8246/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8246/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("User already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Discovery", self.driver.title)  # Check if redirected to Discovery Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8246/')
        self.driver.find_element(By.NAME, 'username').send_keys("invalid_user")
        self.driver.find_element(By.NAME, 'password').send_keys("wrong_password")
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8246/profile')  # Navigate to Profile Page
        self.assertIn("Profile", self.driver.title)

        # Update bio
        self.driver.find_element(By.NAME, 'bio').send_keys("This is my bio.")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify profile update success
        self.assertIn("Profile", self.driver.title)

        # Attempt to save with empty bio
        self.driver.find_element(By.NAME, 'bio').clear()  # Clear the bio field
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for empty bio
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_share(self):
        # Functionality 4: Content Upload and Sharing
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8246/content_share')  # Navigate to Content Share Page
        self.assertIn("Share Content", self.driver.title)

        # Share a valid article
        self.driver.find_element(By.NAME, 'title').send_keys("My First Article")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of my first article.")
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify article share success
        self.assertIn("Discovery", self.driver.title)

        # Attempt to share an article with empty title
        self.driver.get('http://localhost:8246/content_share')
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content without a title.")
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for empty title
        self.assertIn("Title cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8246/discovery')  # Navigate to Discovery Page
        self.assertIn("Discovery", self.driver.title)

        # Verify that shared content is displayed
        self.assertIn("My First Article", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
