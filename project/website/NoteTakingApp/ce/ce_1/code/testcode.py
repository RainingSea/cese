import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web app to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8174')

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "password123")
        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
        # Assuming a registration page exists, which is not implemented in the codebase
        self.fail("Registration functionality not implemented")

    def test_view_notes_on_dashboard(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("admin", "password123")
        # Verify that the Dashboard Page shows notes
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        time.sleep(1)  # Wait for the Add Note Page to load

        note_title = "Test Note"
        note_content = "This is a test note."

        # Fill out the new note form
        self.driver.find_element(By.ID, 'title').send_keys(note_title)
        self.driver.find_element(By.ID, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Note"]').click()
        time.sleep(1)  # Wait for the note to be saved

        # Verify that the new note is displayed on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the View Note Page to load

        # Verify that the note details are displayed
        self.assertIn("View Note", self.driver.title)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the View Note Page to load

        new_title = "Updated Note Title"
        new_content = "Updated content of the note."

        # Edit the note
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys(new_title)
        self.driver.find_element(By.ID, 'content').clear()
        self.driver.find_element(By.ID, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        time.sleep(1)  # Wait for the changes to be saved

        # Verify that the note is updated
        self.assertIn(new_title, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the View Note Page to load

        # Delete the note
        self.driver.find_element(By.XPATH, '//button[text()="Delete Note"]').click()
        time.sleep(1)  # Wait for the note to be deleted

        # Verify that the note is no longer displayed on the Dashboard
        self.assertNotIn("Test Note", self.driver.page_source)

    def test_search_for_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the Search Note Page to load

        search_query = "First Note"
        self.driver.find_element(By.ID, 'query').send_keys(search_query)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results display the matching note
        self.assertIn(search_query, self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the Dashboard
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the Search Note Page to load

        # Navigate back to the Dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the Dashboard Page to load

        # Verify that the user is back on the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "password123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the Login Page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
