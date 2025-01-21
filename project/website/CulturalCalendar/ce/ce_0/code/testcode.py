import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9004/') 

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration form is displayed
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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Expect an error message indicating the username is already in use
        self.assertIn("Username is already in use", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9004/')
        self.login("invalid_user", "invalid_pass")

        # Expect an error message indicating invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_view_upcoming_events(self):
        # Functionality 3: View Upcoming Cultural Events on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that a list of upcoming cultural events is displayed
        events = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(events), 0, "No cultural events found.")

    def test_view_event_details(self):
        # Functionality 4: View Event Details
        self.login("admin", "admin123")

        # Click on a specific event from the list on the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'Cultural Festival').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Event Details Page for that event is displayed
        self.assertIn("Event Details", self.driver.title)

        # Check the significance, history, and location information
        self.assertIn("Cultural Festival", self.driver.page_source)
        self.assertIn("A celebration of local culture and arts.", self.driver.page_source)
        self.assertIn("City Park", self.driver.page_source)

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

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Functionality 9: Local Data Storage
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
