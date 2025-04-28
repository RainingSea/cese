import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalInfoTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8342/')  # Use the port from main.py

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
        self.driver.get('http://localhost:8342/register')  # Navigate to Registration Page
        self.assertIn("Registration", self.driver.title)

        new_username = "testuser"
        new_password = "testpass"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8342/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("testpass")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials

        # Verify redirection to Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8342/')
        self.login("user1", "wrongpassword")  # Invalid password

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_manage_medical_info(self):
        # Functionality 3: Manage Medical Information
        self.login("user1", "user123")  # Log in successfully

        # Navigate to Medical Information section (assuming it's part of the dashboard)
        self.driver.get('http://localhost:8342/dashboard')  # Assuming this is the dashboard URL
        self.assertIn("Your Medical Information", self.driver.page_source)

        # Input new medical information
        self.driver.find_element(By.NAME, 'info').send_keys('{"diagnoses": ["Cold"], "medications": ["Cough Syrup"], "treatments": ["Rest"]}')
        self.driver.find_element(By.XPATH, '//button[text()="Add Medical Info"]').click()

        # Verify that the new information is saved and displayed
        self.assertIn("Cold", self.driver.page_source)

    def test_set_appointment(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("user1", "user123")  # Log in successfully

        # Navigate to set appointment (assuming it's part of the dashboard)
        self.driver.get('http://localhost:8342/dashboard')  # Assuming this is the dashboard URL
        self.driver.find_element(By.NAME, 'appointment').send_keys('{"date": "2023-10-01", "time": "10:00 AM", "description": "Check-up"}')
        self.driver.find_element(By.XPATH, '//button[text()="Set Appointment"]').click()

        # Verify that the appointment is saved and displayed
        self.assertIn("Check-up", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("user1", "user123")  # Log in successfully

        # Click the logout button (assuming it's part of the dashboard)
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
