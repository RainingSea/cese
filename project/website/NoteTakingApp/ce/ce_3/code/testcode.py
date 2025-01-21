import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8959/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the process
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
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
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

    def test_view_notes_on_dashboard(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows notes
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the Dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "admin123")

        # Navigate to Add Note Page
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        time.sleep(1)  # Wait for the next page to load

        note_title = "Test Note"
        note_content = "This is a test note."

        # Fill out the new note form
        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Add Note"]').click()
        time.sleep(1)  # Wait for saving the note

        # Verify that the new note is displayed on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")

        # Click on a note to view details
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the View Note Page displays the note's title and content
        self.assertIn("First Note", self.driver.page_source)
        self.assertIn("This is the content of the first note.", self.driver.page_source)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")

        # Navigate to a note and edit it
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()
        time.sleep(1)  # Wait for the next page to load

        new_content = "Updated content for the first note."
        textarea = self.driver.find_element(By.NAME, 'content')
        textarea.clear()
        textarea.send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Edit Note"]').click()
        time.sleep(1)  # Wait for the update

        # Verify that the note content is updated
        self.assertIn(new_content, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.fail("Delete note functionality not implemented")

    def test_search_for_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")

        # Navigate to Search Note Page
        self.driver.get('http://localhost:8959/search_note')
        time.sleep(1)  # Wait for the next page to load

        # Perform a search
        self.driver.find_element(By.NAME, 'query').send_keys("First Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results display the matching note
        self.assertIn("First Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the Dashboard
        self.login("admin", "admin123")

        # Navigate to Search Note Page and then back to Dashboard
        self.driver.get('http://localhost:8959/search_note')
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the Dashboard to load

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.fail("Logout functionality not implemented")

if __name__ == '__main__':
    unittest.main()
