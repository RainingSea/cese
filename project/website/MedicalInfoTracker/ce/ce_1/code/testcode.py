import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestMedicalInfoTrackerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8180/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8180/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8180/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing user
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("User already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8180/')
        self.login("admin", "wrong_password")
        self.assertIn("Invalid credentials.", self.driver.page_source)

    def test_manage_medical_info(self):
        # Functionality 3: Manage Medical Information
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8180/dashboard')  # Navigate to Dashboard

        # Add medical information
        self.driver.find_element(By.NAME, 'medical_info').send_keys("Allergy to pollen")
        self.driver.find_element(By.XPATH, '//button[text()="Add"]').click()

        # Verify the new information is displayed
        self.assertIn("Allergy to pollen", self.driver.page_source)

        # Edit medical information
        self.driver.find_element(By.NAME, 'medical_info').send_keys("Updated allergy information")
        self.driver.find_element(By.XPATH, '//button[text()="Add"]').click()
        self.assertIn("Updated allergy information", self.driver.page_source)

    def test_set_appointment_reminders(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8180/dashboard')  # Navigate to Dashboard

        # Set a new appointment reminder
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-31")
        self.driver.find_element(By.NAME, 'time').send_keys("10:00")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify the reminder is displayed
        self.assertIn("2023-12-31 10:00", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8180/dashboard')  # Navigate to Dashboard

        # Click the logout button
        self.driver.find_element(By.NAME, 'logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard after logging out
        self.driver.get('http://localhost:8180/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
