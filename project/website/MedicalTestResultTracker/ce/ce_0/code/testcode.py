import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8704/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the process
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
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the registration form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify the error message is displayed
        self.assertIn("Username already exists.", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8704/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_password")

        # Verify the error message is displayed
        self.assertIn("Invalid credentials.", self.driver.page_source)

    def test_input_and_manage_medical_test_results(self):
        # Log in successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Input valid medical test results and submit
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.NAME, 'test_name').send_keys("Blood Test")
        self.driver.find_element(By.NAME, 'result').send_keys("Normal")
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the test results are saved successfully
        self.assertIn("2023-10-10|Blood Test|Normal", self.driver.page_source)

        # Attempt to input invalid test results
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")
        self.driver.find_element(By.NAME, 'test_name').send_keys("Blood Test")
        self.driver.find_element(By.NAME, 'result').send_keys("-10")
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify the error message is displayed
        self.assertIn("Invalid input.", self.driver.page_source)

    def test_view_historical_data_and_trends(self):
        # Log in successfully and navigate to the Trends Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8704/history')  # Navigate to the history page

        # Verify the Trends Page is displayed
        self.assertIn("History", self.driver.title)

        # Select a specific test type to view its trends over time
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_set_and_receive_reminders(self):
        # Log in successfully and navigate to the Reminders Page
        self.login("admin", "admin123")
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_view_test_result_history(self):
        # Log in successfully and navigate to the Test Result History Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8704/history')  # Navigate to the history page

        # Verify the Test Result History Page is displayed
        self.assertIn("History", self.driver.title)

        # Click on a specific test result to view its details
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_user_logout(self):
        # Log in successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the logout button
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_navigate_back_to_dashboard(self):
        # Navigate to the Test Results Page after logging in
        self.login("admin", "admin123")

        # Click the back button to return to the Dashboard Page
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

    def test_view_test_result_details(self):
        # Log in successfully and navigate to the Test Results Page
        self.login("admin", "admin123")

        # Click on a specific test result to view its details
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
