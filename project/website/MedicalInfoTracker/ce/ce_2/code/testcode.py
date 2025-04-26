import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestMedicalInfoTracker(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8080/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8080/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8080/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("username is already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8080/')
        self.login("admin", "wrongpassword")  # Invalid password
        time.sleep(1)  # Wait for the next page to load

        # Check for error message
        self.assertIn("credentials are incorrect", self.driver.page_source)

    def test_manage_medical_info(self):
        # Functionality 3: Manage Medical Information
        self.login("admin", "admin123")  # Log in successfully

        # Navigate to Medical Information section (assuming a link exists)
        self.driver.get('http://localhost:8080/medical_info')  # Replace with actual URL if needed
        time.sleep(1)  # Wait for the next page to load

        # Verify current medical information
        self.assertIn("Allergic to penicillin", self.driver.page_source)

        # Input new medical information
        self.driver.find_element(By.NAME, 'info').send_keys("New medical info")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)  # Wait for saving the entry

        # Verify that the new information is displayed
        self.assertIn("New medical info", self.driver.page_source)

    def test_set_reminders(self):
        # Functionality 4: Set and Receive Appointment Reminders
        self.login("admin", "admin123")  # Log in successfully

        # Navigate to Appointment Reminders section (assuming a link exists)
        self.driver.get('http://localhost:8080/reminders')  # Replace with actual URL if needed
        time.sleep(1)  # Wait for the next page to load

        # Verify existing reminders
        self.assertIn("Doctor appointment on 2023-12-01", self.driver.page_source)

        # Set a new reminder
        self.driver.find_element(By.NAME, 'reminder').send_keys("New appointment on 2023-12-10")
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()
        time.sleep(1)  # Wait for saving the reminder

        # Verify that the new reminder is displayed
        self.assertIn("New appointment on 2023-12-10", self.driver.page_source)

    def test_logout(self):
        # Functionality 6: User Logout
        self.login("admin", "admin123")  # Log in successfully

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8080/dashboard')  # Replace with actual URL if needed
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
