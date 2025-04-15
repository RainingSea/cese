import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8315/')

    def tearDown(self):
        # Close the web driver session and stop the application
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

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_user_registration(self):
        # Functionalities 2: Test user registration functionality
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

    def test_view_notes_on_dashboard(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("admin", "admin123")

        # Verify that the Dashboard Page shows notes
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

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
        time.sleep(1)  # Wait for the note to be added

        # Verify that the new note is displayed on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")

        # Click on the first note's view button
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the View Note Page to load

        # Verify that the note's title and content are displayed
        self.assertIn("First Note", self.driver.page_source)
        self.assertIn("This is the content of the first note.", self.driver.page_source)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")

        # Click on the first note's view button
        self.driver.find_element(By.LINK_TEXT, 'View').click()
        time.sleep(1)  # Wait for the View Note Page to load

        # Edit the note content
        new_content = "Updated content for the first note."
        content_field = self.driver.find_element(By.NAME, 'content')
        content_field.clear()
        content_field.send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        time.sleep(1)  # Wait for the note to be updated

        # Verify that the updated content is displayed
        self.assertIn(new_content, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "admin123")

        # Click on the first note's delete button
        self.driver.find_element(By.LINK_TEXT, 'Delete').click()
        time.sleep(1)  # Wait for the note to be deleted

        # Verify that the note is no longer displayed on the Dashboard
        self.assertNotIn("First Note", self.driver.page_source)

    def test_search_for_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")

        # Navigate to Search Note Page
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the Search Note Page to load

        # Search for a note
        self.driver.find_element(By.NAME, 'query').send_keys("First Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify that the search results display the matching note
        self.assertIn("First Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the Dashboard
        self.login("admin", "admin123")

        # Navigate to Search Note Page
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        time.sleep(1)  # Wait for the Search Note Page to load

        # Click the back to Dashboard link
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        time.sleep(1)  # Wait for the Dashboard Page to load

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
