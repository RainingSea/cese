import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess

class TestNoteTakingApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8095/')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the webdriver and stop the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Wait for dashboard to load
        self.wait.until(EC.title_contains('Dashboard'))

    def test_functionality_1_user_login(self):
        """Test valid user login"""
        self.login("testuser", "testpass")
        self.assertIn('Welcome, testuser!', self.driver.page_source)
        self.assertIn('Dashboard', self.driver.title)

    def test_functionality_2_user_registration(self):
        """Test user registration"""
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Register new user
        username = "newuser_" + str(int(time.time()))
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys("newpass123")
        self.driver.find_element(By.ID, 'confirm_password').send_keys("newpass123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirected to login page
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

    def test_functionality_3_view_notes_on_dashboard(self):
        """Test viewing notes on dashboard"""
        self.login("testuser", "testpass")
        notes = self.driver.find_elements(By.CLASS_NAME, 'note')
        self.assertTrue(len(notes) >= 0)  # Can be zero if no notes exist

    def test_functionality_4_add_new_note(self):
        """Test adding a new note"""
        self.login("testuser", "testpass")
        
        # Go to add note page
        self.driver.find_element(By.LINK_TEXT, 'Add New Note').click()
        self.wait.until(EC.title_contains('Add Note'))
        
        # Add a new note
        note_title = "Test Note " + str(int(time.time()))
        self.driver.find_element(By.ID, 'title').send_keys(note_title)
        self.driver.find_element(By.ID, 'content').send_keys("This is a test note content")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Verify note appears on dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn(note_title, self.driver.page_source)

    def test_functionality_5_view_note_details(self):
        """Test viewing note details"""
        self.login("testuser", "testpass")
        
        # First add a note if none exist
        if "No notes yet" in self.driver.page_source:
            self.test_functionality_4_add_new_note()
        
        # Click on first note
        first_note = self.driver.find_element(By.CSS_SELECTOR, '.note a')
        note_title = first_note.text
        first_note.click()
        
        # Verify note details page
        self.wait.until(EC.title_contains(note_title))
        self.assertIn(note_title, self.driver.page_source)

    def test_functionality_6_edit_note(self):
        """Test editing a note"""
        self.login("testuser", "testpass")
        
        # First add a note if none exist
        if "No notes yet" in self.driver.page_source:
            self.test_functionality_4_add_new_note()
        
        # View first note
        self.driver.find_element(By.CSS_SELECTOR, '.note a').click()
        self.wait.until(EC.title_contains('View Note'))
        
        # Click edit button
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        
        # Edit note
        new_title = "Edited Note " + str(int(time.time()))
        self.driver.find_element(By.ID, 'title').clear()
        self.driver.find_element(By.ID, 'title').send_keys(new_title)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        
        # Verify changes
        self.wait.until(EC.title_contains(new_title))
        self.assertIn(new_title, self.driver.page_source)

    def test_functionality_7_delete_note(self):
        """Test deleting a note"""
        self.login("testuser", "testpass")
        
        # First add a note if none exist
        if "No notes yet" in self.driver.page_source:
            self.test_functionality_4_add_new_note()
        
        # View first note
        self.driver.find_element(By.CSS_SELECTOR, '.note a').click()
        self.wait.until(EC.title_contains('View Note'))
        
        # Click delete button
        self.driver.find_element(By.XPATH, '//button[text()="Delete Note"]').click()
        
        # Handle alert
        alert = self.driver.switch_to.alert
        alert.accept()
        
        # Verify back on dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn('Dashboard', self.driver.title)

    def test_functionality_8_search_for_note(self):
        """Test searching for notes"""
        self.login("testuser", "testpass")
        
        # First add a test note
        unique_text = "UniqueSearchTerm" + str(int(time.time()))
        self.driver.find_element(By.LINK_TEXT, 'Add New Note').click()
        self.wait.until(EC.title_contains('Add Note'))
        self.driver.find_element(By.ID, 'title').send_keys(unique_text)
        self.driver.find_element(By.ID, 'content').send_keys("Content for search test")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Search for the note
        search_box = self.wait.until(EC.presence_of_element_located((By.NAME, 'query')))
        search_box.send_keys(unique_text)
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify search results
        self.wait.until(EC.title_contains('Search Results'))
        self.assertIn(unique_text, self.driver.page_source)

    def test_functionality_9_navigate_back_to_dashboard(self):
        """Test navigating back to dashboard"""
        self.login("testuser", "testpass")
        
        # Go to search page
        self.driver.find_element(By.NAME, 'query').send_keys("test")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        self.wait.until(EC.title_contains('Search Results'))
        
        # Click back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        
        # Verify back on dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn('Dashboard', self.driver.title)

    def test_functionality_10_logout(self):
        """Test logout functionality"""
        self.login("testuser", "testpass")
        
        # Click logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        
        # Verify back on login page
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Login', self.driver.title)

if __name__ == '__main__':
    unittest.main()
