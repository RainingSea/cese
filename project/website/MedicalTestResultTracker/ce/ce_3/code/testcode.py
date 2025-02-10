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
        self.driver.get('http://localhost:8707/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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

        # Enter a valid username and password, then submit
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("user1")
        self.driver.find_element(By.NAME, 'password').send_keys("user123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("user1", "user123")

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8707/')
        self.login("user1", "wrongpassword")

        # Verify redirection back to login page
        self.assertIn("Login", self.driver.title)

    def test_input_and_manage_medical_test_results(self):
        self.login("user1", "user123")

        # Verify the Dashboard Page is displayed
        self.assertIn("Dashboard", self.driver.title)

        # Input valid medical test results
        self.driver.find_element(By.NAME, 'test_name').send_keys("Cholesterol Test")
        self.driver.find_element(By.NAME, 'result_value').send_keys("180")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-25")
        self.driver.find_element(By.XPATH, '//button[text()="Add Test Result"]').click()
        time.sleep(1)

        # Verify the test result is saved
        self.assertIn("Cholesterol Test", self.driver.page_source)

    def test_set_and_receive_reminders(self):
        self.login("user1", "user123")

        # Navigate to the Reminders Page
        self.driver.find_element(By.LINK_TEXT, 'Go to Reminders').click()
        time.sleep(1)

        # Verify the Reminders Page is displayed
        self.assertIn("Reminders", self.driver.title)

        # Set a reminder
        self.driver.find_element(By.NAME, 'test_name').send_keys("MRI Scan")
        self.driver.find_element(By.NAME, 'reminder_date').send_keys("2023-11-01")
        self.driver.find_element(By.XPATH, '//button[text()="Add Reminder"]').click()
        time.sleep(1)

        # Verify the reminder is saved
        self.assertIn("MRI Scan", self.driver.page_source)

    def test_user_logout(self):
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
