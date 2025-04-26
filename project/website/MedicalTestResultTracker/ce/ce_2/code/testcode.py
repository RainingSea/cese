import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8184/')  # Access the login page

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
        self.driver.get('http://localhost:8184/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8184/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8184/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_dashboard(self):
        # Functionality 3: Input and Manage Medical Test Results
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Check if test results and reminders are displayed
        self.assertIn("Your Test Results", self.driver.page_source)
        self.assertIn("Your Reminders", self.driver.page_source)

    def test_set_reminder(self):
        # Functionality 5: Set and Receive Reminders
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8184/dashboard')  # Navigate to Dashboard

        # Set a new reminder
        self.driver.find_element(By.LINK_TEXT, 'Set Reminder').click()
        self.driver.find_element(By.NAME, 'reminder').send_keys("Follow up in 6 months")
        self.driver.find_element(By.XPATH, '//button[text()="Save Reminder"]').click()

        # Verify the reminder is saved
        self.assertIn("Follow up in 6 months", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8184/dashboard')  # Navigate to Dashboard
        self.driver.find_element(By.LINK_TEXT, 'View Test Results').click()  # Navigate to Test Results
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()  # Click back
        self.assertIn("Dashboard", self.driver.title)

    def test_view_test_result_details(self):
        # Functionality 9: View Test Result Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8184/dashboard')  # Navigate to Dashboard
        self.driver.find_element(By.LINK_TEXT, 'View Test Results').click()  # Navigate to Test Results
        self.assertIn("Test Results", self.driver.title)

        # Click on a specific test result
        self.driver.find_element(By.LINK_TEXT, 'Blood Test: Normal').click()
        self.assertIn("Blood Test: Normal", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
