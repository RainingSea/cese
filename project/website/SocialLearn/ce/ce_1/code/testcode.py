import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8415/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8415/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8415/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message (assuming it redirects back to register)
        self.assertIn("Register", self.driver.title)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Profile", self.driver.title)  # Check if redirected to Profile Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8415/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login", self.driver.title)  # Check for error message

    def test_profile_management(self):
        # Functionality 3: User Profile Management
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8415/profile')  # Navigate to Profile Page
        self.assertIn("Profile", self.driver.title)  # Check if Profile Page is displayed

        # Update profile with new interests
        self.driver.find_element(By.NAME, 'interests').send_keys("Physics, Chemistry")
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify profile update success (assuming it redirects back to profile)
        self.assertIn("Profile", self.driver.title)

    def test_resources_management(self):
        # Functionality 5: Share and Access Educational Resources
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8415/resources')  # Navigate to Resources Page
        self.assertIn("Shared Resources", self.driver.title)  # Check if Resources Page is displayed

        # Share a new resource
        self.driver.find_element(By.NAME, 'resource').send_keys("New Resource")
        self.driver.find_element(By.XPATH, '//button[text()="Share Resource"]').click()

        # Verify resource is shared (assuming it redirects back to resources)
        self.assertIn("Shared Resources", self.driver.title)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click Logout
        self.assertIn("Login", self.driver.title)  # Verify redirection to Login Page

if __name__ == '__main__':
    unittest.main()
