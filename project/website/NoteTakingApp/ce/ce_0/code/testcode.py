import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start the Flask application
        cls.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8094/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver session
        self.driver.quit()

    def login(self, username="testuser", password="testpass"):
        """Helper method to perform login"""
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        self.wait.until(EC.title_contains("Dashboard"))

    def test_1_user_login(self):
        """Functionalities 1: Test user login with valid credentials"""
        # Register a test user first
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()
        self.driver.find_element(By.ID, 'username').send_keys("testuser")
        self.driver.find_element(By.ID, 'password').send_keys("testpass")
        self.driver.find_element(By.ID, 'confirm_password').send_keys("testpass")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Now test login
        self.login()
        self.assertIn("Dashboard", self.driver.title)

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration"""
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register").click()
        self.driver.find_element(By.ID, 'username').send_keys("newuser")
        self.driver.find_element(By.ID, 'password').send_keys("newpass")
        self.driver.find_element(By.ID, 'confirm_password').send_keys("newpass")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirection to login page
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

    def test_3_view_notes_on_dashboard(self):
        """Functionalities 3: Test viewing notes on dashboard"""
        self.login()
        notes = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertTrue(len(notes) >= 0)  # Can be empty if no notes

    def test_4_add_new_note(self):
        """Functionalities 4: Test adding a new note"""
        self.login()
        self.driver.find_element(By.LINK_TEXT, "Add Note").click()
        
        # Fill out the form
        self.driver.find_element(By.ID, 'title').send_keys("Test Note Title")
        self.driver.find_element(By.ID, 'content').send_keys("Test Note Content")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Verify redirection to dashboard and note appears
        self.wait.until(EC.title_contains("Dashboard"))
        self.assertIn("Test Note Title", self.driver.page_source)

    def test_5_view_note_details(self):
        """Functionalities 5: Test viewing note details"""
        self.login()
        # First add a note if none exists
        if "You don't have any notes yet" in self.driver.page_source:
            self.test_4_add_new_note()
        
        # Click on the first note
        note_link = self.driver.find_element(By.CLASS_NAME, 'list-group-item')
        note_link.click()
        
        # Verify we're on the view note page
        self.wait.until(EC.title_contains("Test Note Title"))
        self.assertIn("Test Note Content", self.driver.page_source)

    def test_6_edit_note(self):
        """Functionalities 6: Test editing a note"""
        self.login()
        # First add a note if none exists
        if "You don't have any notes yet" in self.driver.page_source:
            self.test_4_add_new_note()
        
        # Click on the first note
        note_link = self.driver.find_element(By.CLASS_NAME, 'list-group-item')
        note_link.click()
        
        # Click edit button and modify the note
        self.driver.find_element(By.XPATH, '//button[text()="Edit"]').click()
        title_field = self.driver.find_element(By.ID, 'title')
        title_field.clear()
        title_field.send_keys("Edited Note Title")
        content_field = self.driver.find_element(By.ID, 'content')
        content_field.clear()
        content_field.send_keys("Edited Note Content")
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        
        # Verify changes were saved
        self.wait.until(EC.title_contains("Edited Note Title"))
        self.assertIn("Edited Note Content", self.driver.page_source)

    def test_7_delete_note(self):
        """Functionalities 7: Test deleting a note"""
        self.login()
        # First add a note if none exists
        if "You don't have any notes yet" in self.driver.page_source:
            self.test_4_add_new_note()
        
        # Click on the first note
        note_link = self.driver.find_element(By.CLASS_NAME, 'list-group-item')
        note_link.click()
        
        # Click delete button and confirm
        self.driver.find_element(By.XPATH, '//button[text()="Delete"]').click()
        self.driver.switch_to.alert.accept()
        
        # Verify redirection to dashboard
        self.wait.until(EC.title_contains("Dashboard"))
        self.assertNotIn("Edited Note Title", self.driver.page_source)

    def test_8_search_for_note(self):
        """Functionalities 8: Test searching for a note"""
        self.login()
        # First add a test note if none exists
        if "You don't have any notes yet" in self.driver.page_source:
            self.test_4_add_new_note()
        
        # Search for the note
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("Test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify search results
        self.wait.until(EC.title_contains("Search Results"))
        self.assertIn("Test Note Title", self.driver.page_source)

    def test_9_navigate_back_to_dashboard(self):
        """Functionalities 9: Test navigating back to dashboard"""
        self.login()
        # Go to search page first
        search_box = self.driver.find_element(By.NAME, 'query')
        search_box.send_keys("Test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Click back to dashboard link
        self.driver.find_element(By.LINK_TEXT, "Back to Dashboard").click()
        
        # Verify we're back on dashboard
        self.wait.until(EC.title_contains("Dashboard"))
        self.assertIn("Your Notes", self.driver.page_source)

    def test_10_logout(self):
        """Functionalities 10: Test logout functionality"""
        self.login()
        # Click logout button
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        
        # Verify we're back on login page
        self.wait.until(EC.title_contains("Login"))
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
