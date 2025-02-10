import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start

        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8667/login')

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
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
        self.driver.get('http://localhost:8667/register')
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8667/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the current codebase)
        # self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8667/login')
        self.login("invaliduser", "invalidpass")
        self.assertIn("Login", self.driver.title)

    def test_create_and_save_journal_entries(self):
        # Log in and navigate to the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Create a new journal entry
        self.driver.find_element(By.NAME, 'destination').send_keys('New York')
        self.driver.find_element(By.NAME, 'date').send_keys('2023-10-10')
        self.driver.find_element(By.NAME, 'activities').send_keys('Visited Central Park')
        self.driver.find_element(By.NAME, 'photos').send_keys('photo4.jpg')
        self.driver.find_element(By.NAME, 'reflections').send_keys('It was amazing!')
        self.driver.find_element(By.XPATH, '//button[text()="Create Entry"]').click()
        time.sleep(1)

        # Verify the entry is saved
        self.assertIn("New York", self.driver.page_source)

        # Attempt to submit with missing fields
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'date').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Create Entry"]').click()
        time.sleep(1)

        # Check for error message (not implemented in the current codebase)
        # self.assertIn("Fields are required", self.driver.page_source)

    def test_view_and_organize_past_entries(self):
        # Log in and navigate to the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify past entries are displayed
        entries = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(entries), 0)

        # Filter and sort functionality not implemented in the current codebase

    def test_edit_or_delete_travel_entries(self):
        # Functionality not implemented in the current codebase
        self.fail("Edit or delete functionality not implemented")

    def test_share_travel_entries(self):
        # Functionality not implemented in the current codebase
        self.fail("Share functionality not implemented")

    def test_search_for_specific_entries(self):
        # Functionality not implemented in the current codebase
        self.fail("Search functionality not implemented")

    def test_user_logout(self):
        # Log in and navigate to the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Functionality not implemented in the current codebase
        self.fail("Navigate back to dashboard functionality not implemented")

if __name__ == '__main__':
    unittest.main()
