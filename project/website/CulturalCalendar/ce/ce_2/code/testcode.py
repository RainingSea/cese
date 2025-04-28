import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8305/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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

        # Verify that the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Using an existing username
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check for error message indicating username is already in use
        self.assertIn("Username already in use", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8305/')  # Access the login page

        # Enter a valid username and password
        self.login("user1", "user123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Upcoming Events", self.driver.page_source)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8305/')  # Access the login page again
        self.login("user1", "wrong_password")

        # Check for error message indicating invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_upcoming_events(self):
        # Login successfully
        self.login("user1", "user123")

        # Verify that a list of upcoming cultural events is displayed
        self.assertIn("Upcoming Events", self.driver.page_source)

    def test_view_event_details(self):
        # Login successfully
        self.login("user1", "user123")

        # Click on a specific event from the list on the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, "Details").click()

        # Verify that the Event Details Page is displayed
        self.assertIn("Event Details", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("Significance:", self.driver.page_source)
        self.assertIn("History:", self.driver.page_source)
        self.assertIn("Location:", self.driver.page_source)

    def test_set_reminder_for_event(self):
        # Login successfully
        self.login("user1", "user123")

        # Click on a specific event from the list on the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, "Details").click()

        # Click the 'Set Reminder' button
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is set (check for confirmation message)
        self.assertIn("Reminder set successfully", self.driver.page_source)

        # Navigate to the Reminders Page
        self.driver.get('http://localhost:8305/reminders')

        # Verify that the event appears in the list of reminders
        self.assertIn("Event ID:", self.driver.page_source)

    def test_view_and_manage_reminders(self):
        # Login successfully
        self.login("user1", "user123")

        # Navigate to the Reminders Page
        self.driver.get('http://localhost:8305/reminders')

        # Verify that the list of reminders is displayed
        self.assertIn("Your Reminders", self.driver.page_source)

        # Click on a reminder to remove it from the list (assuming there's a remove button)
        # This part is not implemented in the codebase, so we will fail the test
        self.fail("Remove reminder functionality not implemented")

    def test_user_logout(self):
        # Login successfully
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8305/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
