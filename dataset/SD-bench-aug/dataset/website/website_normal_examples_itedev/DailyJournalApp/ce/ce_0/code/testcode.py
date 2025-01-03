import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDailyJournalApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

    def tearDown(self):
        # Close the web driver session and the application process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")  # Use valid credentials

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_journal_entries(self):
        # Functionalities 4: Test viewing journal entries after logging in
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows entries
        entries = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_create_new_entry(self):
        # Functionalities 5: Test creating a new journal entry
        self.login("admin", "admin123")

        # Navigate to New Entry Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Entry').click()
        time.sleep(1)  # Wait for the next page to load

        entry_title = "My New Journal Entry"
        entry_content = "This is the content of my new journal entry."

        # Fill out the new entry form
        self.driver.find_element(By.NAME, 'title').send_keys(entry_title)
        self.driver.find_element(By.NAME, 'content').send_keys(entry_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        time.sleep(1)  # Wait for saving the entry

        # Verify that the new entry is displayed on the Dashboard
        self.assertIn(entry_title, self.driver.page_source)

    def test_save_journal_entry(self):
        # Functionalities 6: Test saving journal entry (not implemented)
        self.fail("Save journal entry functionality not implemented")

    def test_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionalities 8: Test data storage (not implemented)
        self.fail("Data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
