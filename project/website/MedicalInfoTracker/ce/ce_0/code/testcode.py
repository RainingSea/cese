import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8301/login')

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
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8301/register')

        # Verify registration page loaded
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with existing username
        self.driver.get('http://localhost:8301/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        error_message = self.driver.find_element(By.XPATH, '//p[@style="color:red;"]').text
        self.assertEqual(error_message, "Username already exists.")

    def test_user_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8301/login')

        # Verify login page loaded
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Attempt login with invalid credentials
        self.driver.get('http://localhost:8301/login')
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("Login", self.driver.title)

    def test_manage_medical_information(self):
        # Functionality 3: Manage Medical Information
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Medical Info').click()
        time.sleep(1)

        # Verify medical information page loaded
        self.assertIn("Medical Information", self.driver.title)

        # Add new medical information
        self.driver.find_element(By.NAME, 'diagnosis').send_keys("Test Diagnosis")
        self.driver.find_element(By.XPATH, '//button[text()="Add Diagnosis"]').click()
        time.sleep(1)

        # Verify new diagnosis added
        self.assertIn("Test Diagnosis", self.driver.page_source)

    def test_set_and_receive_appointment_reminders(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Manage Appointments').click()
        time.sleep(1)

        # Verify appointments page loaded
        self.assertIn("Appointments", self.driver.title)

        # Set a new appointment
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")
        self.driver.find_element(By.NAME, 'time').send_keys("15:00")
        self.driver.find_element(By.NAME, 'description').send_keys("Test Appointment")
        self.driver.find_element(By.XPATH, '//button[text()="Add Appointment"]').click()
        time.sleep(1)

        # Verify new appointment added
        self.assertIn("Test Appointment", self.driver.page_source)

    def test_view_and_edit_medical_history(self):
        # Functionality 5: View and Edit Medical History
        self.fail("Not implemented")

    def test_user_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")

        # Verify dashboard page loaded
        self.assertIn("Dashboard", self.driver.title)

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access dashboard after logout
        self.driver.get('http://localhost:8301/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
