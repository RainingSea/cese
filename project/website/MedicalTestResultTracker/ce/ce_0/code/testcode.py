import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8346/')  # Accessing the login page

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
        self.driver.get('http://localhost:8346/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8346/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8346/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_dashboard(self):
        # Functionality 3: Input and Manage Medical Test Results
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Check if test results can be added (this part is not implemented in the codebase)
        self.fail("Test result management functionality not implemented")

    def test_view_trends(self):
        # Functionality 4: View Historical Data and Trends
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Trends Page
        self.assertIn("Dashboard", self.driver.title)

        # Check if trends can be viewed (this part is not implemented in the codebase)
        self.fail("Trends viewing functionality not implemented")

    def test_set_reminders(self):
        # Functionality 5: Set and Receive Reminders
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Reminders Page
        self.assertIn("Dashboard", self.driver.title)

        # Check if reminders can be set (this part is not implemented in the codebase)
        self.fail("Reminder setting functionality not implemented")

    def test_view_test_result_history(self):
        # Functionality 6: View Test Result History
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Test Result History Page
        self.assertIn("Dashboard", self.driver.title)

        # Check if test result history can be viewed (this part is not implemented in the codebase)
        self.fail("Test result history viewing functionality not implemented")

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click the logout button
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Test Results Page
        self.driver.back()  # Click the back button
        self.assertIn("Dashboard", self.driver.title)

    def test_view_test_result_details(self):
        # Functionality 9: View Test Result Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8346/dashboard')  # Navigate to Test Results Page
        self.assertIn("Dashboard", self.driver.title)

        # Check if test result details can be viewed (this part is not implemented in the codebase)
        self.fail("Test result details viewing functionality not implemented")

if __name__ == '__main__':
    unittest.main()
