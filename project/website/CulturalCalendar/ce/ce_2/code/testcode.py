import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalCalendarApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9006/')  # Navigate to the login page

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

        # Verify the Registration form is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already taken username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming the page reloads with an error

    def test_user_login(self):
        # Verify the Login form is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9006/')  # Navigate back to login
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming the page reloads with an error

    def test_view_upcoming_events(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify a list of upcoming cultural events is displayed
        events = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(events), 0, "No events found.")

    def test_view_event_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a specific event
        event_link = self.driver.find_element(By.LINK_TEXT, 'Art Exhibition')
        event_link.click()

        # Verify the Event Details Page is displayed
        self.assertIn("Event Details", self.driver.title)

    def test_search_for_events(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Enter a keyword in the search bar
        search_box = self.driver.find_element(By.NAME, 'search')
        search_box.send_keys("Art")
        search_box.submit()

        # Verify the list of events is filtered
        events = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(events), 0, "No events found.")

    def test_set_reminder_for_event(self):
        # Login and navigate to the Event Details Page
        self.login("admin", "admin123")
        event_link = self.driver.find_element(By.LINK_TEXT, 'Art Exhibition')
        event_link.click()

        # Click the 'Set Reminder' button
        self.driver.find_element(By.LINK_TEXT, 'Set Reminder').click()

        # Verify the event is added to the user's reminders list
        self.driver.find_element(By.LINK_TEXT, 'Reminders').click()
        reminders = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(reminders), 0, "No reminders found.")

    def test_view_and_manage_reminders(self):
        # Login and navigate to the Reminders Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Reminders').click()

        # Verify the list of reminders is displayed
        reminders = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(reminders), 0, "No reminders found.")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local Data Storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
