import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8527/')

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Functionality 2: User Login
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8527/login')
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_view_upcoming_events(self):
        # Functionality 3: View Upcoming Cultural Events on the Dashboard Page
        self.login("admin", "admin123")

        # Verify a list of upcoming cultural events is displayed
        events = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(events), 0, "No events found.")

    def test_view_event_details(self):
        # Functionality 4: View Event Details
        self.login("admin", "admin123")

        # Click on a specific event from the list on the Dashboard Page
        events = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        if events:
            events[0].find_element(By.TAG_NAME, 'a').click()
            time.sleep(1)  # Wait for the next page to load

            # Verify the Event Details Page is displayed
            self.assertIn("Event Details", self.driver.title)

    def test_search_for_events(self):
        # Functionality 5: Search for Events
        self.fail("Not implemented")

    def test_set_reminder_for_event(self):
        # Functionality 6: Set Reminder for an Event
        self.fail("Not implemented")

    def test_view_and_manage_reminders(self):
        # Functionality 7: View and Manage Reminders
        self.fail("Not implemented")

    def test_user_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Functionality 9: Local Data Storage
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
