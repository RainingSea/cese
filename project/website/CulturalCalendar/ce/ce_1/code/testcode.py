import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8304/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8304/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)  # Check if Registration form is displayed

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.get('http://localhost:8304/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Registration failed", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to Dashboard

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8304/')
        self.login("admin", "wrongpassword")  # Invalid password
        self.assertIn("Login failed", self.driver.page_source)  # Check for error message

    def test_view_upcoming_events(self):
        # Functionality 3: View Upcoming Cultural Events on the Dashboard Page
        self.login("admin", "admin123")  # Login successfully
        self.assertIn("Upcoming Cultural Events", self.driver.page_source)  # Check if events are displayed

    def test_view_event_details(self):
        # Functionality 4: View Event Details
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, "Details").click()  # Click on event details
        self.assertIn("Event Details", self.driver.title)  # Check if Event Details Page is displayed

    def test_set_reminder(self):
        # Functionality 6: Set Reminder for an Event
        self.login("admin", "admin123")  # Login successfully
        self.driver.find_element(By.LINK_TEXT, "Details").click()  # Click on event details
        self.driver.find_element(By.NAME, 'date').send_keys("2023-12-01")  # Set reminder date
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()  # Submit reminder
        self.assertIn("Dashboard", self.driver.title)  # Check if redirected to Dashboard

    def test_view_reminders(self):
        # Functionality 7: View and Manage Reminders
        self.login("admin", "admin123")  # Login successfully
        self.driver.get('http://localhost:8304/reminders/admin')  # Navigate to Reminders Page
        self.assertIn("Your Reminders", self.driver.page_source)  # Check if reminders are displayed

if __name__ == '__main__':
    unittest.main()
