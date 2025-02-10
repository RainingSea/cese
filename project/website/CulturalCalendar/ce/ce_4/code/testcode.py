import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8603/')  # Navigate to the login page

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
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration form is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "new_user"
        new_password = "new_password"
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
        self.assertIn("Registration", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8603/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_view_upcoming_events(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify a list of upcoming cultural events is displayed
        events = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(events), 0, "No events found.")

    def test_view_event_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a specific event from the list
        self.driver.find_element(By.LINK_TEXT, 'Art Exhibition').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Event Details Page is displayed
        self.assertIn("Art Exhibition", self.driver.title)

    def test_search_for_events(self):
        # This functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_set_reminder_for_event(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the 'Add Reminder' button for an event
        self.driver.find_element(By.XPATH, '//button[text()="Add Reminder"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the Reminders Page
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the event appears in the list of reminders
        reminders = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(reminders), 0, "No reminders found.")

    def test_view_and_manage_reminders(self):
        # This functionality is not implemented in the codebase
        self.fail("Manage reminders functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
