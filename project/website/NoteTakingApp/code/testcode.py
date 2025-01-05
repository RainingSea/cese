import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8033')

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

    def test_user_login(self):
        # Test case for user login
        self.login("admin", "pass123")
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        self.assertIn("Login", self.driver.title)

    def test_view_notes_on_dashboard(self):
        # Test case for viewing notes on the dashboard
        self.login("admin", "pass123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Test case for adding a new note
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        time.sleep(1)  # Wait for the add note page to load

        note_title = "Test Note"
        note_content = "This is a test note."

        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Add Note"]').click()
        time.sleep(1)  # Wait for the dashboard to load

        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Test case for viewing note details
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Note 1').click()
        time.sleep(1)  # Wait for the view note page to load

        self.assertIn("Note 1", self.driver.page_source)
        self.assertIn("This is the content of note 1.", self.driver.page_source)

    def test_edit_note(self):
        # Test case for editing a note (not implemented)
        self.fail("Edit note functionality not implemented")

    def test_delete_note(self):
        # Test case for deleting a note (not implemented)
        self.fail("Delete note functionality not implemented")

    def test_search_for_note(self):
        # Test case for searching for a note
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        time.sleep(1)  # Wait for the search note page to load

        self.driver.find_element(By.NAME, 'title').send_keys("Note 1")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        self.assertIn("Note 1", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Test case for navigating back to the dashboard
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        time.sleep(1)  # Wait for the search note page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the dashboard to load

        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Test case for logging out
        self.login("admin", "pass123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
