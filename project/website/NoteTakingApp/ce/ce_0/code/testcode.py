import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8194/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
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
        self.assertIn("Dashboard", self.driver.title)  # Verify redirection to Dashboard

    def test_registration(self):
        # Functionalities 2: Test user registration functionality
        self.driver.get('http://localhost:8194/register')  # Navigate to registration page
        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_notes(self):
        # Functionalities 3: Test viewing notes on the Dashboard
        self.login("admin", "admin123")
        self.assertIn("Your Notes", self.driver.page_source)  # Check if notes are displayed

    def test_add_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()  # Navigate to Add Note page

        note_title = "Test Note"
        note_content = "This is a test note."

        # Fill out the note form
        self.driver.find_element(By.NAME, 'title').send_keys(note_title)
        self.driver.find_element(By.NAME, 'content').send_keys(note_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Save the note

        # Verify that the note appears on the Dashboard
        self.assertIn(note_title, self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Note').click()  # Click on the note to view
        self.assertIn("Test Note", self.driver.title)  # Check if the note title is displayed
        self.assertIn("This is a test note.", self.driver.page_source)  # Check if the content is displayed

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Note').click()  # Click on the note to edit
        self.driver.find_element(By.XPATH, '//a[text()="Edit"]').click()  # Click edit

        new_content = "This is the updated content."
        self.driver.find_element(By.NAME, 'content').clear()  # Clear existing content
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)  # Enter new content
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()  # Save changes

        # Verify that the updated content is displayed
        self.assertIn(new_content, self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Note').click()  # Click on the note to delete
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()  # Confirm deletion

        # Verify that the note is no longer present on the Dashboard
        self.assertNotIn("Test Note", self.driver.page_source)

    def test_search_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()  # Navigate to search page

        self.driver.find_element(By.NAME, 'query').send_keys("Test Note")  # Enter search query
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()  # Perform search

        # Verify that the search results contain the note
        self.assertIn("Test Note", self.driver.page_source)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()  # Click logout

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
