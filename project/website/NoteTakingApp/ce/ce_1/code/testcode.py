import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8359/')  # Access the login page

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
        self.driver.get('http://localhost:8359/register')  # Navigate to registration page
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

    def test_view_notes(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)
        notes = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(notes), 0, "No notes found on the dashboard.")

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        self.driver.find_element(By.NAME, 'title').send_keys("Test Note")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a test note.")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Verify that the note appears on the dashboard
        self.assertIn("Test Note", self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()  # Assuming "First Note" exists
        self.assertIn("Edit Note", self.driver.title)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()  # Assuming "First Note" exists
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys("Updated Note Title")
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys("Updated content.")
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        
        # Verify that the updated note is displayed
        self.assertIn("Updated Note Title", self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'First Note').click()  # Assuming "First Note" exists
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
        
        # Verify that the note is deleted
        self.assertNotIn("First Note", self.driver.page_source)

    def test_search_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        self.driver.find_element(By.NAME, 'query').send_keys("First Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify that the search results display the matching note
        self.assertIn("First Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Note').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        
        # Verify that the dashboard is displayed
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        
        # Verify that the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
