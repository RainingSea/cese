import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8419/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8419/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8419/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8419/')  # Navigate to login page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Feed", self.driver.title)  # Check if redirected to feed page

        # Invalid login
        self.driver.get('http://localhost:8419/')  # Navigate to login page again
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")  # Log in
        self.driver.get('http://localhost:8419/profile')  # Navigate to profile page
        self.assertIn("User Profile", self.driver.title)

        # Attempt to update profile with empty bio
        self.driver.find_element(By.NAME, 'bio').send_keys("")  # Assuming there's a bio field
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        self.assertIn("Bio cannot be empty", self.driver.page_source)

        # Update profile with valid bio
        self.driver.find_element(By.NAME, 'bio').send_keys("This is my bio.")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        self.assertIn("Profile updated successfully", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        # Functionality 4: Content Upload and Sharing
        self.login("admin", "admin123")  # Log in
        self.driver.get('http://localhost:8419/upload')  # Navigate to upload page
        self.assertIn("Upload Article", self.driver.title)

        # Upload a valid article
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Upload"]').click()
        self.assertIn("Feed", self.driver.title)  # Check if redirected to feed page

        # Verify the article is in the feed
        self.assertIn("This is a new article.", self.driver.page_source)

        # Attempt to upload an article with empty content
        self.driver.get('http://localhost:8419/upload')  # Navigate to upload page again
        self.driver.find_element(By.NAME, 'content').send_keys("")  # Empty content
        self.driver.find_element(By.XPATH, '//button[text()="Upload"]').click()
        self.assertIn("Content cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")  # Log in
        self.driver.get('http://localhost:8419/feed')  # Navigate to feed page
        self.assertIn("Feed", self.driver.title)

        # Verify articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found in the feed.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to login page

if __name__ == '__main__':
    unittest.main()
