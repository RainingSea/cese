import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8303/') 

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8303/register')
        
        # Verify that the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.get('http://localhost:8303/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Using an existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Username already in use", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8303/')
        
        # Verify that the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials and log in
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to log in with invalid credentials
        self.driver.get('http://localhost:8303/')
        self.login("invalid_user", "wrong_password")

        # Verify that an error message is displayed
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_upcoming_events(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows upcoming events
        self.assertIn("Upcoming Events", self.driver.page_source)

    def test_view_event_details(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click on a specific event from the list
        self.driver.find_element(By.LINK_TEXT, "New Year Celebration").click()

        # Verify that the Event Details Page is displayed
        self.assertIn("Event Details", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("Celebration of the new year", self.driver.page_source)
        self.assertIn("A grand celebration welcoming the new year", self.driver.page_source)
        self.assertIn("City Square", self.driver.page_source)

    def test_set_reminder_for_event(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click on a specific event from the list
        self.driver.find_element(By.LINK_TEXT, "New Year Celebration").click()

        # Click the 'Set Reminder' button
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the reminder is set by checking the reminders page
        self.driver.get('http://localhost:8303/reminders')
        self.assertIn("New Year Celebration", self.driver.page_source)

    def test_view_and_manage_reminders(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Set a reminder for an event
        self.driver.get('http://localhost:8303/event/1')  # Assuming event ID 1 is "New Year Celebration"
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Navigate to the Reminders Page
        self.driver.get('http://localhost:8303/reminders')

        # Verify that the reminder is displayed
        self.assertIn("New Year Celebration", self.driver.page_source)

        # Note: The functionality to remove reminders is not implemented in the provided codebase
        self.fail("Functionality to remove reminders is not implemented")

    def test_user_logout(self):
        # Log in successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
