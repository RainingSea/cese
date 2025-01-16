import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8642/') 

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here").click()
        time.sleep(1)

        # Enter a valid username and password, then submit the registration form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8642/')
        self.login("invalid_user", "wrong_password")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_input_and_manage_medical_test_results(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify the Test Results Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Input valid medical test results and submit
        self.driver.find_element(By.NAME, 'test_name').send_keys('Urine Test')
        self.driver.find_element(By.NAME, 'result').send_keys('Normal')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-11-10')
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()
        time.sleep(1)

        # Verify the test results are saved successfully
        self.assertIn("Urine Test: Normal on 2023-11-10", self.driver.page_source)

    def test_view_historical_data_and_trends(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_set_and_receive_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Set a reminder for a follow-up test and save it
        self.driver.find_element(By.NAME, 'test_name').send_keys('Blood Test')
        self.driver.find_element(By.NAME, 'result').send_keys('Pending')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-11-15')
        self.driver.find_element(By.NAME, 'reminder_date').send_keys('2023-11-20')
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()
        time.sleep(1)

        # Verify the reminder is saved successfully
        self.assertIn("Reminder for Blood Test on 2023-11-20", self.driver.page_source)

    def test_view_test_result_history(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_view_test_result_details(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
