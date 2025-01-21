import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import subprocess
import time

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8960/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and terminate the server process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the registration page to load

        new_username = "test_user"
        new_password = "test_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the login page to load

        self.assertIn("Login", self.driver.title)

    def test_view_notes_on_dashboard(self):
        # Functionalities 3: Test viewing notes on the dashboard
        self.login("user1", "user123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        time.sleep(1)  # Wait for the add note page to load

        note_title = "Test Note"
        note_content = "This is a test note."

        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Note"]').click()
        time.sleep(1)  # Wait for the dashboard to load

        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()
        time.sleep(1)  # Wait for the view note page to load

        self.assertIn("First Note", self.driver.page_source)
        self.assertIn("This is the content of the first note.", self.driver.page_source)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.fail("Edit Note functionality not implemented")

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.fail("Delete Note functionality not implemented")

    def test_search_for_note(self):
        # Functionalities 8: Test searching for a note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the search note page to load

        self.driver.find_element(By.NAME, 'query').send_keys("First Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results to load

        self.assertIn("First Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the dashboard
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the search note page to load

        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the dashboard to load

        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
