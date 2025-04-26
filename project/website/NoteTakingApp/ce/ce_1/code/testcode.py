import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8195/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        self.login("admin", "admin123")
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(notes), 0, "No notes found.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()

        note_title = "Test Note"
        note_content = "This is a test note."

        # Fill out the new note form
        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Note"]').click()

        # Verify that the new note is displayed on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        if notes:
            notes[0].click()  # Click the first note
            self.assertIn("View Note", self.driver.title)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        if notes:
            notes[0].click()  # Click the first note
            new_content = "Updated content."
            self.driver.find_element(By.NAME, 'content').clear()
            self.driver.find_element(By.NAME, 'content').send_keys(new_content)
            self.driver.find_element(By.XPATH, '//button[text()="Update Note"]').click()

            # Verify that the updated content is displayed
            self.assertIn(new_content, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "admin123")
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        if notes:
            note_title = notes[0].text
            self.driver.find_element(By.LINK_TEXT, note_title).find_element(By.XPATH, './following-sibling::a').click()  # Click delete
            self.assertNotIn(note_title, self.driver.page_source)

    def test_search_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        search_title = "Test Note"
        self.driver.find_element(By.NAME, 'title').send_keys(search_title)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()

        # Verify that the search results display the matching note(s)
        self.assertIn(search_title, self.driver.page_source)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
