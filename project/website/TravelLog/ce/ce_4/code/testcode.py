import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8669/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.driver.get('http://localhost:8669/register')
        self.assertIn("Register", self.driver.title)

        # Register a new user
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Attempt to register with an existing username
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in UI, so we assume failure)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Journal", self.driver.page_source)

        # Invalid login
        self.driver.get('http://localhost:8669/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_create_and_save_journal_entries(self):
        self.login("admin", "admin123")
        self.assertIn("Journal", self.driver.page_source)

        # Create a new journal entry
        self.driver.find_element(By.NAME, 'destination').send_keys('New York')
        self.driver.find_element(By.NAME, 'dates').send_keys('2023-03-01 to 2023-03-10')
        self.driver.find_element(By.NAME, 'activities').send_keys('Sightseeing, Dining')
        self.driver.find_element(By.NAME, 'reflections').send_keys('Amazing experience!')
        self.driver.find_element(By.XPATH, '//button[text()="Add Entry"]').click()
        time.sleep(1)

        # Verify the entry is saved
        self.assertIn("New York", self.driver.page_source)

    def test_view_and_organize_past_entries(self):
        self.fail("View and organize past entries not implemented")

    def test_edit_or_delete_travel_entries(self):
        self.fail("Edit or delete travel entries not implemented")

    def test_share_travel_entries(self):
        self.fail("Share travel entries not implemented")

    def test_search_for_specific_entries_or_destinations(self):
        self.fail("Search functionality not implemented")

    def test_user_logout(self):
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        self.fail("Navigate back to dashboard not implemented")

if __name__ == '__main__':
    unittest.main()
