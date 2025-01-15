import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8459/login')

    def tearDown(self):
        # Close the web driver session and stop the server
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_login(self):
        # Functionalities 1: User Login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_registration(self):
        # Functionalities 2: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)

        new_username = "new_user"
        new_password = "new_password"

        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        self.assertIn("Login", self.driver.title)

    def test_view_notes_on_dashboard(self):
        # Functionalities 3: View Notes on Dashboard Page
        self.login("user1", "user123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Add New Note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        time.sleep(1)

        note_title = "Test Note"
        note_content = "This is a test note."

        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Add Note"]').click()
        time.sleep(1)

        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: View Note Details
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()
        time.sleep(1)

        self.assertIn("First Note", self.driver.page_source)
        self.assertIn("This is the content of the first note.", self.driver.page_source)

    def test_edit_note(self):
        # Functionalities 6: Edit Note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)

        new_title = "Updated Note"
        new_content = "Updated content."

        self.driver.find_element(By.NAME, 'new_title').clear()
        self.driver.find_element(By.NAME, 'new_title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'new_content').clear()
        self.driver.find_element(By.NAME, 'new_content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        time.sleep(1)

        self.assertIn(new_title, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Delete Note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Second Note').click()
        time.sleep(1)

        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
        time.sleep(1)

        self.assertNotIn("Second Note", self.driver.page_source)

    def test_search_for_note(self):
        # Functionalities 8: Search for Note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        time.sleep(1)

        self.driver.find_element(By.NAME, 'title').send_keys("First Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        self.assertIn("First Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Navigate Back to Dashboard
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)

        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Logout
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
