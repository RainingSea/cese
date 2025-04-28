import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session and the application
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'confirm_password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        self.assertIn("Login", self.driver.title)

    def test_view_notes(self):
        # Functionalities 3: Test viewing notes on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Your Notes", self.driver.page_source)

    def test_add_new_note(self):
        # Functionalities 4: Test adding a new note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        self.driver.find_element(By.ID, 'title').send_keys("Test Note")
        self.driver.find_element(By.ID, 'content').send_keys("This is a test note.")
        self.driver.find_element(By.XPATH, '//button[text()="Save Note"]').click()
        self.assertIn("Test Note", self.driver.page_source)

    def test_view_note_details(self):
        # Functionalities 5: Test viewing note details
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Note').click()  # Assuming the note title is clickable
        self.assertIn("Test Note", self.driver.page_source)

    def test_edit_note(self):
        # Functionalities 6: Test editing a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Test Note').click()
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys("Updated Test Note")
        self.driver.find_element(By.XPATH, '//button[text()="Save Note"]').click()
        self.assertIn("Updated Test Note", self.driver.page_source)

    def test_delete_note(self):
        # Functionalities 7: Test deleting a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Updated Test Note').click()
        self.driver.find_element(By.LINK_TEXT, 'Delete').click()
        self.assertNotIn("Updated Test Note", self.driver.page_source)

    def test_search_note(self):
        # Functionalities 8: Test searching for a note
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        self.driver.find_element(By.ID, 'search').send_keys("Test Note")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.assertIn("Test Note", self.driver.page_source)

    def test_navigate_back_to_dashboard(self):
        # Functionalities 9: Test navigating back to the Dashboard
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        self.assertIn("Dashboard", self.driver.title)

    def test_logout(self):
        # Functionalities 10: Test logging out
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
