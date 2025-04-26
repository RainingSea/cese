import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalTestResultTracker(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8182/') 

    def tearDown(self):
        # Close the web driver session and the subprocess
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8182/register')
        
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.get('http://localhost:8182/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")

        # Verify that the Test Results Page has loaded
        self.assertIn("Test Results", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8182/')
        self.login("user1", "wrongpassword")  # invalid password

        # Verify error message for incorrect credentials
        self.assertIn("Login credentials are incorrect", self.driver.page_source)

    def test_manage_test_results(self):
        # Functionality 3: Input and Manage Medical Test Results
        self.login("user1", "user123")
        
        # Verify that the Test Results Page is displayed
        self.assertIn("Test Results", self.driver.title)

        # Input valid medical test results
        self.driver.find_element(By.NAME, 'test_name').send_keys("Blood Test")
        self.driver.find_element(By.NAME, 'result').send_keys("Normal")
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()

        # Verify that the test result is saved
        self.assertIn("Blood Test: Normal", self.driver.page_source)

        # Attempt to input invalid test results (e.g., negative values)
        self.driver.find_element(By.NAME, 'test_name').send_keys("Invalid Test")
        self.driver.find_element(By.NAME, 'result').send_keys("-1")  # invalid result
        self.driver.find_element(By.XPATH, '//button[text()="Add Result"]').click()

        # Verify error message for invalid input
        self.assertIn("Invalid input", self.driver.page_source)

    def test_set_reminders(self):
        # Functionality 5: Set and Receive Reminders
        self.login("user1", "user123")
        self.driver.get('http://localhost:8182/reminders')

        # Set a reminder
        self.driver.find_element(By.NAME, 'reminder_text').send_keys("Follow-up Test")
        self.driver.find_element(By.NAME, 'date').send_keys("2023-10-10")  # example date
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is saved
        self.assertIn("Follow-up Test", self.driver.page_source)

    def test_logout(self):
        # Functionality 7: User Logout
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
