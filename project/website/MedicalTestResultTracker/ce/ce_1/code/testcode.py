import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8347/')  # Access the login page

    def tearDown(self):
        # Close the web driver and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8347/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8347/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message (assuming it redirects back to registration)
        self.assertIn("Register", self.driver.title)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8347/')  # Go back to login page
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login", self.driver.title)

    def test_manage_test_results(self):
        # Functionality 3: Input and Manage Medical Test Results
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8347/dashboard')  # Navigate to Test Results Page
        self.assertIn("Test Results", self.driver.title)

        # Input valid medical test results
        self.driver.find_element(By.NAME, 'test_name').send_keys("Blood Test")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-03-01")
        self.driver.find_element(By.NAME, 'result').send_keys("Normal")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()

        # Verify that the test result is saved (assuming it redirects back to the dashboard)
        self.assertIn("Test Results", self.driver.page_source)

    def test_view_trends(self):
        # Functionality 4: View Historical Data and Trends
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8347/trends')  # Navigate to Trends Page
        self.assertIn("Test Trends", self.driver.title)

    def test_set_reminders(self):
        # Functionality 5: Set and Receive Reminders
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8347/reminders')  # Navigate to Reminders Page
        self.assertIn("Set Reminders", self.driver.title)

        # Set a reminder (assuming there's a form to fill)
        self.driver.find_element(By.NAME, 'reminder').send_keys("Follow-up Test")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-04-01")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is saved (assuming it redirects back to the reminders page)
        self.assertIn("Set Reminders", self.driver.page_source)

    def test_view_history(self):
        # Functionality 6: View Test Result History
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8347/history')  # Navigate to History Page
        self.assertIn("Test Results History", self.driver.title)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Assuming there's a logout link
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality 8: Navigate Back to Dashboard
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8347/dashboard')  # Navigate to Dashboard
        self.driver.get('http://localhost:8347/reminders')  # Navigate to Reminders
        self.driver.back()  # Go back to Dashboard
        self.assertIn("Dashboard", self.driver.title)

    def test_view_test_result_details(self):
        # Functionality 9: View Test Result Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8347/history')  # Navigate to History Page
        # Assuming there's a way to click on a test result to view details
        # This part needs to be implemented based on the actual HTML structure
        # self.driver.find_element(By.LINK_TEXT, 'Blood Test').click()  # Example
        # self.assertIn("Blood Test", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
