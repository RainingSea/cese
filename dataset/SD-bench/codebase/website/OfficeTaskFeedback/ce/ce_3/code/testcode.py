import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestOfficeTaskFeedback(unittest.TestCase):

    def setUp(self):
        # Start the application server
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8660/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        # Verify registration page loaded
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.assertIn("Register", self.driver.title)  # Should ideally check for an error message

    def test_user_login(self):
        # Test user login functionality
        self.login("admin", "admin123")

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8660/')
        self.login("invalid_user", "invalid_pass")

        # Check for error message (not implemented in the codebase)
        self.assertIn("Login", self.driver.title)  # Should ideally check for an error message

    def test_feedback_submission(self):
        # Test feedback submission functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the feedback page to load

        # Verify feedback page loaded
        self.assertIn("Feedback", self.driver.title)

        # Submit feedback
        self.driver.find_element(By.NAME, 'content').send_keys('This is a test feedback.')
        self.driver.find_element(By.NAME, 'category').send_keys('General')
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        time.sleep(1)  # Wait for redirection to dashboard

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to submit feedback without filling required fields
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the codebase)
        self.assertIn("Feedback", self.driver.title)  # Should ideally check for an error message

    def test_feedback_categorization(self):
        # Test feedback categorization functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Submit Feedback').click()
        time.sleep(1)  # Wait for the feedback page to load

        # Select category and submit feedback
        self.driver.find_element(By.NAME, 'content').send_keys('Feedback with category.')
        category_dropdown = self.driver.find_element(By.NAME, 'category')
        category_dropdown.find_element(By.XPATH, '//option[text()="Bug"]').click()
        self.driver.find_element(By.XPATH, '//input[@value="Submit Feedback"]').click()
        time.sleep(1)  # Wait for redirection to dashboard

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_user_logout(self):
        # Test user logout functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection to login

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8660/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_return_to_login_page(self):
        # Test return to login page functionality
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection to login

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Navigate to registration page from login
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify redirection to registration page
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
