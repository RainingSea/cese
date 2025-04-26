import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyJournalApp(unittest.TestCase):

    def setUp(self):
        # Start the server and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8000/')  # Replace XXXX with the port from main.py

    def tearDown(self):
        # Close the web driver session and terminate the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_journal_entries(self):
        # Functionalities 4: Test viewing journal entries after logging in
        self.login("admin", "admin123")
        self.assertIn("Your Journal Entries:", self.driver.page_source)

    def test_create_new_entry(self):
        # Functionalities 5: Test creating a new journal entry
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Entry').click()

        entry_title = "My New Journal Entry"
        entry_content = "This is the content of my new journal entry."

        # Fill out the new entry form
        self.driver.find_element(By.NAME, 'title').send_keys(entry_title)
        self.driver.find_element(By.NAME, 'content').send_keys(entry_content)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()

        # Verify that the new entry is displayed on the Dashboard
        self.assertIn(entry_title, self.driver.page_source)

    def test_save_journal_entry(self):
        # Functionalities 6: This functionality is already covered in test_create_new_entry
        self.fail("Not implemented")

    def test_logout(self):
        # Functionalities 7: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionalities 8: This functionality is not directly testable via the UI
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
