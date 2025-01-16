import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8538/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'password').send_keys("user123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("user1", "user123")

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.page_source)

        # Enter invalid credentials
        self.driver.get('http://localhost:8538/login')
        self.login("user1", "wrongpassword")

        # Verify error message for invalid credentials
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_input_and_manage_medical_test_results(self):
        # Log in and navigate to Test Results Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Add Test Result').click()
        time.sleep(1)

        # Verify Test Results Page is displayed
        self.assertIn("Add Test Result", self.driver.title)

        # Input valid test results
        self.driver.find_element(By.NAME, 'test_name').send_keys("New Test")
        self.driver.find_element(By.NAME, 'result').send_keys("99.9")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-04")
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)

        # Verify successful addition of test results
        self.assertIn("Test Results History", self.driver.page_source)

    def test_view_historical_data_and_trends(self):
        # Log in and navigate to Trends Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Trends').click()
        time.sleep(1)

        # Verify Trends Page is displayed
        self.assertIn("Test Results Trend", self.driver.page_source)

    def test_set_and_receive_reminders(self):
        # Log in and navigate to Reminders Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()
        time.sleep(1)

        # Verify Reminders Page is displayed
        self.assertIn("Your Reminders", self.driver.page_source)

        # Set a new reminder
        self.driver.find_element(By.NAME, 'reminder').send_keys("Doctor Appointment")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-05")
        self.driver.find_element(By.XPATH, '//button[text()="Add Reminder"]').click()
        time.sleep(1)

        # Verify reminder is saved
        self.assertIn("Doctor Appointment", self.driver.page_source)

    def test_view_test_result_history(self):
        # Log in and navigate to Test Result History Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Test Results').click()
        time.sleep(1)

        # Verify Test Result History Page is displayed
        self.assertIn("Test Results History", self.driver.page_source)

        # Click on a specific test result to view details
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Verify test result details are displayed
        self.assertIn("Test Result Details", self.driver.page_source)

    def test_user_logout(self):
        # Log in and navigate to Dashboard
        self.login("user1", "user123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Log in and navigate to Test Results Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Test Results').click()
        time.sleep(1)

        # Click back to Dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.page_source)

    def test_view_test_result_details(self):
        # Log in and navigate to Test Results Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Test Results').click()
        time.sleep(1)

        # Click on a specific test result to view details
        self.driver.find_element(By.LINK_TEXT, 'View Details').click()
        time.sleep(1)

        # Verify test result details are displayed
        self.assertIn("Test Result Details", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
