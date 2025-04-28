import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8358/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_notes(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("user1", "user123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()

        note_title = "Test Note"
        note_content = "This is a test note."

        # Fill out the new note form
        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()

        # Verify that the new note is displayed on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("user1", "user123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        if notes:
            notes[0].find_element(By.TAG_NAME, 'a').click()  # Click on the first note

            # Verify that the note details are displayed
            self.assertIn("Test Note", self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("user1", "user123")
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        if notes:
            delete_link = notes[0].find_elements(By.TAG_NAME, 'a')[1]  # Click on the delete link
            delete_link.click()

            # Verify that the note is deleted and no longer appears in the dashboard
            self.assertNotIn("Test Note", self.driver.page_source)

    def test_search_note(self):
        # Functionalities 8: Test searching for a note
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()

        search_title = "First Note"
        self.driver.find_element(By.NAME, 'title').send_keys(search_title)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results display the matching note
        self.assertIn(search_title, self.driver.page_source)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
