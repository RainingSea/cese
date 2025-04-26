import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalInfoTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8179/')  # Access the login page

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
        self.driver.get('http://localhost:8179/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Medical Information", self.driver.page_source)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8179/')
        self.login("admin", "wrong_password")  # Invalid credentials

        # Verify error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_manage_medical_info(self):
        # Functionality 3: Manage Medical Information
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8179/medical_info')  # Navigate to Medical Info Page

        # Verify the page is displayed
        self.assertIn("Medical Information", self.driver.title)

        # Add new medical information
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'info').send_keys("New Diagnosis Info")
        self.driver.find_element(By.XPATH, '//button[text()="Add Info"]').click()

        # Verify that the new information is saved
        self.assertIn("New Diagnosis Info", self.driver.page_source)

    def test_set_reminders(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("admin", "admin123")  # Log in successfully
        self.driver.get('http://localhost:8179/reminders')  # Navigate to Reminders Page

        # Verify the page is displayed
        self.assertIn("Set Reminders", self.driver.title)

        # Set a new reminder
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'reminder').send_keys("Checkup Appointment")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is saved
        self.assertIn("Checkup Appointment", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in successfully
        # Assuming there is a logout button to click
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
