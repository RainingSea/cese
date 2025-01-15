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
        self.driver.get('http://localhost:8641/login')

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

        # Verify Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8641/login')
        self.login("invalid_user", "wrong_password")

        # Check for error message (not implemented in codebase)
        self.fail("Error message for invalid login not implemented")

    def test_input_and_manage_medical_test_results(self):
        # Log in and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify Test Results Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Input valid medical test results
        self.driver.find_element(By.ID, 'test_name').send_keys("X-Ray")
        self.driver.find_element(By.ID, 'result').send_keys("7.5")
        self.driver.find_element(By.ID, 'date').send_keys("2023-10-15")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()
        time.sleep(1)

        # Verify test result is added
        self.assertIn("X-Ray: 7.5 on 2023-10-15", self.driver.page_source)

        # Attempt to input invalid test results
        self.driver.find_element(By.ID, 'test_name').send_keys("Invalid Test")
        self.driver.find_element(By.ID, 'result').send_keys("-5")
        self.driver.find_element(By.ID, 'date').send_keys("2023-10-15")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.fail("Error message for invalid test result not implemented")

    def test_set_and_receive_reminders(self):
        # Log in and navigate to the Reminders Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()
        time.sleep(1)

        # Verify Reminders Page is displayed
        self.assertIn("Reminders", self.driver.title)

        # Set a reminder
        self.driver.find_element(By.ID, 'message').send_keys("Follow-up Test")
        self.driver.find_element(By.ID, 'date').send_keys("2023-10-20")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()
        time.sleep(1)

        # Verify reminder is added
        self.assertIn("Follow-up Test on 2023-10-20", self.driver.page_source)

    def test_user_logout(self):
        # Log in and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
