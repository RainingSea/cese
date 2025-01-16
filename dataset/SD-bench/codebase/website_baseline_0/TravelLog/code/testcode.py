import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestTravelLogApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8559')

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
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)

        # Enter a valid username and password, then submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an already existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        messages = self.driver.find_elements(By.CLASS_NAME, 'alert-danger')
        self.assertGreater(len(messages), 0, "No error message displayed for existing username.")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Journal", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8559')
        self.login("invalid", "invalid")

        # Verify error message for invalid credentials
        messages = self.driver.find_elements(By.CLASS_NAME, 'alert-danger')
        self.assertGreater(len(messages), 0, "No error message displayed for invalid credentials.")

    def test_create_and_save_journal_entries(self):
        # Log in and navigate to the Journal Entry Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add New Entry').click()
        time.sleep(1)

        # Fill in the form with valid details and submit
        self.driver.find_element(By.NAME, 'destination').send_keys('Tokyo')
        self.driver.find_element(By.NAME, 'dates').send_keys('2023-08-01 to 2023-08-10')
        self.driver.find_element(By.NAME, 'activities').send_keys('Sightseeing')
        self.driver.find_element(By.NAME, 'photos').send_keys('')
        self.driver.find_element(By.NAME, 'reflections').send_keys('Great trip!')
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)

        # Verify entry is saved successfully
        self.assertIn("View Entries", self.driver.title)

        # Attempt to submit the form with missing required fields
        self.driver.find_element(By.LINK_TEXT, 'Add New Entry').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'destination').send_keys('')
        self.driver.find_element(By.NAME, 'dates').send_keys('')
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)

        # Verify error message for missing fields
        messages = self.driver.find_elements(By.CLASS_NAME, 'alert-danger')
        self.assertGreater(len(messages), 0, "No error message displayed for missing fields.")

    def test_view_and_organize_past_entries(self):
        # Log in and navigate to the Past Entries Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Entries').click()
        time.sleep(1)

        # Verify list of past entries is displayed
        entries = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(entries), 0, "No past entries found.")

        # Filter entries by destination
        # (Assuming there is a filter functionality implemented, which is not present in the codebase)
        self.fail("Filter functionality not implemented.")

        # Sort entries by date
        # (Assuming there is a sort functionality implemented, which is not present in the codebase)
        self.fail("Sort functionality not implemented.")

    def test_edit_or_delete_travel_entries(self):
        # Log in and navigate to the Past Entries Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Entries').click()
        time.sleep(1)

        # Select an entry to edit
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)

        # Modify the entry details and submit
        self.driver.find_element(By.NAME, 'destination').clear()
        self.driver.find_element(By.NAME, 'destination').send_keys('Kyoto')
        self.driver.find_element(By.XPATH, '//button[text()="Update Entry"]').click()
        time.sleep(1)

        # Verify entry is updated successfully
        self.assertIn("View Entries", self.driver.title)

        # Select an entry to delete
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
        time.sleep(1)

        # Verify entry is deleted successfully
        self.assertIn("View Entries", self.driver.title)

    def test_share_travel_entries(self):
        # Log in and navigate to a specific travel entry
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Entries').click()
        time.sleep(1)

        # Click the "Share" button
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)

        # Verify shareable link is generated
        messages = self.driver.find_elements(By.CLASS_NAME, 'alert-info')
        self.assertGreater(len(messages), 0, "No shareable link generated.")

        # Attempt to share an entry that has not been saved
        # (Assuming there is a check for unsaved entries, which is not present in the codebase)
        self.fail("Check for unsaved entries not implemented.")

    def test_search_for_specific_entries_or_destinations(self):
        # Log in and navigate to the Search Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Entries').click()
        time.sleep(1)

        # Enter a keyword related to an entry or destination and submit
        self.driver.find_element(By.NAME, 'search_term').send_keys('Paris')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results display entries that match the keyword
        entries = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(entries), 0, "No search results found for the keyword.")

        # Enter a keyword that does not match any entries
        self.driver.find_element(By.NAME, 'search_term').clear()
        self.driver.find_element(By.NAME, 'search_term').send_keys('Nonexistent')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify message indicating no entries were found
        messages = self.driver.find_elements(By.CLASS_NAME, 'alert-info')
        self.assertGreater(len(messages), 0, "No message displayed for no search results.")

    def test_user_logout(self):
        # Log in and click the "Logout" button
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify user is logged out and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8559/journal')
        self.assertIn("Login", self.driver.title)

    def test_navigate_back_to_dashboard(self):
        # Log in and navigate to a specific travel entry
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Entries').click()
        time.sleep(1)

        # Click the "Back to Dashboard" button
        # (Assuming there is a "Back to Dashboard" button, which is not present in the codebase)
        self.fail("Back to Dashboard functionality not implemented.")

        # Refresh the Dashboard Page after making changes to an entry
        self.driver.refresh()
        time.sleep(1)

        # Verify updated entries are displayed correctly
        # (Assuming there is a check for updated entries, which is not present in the codebase)
        self.fail("Check for updated entries not implemented.")

if __name__ == '__main__':
    unittest.main()
