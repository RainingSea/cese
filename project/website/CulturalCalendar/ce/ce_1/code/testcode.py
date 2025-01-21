import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9005/')

    def tearDown(self):
        # Close the web driver session and stop the server
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

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

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
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Expect an error message indicating that the username is already in use
        self.assertIn("already in use", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9005/')
        self.login("invalid_user", "invalid_pass")

        # Expect an error message indicating invalid credentials
        self.assertIn("invalid credentials", self.driver.page_source)

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
        time.sleep(1)

        # Verify the Event Details Page is displayed
        self.assertIn("Art Exhibition", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("An exhibition showcasing local artists.", self.driver.page_source)

    def test_set_reminder_for_event(self):
        # Login and navigate to the Event Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Art Exhibition').click()
        time.sleep(1)

        # Click the 'Set Reminder' button
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()
        time.sleep(1)

        # Navigate to the Reminders Page
        self.driver.find_element(By.LINK_TEXT, 'View Reminders').click()
        time.sleep(1)

        # Verify the event appears in the list of reminders
        reminders = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn("Art Exhibition", [reminder.text for reminder in reminders])

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9005/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
