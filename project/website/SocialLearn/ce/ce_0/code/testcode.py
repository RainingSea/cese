import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestSocialLearnApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8414/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8414/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        interests = "test_interests"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'interests').send_keys(interests)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8414/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.NAME, 'interests').send_keys("math")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Profile", self.driver.title)  # Check if redirected to Profile Page

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8414/')
        self.login("admin", "wrong_password")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)  # Check for error message

    def test_profile_management(self):
        # Functionality 3: User Profile Management
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8414/profile')  # Navigate to Profile Page

        # Check if current profile information is displayed
        self.assertIn("Profile of admin", self.driver.page_source)

        # Update profile
        new_interests = "updated_interests"
        self.driver.find_element(By.NAME, 'interests').clear()
        self.driver.find_element(By.NAME, 'interests').send_keys(new_interests)
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()

        # Verify profile update
        self.assertIn("Profile updated successfully", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click Logout
        self.assertIn("Login", self.driver.title)  # Check if redirected to Login Page

        # Attempt to navigate back to Profile Page
        self.driver.get('http://localhost:8414/profile')
        self.assertIn("Login", self.driver.title)  # Access denied, should be redirected to Login Page

if __name__ == '__main__':
    unittest.main()
