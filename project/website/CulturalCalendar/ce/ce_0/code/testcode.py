import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the server and initialize the webdriver
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the server process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        new_username = "test_user"
        new_password = "test_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with the same username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Username already in use", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8000/')  # Go back to login page
        self.login("invalid_user", "invalid_password")

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_upcoming_events(self):
        # Functionality 3: View Upcoming Cultural Events on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows events
        self.assertIn("Upcoming Cultural Events", self.driver.page_source)

    def test_view_event_details(self):
        # Functionality 4: View Event Details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'New Year').click()  # Click on an event

        # Verify that the Event Details Page is displayed
        self.assertIn("Event Details", self.driver.title)
        self.assertIn("Celebration of the new year", self.driver.page_source)

    def test_set_reminder(self):
        # Functionality 6: Set Reminder for an Event
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Diwali').click()  # Click on an event
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder was set
        self.driver.get('http://localhost:8000/reminders')  # Navigate to reminders page
        self.assertIn("Diwali", self.driver.page_source)

    def test_view_reminders(self):
        # Functionality 7: View and Manage Reminders
        self.login("user1", "user123")
        self.driver.get('http://localhost:8000/reminders')  # Navigate to reminders page

        # Verify that the reminders are displayed
        self.assertIn("Your Reminders", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
