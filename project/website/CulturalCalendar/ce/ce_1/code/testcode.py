import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8600/')  # Access the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        # Expect an error message (not implemented in the codebase)
        self.fail("Error message for duplicate username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8600/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_view_upcoming_events(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify that a list of upcoming cultural events is displayed
        events = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(events), 0, "No events found on the Dashboard.")

    def test_view_event_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a specific event
        self.driver.find_element(By.LINK_TEXT, 'Diwali').click()
        self.assertIn("Event Details", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("Festival of Lights", self.driver.page_source)
        self.assertIn("Celebrated in India", self.driver.page_source)
        self.assertIn("India", self.driver.page_source)

    def test_set_reminder_for_event(self):
        # Login and navigate to the Event Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Diwali').click()

        # Click the 'Set Reminder' button
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Navigate to the Reminders Page
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()
        self.assertIn("Your Reminders", self.driver.title)

        # Verify the event appears in the list of reminders
        reminders = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertTrue(any("Diwali" in reminder.text for reminder in reminders))

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8600/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
