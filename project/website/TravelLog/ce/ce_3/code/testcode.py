import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8668/')  # Navigate to the login page

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('user1')
        self.driver.find_element(By.NAME, 'password').send_keys('user123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Enter a valid username and password
        self.login("user1", "user123")

        # Verify that the user is redirected to the Journal Page
        self.assertIn("Journal", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8668/')
        self.login("invaliduser", "invalidpass")

        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_create_and_save_journal_entries(self):
        # Log in to the user account
        self.login("user1", "user123")

        # Verify that the Journal Entry form is displayed
        self.assertIn("Journal", self.driver.title)

        # Fill in the form with valid details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('New York')
        self.driver.find_element(By.NAME, 'dates').send_keys('2023-05-01 to 2023-05-10')
        self.driver.find_element(By.NAME, 'activities').send_keys('Sightseeing')
        self.driver.find_element(By.NAME, 'photos').send_keys('/path/to/photo3.jpg')
        self.driver.find_element(By.NAME, 'reflections').send_keys('Amazing trip!')
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)

        # Verify that the entry is saved successfully
        self.assertIn("New York", self.driver.page_source)

    def test_view_and_organize_past_entries(self):
        # Log in to the user account
        self.login("user1", "user123")

        # Verify that a list of past entries is displayed
        self.assertIn("Paris", self.driver.page_source)

        # Filter entries by destination (not implemented in the codebase)
        self.fail("Filter by destination not implemented")

        # Sort entries by date (not implemented in the codebase)
        self.fail("Sort by date not implemented")

    def test_edit_or_delete_travel_entries(self):
        # Log in to the user account
        self.login("user1", "user123")

        # Navigate to the Past Entries Page and select an entry to edit (not implemented in the codebase)
        self.fail("Edit entry not implemented")

        # Select an entry to delete (not implemented in the codebase)
        self.fail("Delete entry not implemented")

    def test_share_travel_entries(self):
        # Navigate to a specific travel entry (not implemented in the codebase)
        self.fail("Share entry not implemented")

    def test_search_for_specific_entries_or_destinations(self):
        # Navigate to the Search Page (not implemented in the codebase)
        self.fail("Search functionality not implemented")

    def test_user_logout(self):
        # Log in to the user account
        self.login("user1", "user123")

        # Click the "Logout" button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Log in to the user account
        self.login("user1", "user123")

        # Refresh the Dashboard Page after making changes to an entry (not implemented in the codebase)
        self.fail("Navigate back to Dashboard not implemented")

if __name__ == '__main__':
    unittest.main()
