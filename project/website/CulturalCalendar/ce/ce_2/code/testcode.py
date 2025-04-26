import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8141/')  # Access the login page

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
        self.driver.get('http://localhost:8141/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.get('http://localhost:8141/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Using existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expect an error message indicating username is already in use
        self.assertIn("User already exists", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8141/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_events(self):
        # Functionality 3: View Upcoming Cultural Events
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8141/dashboard')  # Navigate to Dashboard Page
        self.assertIn("Upcoming Events", self.driver.page_source)

    def test_view_event_details(self):
        # Functionality 4: View Event Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8141/dashboard')
        self.driver.find_element(By.LINK_TEXT, "Cultural Festival").click()  # Click on an event
        self.assertIn("Event Details", self.driver.title)
        self.assertIn("Cultural Festival", self.driver.page_source)

    def test_set_reminder(self):
        # Functionality 6: Set Reminder for an Event
        self.login("user1", "user123")  # Login as user1
        self.driver.get('http://localhost:8141/event/Cultural Festival')  # Navigate to Event Details Page
        self.driver.find_element(By.LINK_TEXT, "Set Reminder").click()  # Click the 'Set Reminder' button

        # Verify reminder is set
        self.driver.get('http://localhost:8141/reminders')  # Navigate to Reminders Page
        self.assertIn("Cultural Festival", self.driver.page_source)

    def test_view_reminders(self):
        # Functionality 7: View and Manage Reminders
        self.login("user1", "user123")
        self.driver.get('http://localhost:8141/reminders')
        self.assertIn("Your Reminders", self.driver.title)
        self.assertIn("Cultural Festival", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
