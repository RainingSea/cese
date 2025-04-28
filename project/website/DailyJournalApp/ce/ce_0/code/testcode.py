import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDailyJournalApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_journal_entries(self):
        # Functionalities 4: View Journal Entries
        self.login("admin", "admin123")
        entries = self.driver.find_elements(By.TAG_NAME, 'li')  # Assuming entries are in <li> tags
        self.assertGreater(len(entries), 0, "No journal entries found.")

    def test_create_new_entry(self):
        # Functionalities 5: Create a New Journal Entry
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Create New Entry').click()
        entry_title = "My New Journal Entry"
        entry_content = "This is the content of my new journal entry."
        self.driver.find_element(By.NAME, 'title').send_keys(entry_title)
        self.driver.find_element(By.NAME, 'content').send_keys(entry_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Entry"]').click()
        self.assertIn(entry_title, self.driver.page_source)

    def test_save_journal_entry(self):
        # Functionalities 6: Save Journal Entry
        self.fail("Not implemented")  # Placeholder for future implementation

    def test_logout(self):
        # Functionalities 7: Log Out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_data_storage(self):
        # Functionalities 8: Data Storage
        self.fail("Not implemented")  # Placeholder for future implementation

if __name__ == '__main__':
    unittest.main()
