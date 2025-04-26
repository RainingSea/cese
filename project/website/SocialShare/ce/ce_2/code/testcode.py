import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the correct port if necessary

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
        self.driver.get('http://localhost:5000/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:5000/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:5000/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Feed", self.driver.title)  # Assuming the title of the feed page is "Feed"

        # Invalid login
        self.driver.get('http://localhost:5000/')  # Navigate back to Login Page
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:5000/profile')  # Navigate to Profile Page
        self.assertIn("Profile", self.driver.title)

        # Update profile
        self.driver.find_element(By.NAME, 'bio').send_keys("This is my bio.")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to save with empty bio
        self.driver.find_element(By.NAME, 'bio').clear()  # Clear the bio field
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_feed_content(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:5000/feed')  # Navigate to Feed Page
        self.assertIn("Feed", self.driver.title)

        # Check if articles are displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(articles), 0, "No articles found in the feed.")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:5000/')  # Navigate to Login Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
