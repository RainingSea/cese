import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8140/')  # Access the login page

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

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("test_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("User already exists!", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8140/login')

        # Verify that the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8140/login')
        self.login("admin", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_view_upcoming_events(self):
        # Login successfully
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows upcoming events
        self.assertIn("Upcoming Events", self.driver.page_source)

    def test_view_event_details(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click on a specific event from the list
        self.driver.find_element(By.LINK_TEXT, "New Year Celebration").click()

        # Verify that the Event Details Page is displayed
        self.assertIn("Event Details", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("Significance: Significance of new beginnings", self.driver.page_source)

    def test_set_reminder_for_event(self):
        # Login successfully
        self.login("user1", "user123")

        # Navigate to the Event Details Page for a specific event
        self.driver.find_element(By.LINK_TEXT, "Thanksgiving").click()

        # Click the 'Set Reminder' button
        self.driver.find_element(By.XPATH, '//button[text()="Set Reminder"]').click()

        # Verify that the event appears in the user's reminders list
        self.driver.get('http://localhost:8140/reminders')
        self.assertIn("Thanksgiving", self.driver.page_source)

    def test_view_and_manage_reminders(self):
        # Login successfully
        self.login("user1", "user123")

        # Navigate to the Reminders Page
        self.driver.get('http://localhost:8140/reminders')

        # Verify that the list of reminders is displayed
        self.assertIn("My Reminders", self.driver.page_source)

    def test_user_logout(self):
        # Login successfully
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
