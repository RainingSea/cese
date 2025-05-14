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
        # Give the server time to start
        time.sleep(2)
        
    @classmethod
    def tearDownClass(cls):
        # Stop the Flask application
        cls.process.terminate()
        cls.process.wait()

    def setUp(self):
        # Initialize the webdriver
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8096/login')
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # Close the browser
        self.driver.quit()

    def login(self, username, password):
        """Helper method to perform login"""
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        # Wait for dashboard to load
        self.wait.until(EC.title_contains('Dashboard'))

    def test_1_user_login(self):
        """Functionalities 1: Test user login with valid credentials"""
        self.login("testuser", "testpass")
        self.assertIn('Dashboard', self.driver.title)
        self.assertIn('Welcome, testuser!', self.driver.page_source)

    def test_2_user_registration(self):
        """Functionalities 2: Test user registration"""
        # Go to registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.wait.until(EC.title_contains('Register'))
        
        # Fill registration form
        username = "newuser"
        password = "newpass123"
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.NAME, 'confirm').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        
        # Verify redirection to dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn('Welcome, newuser!', self.driver.page_source)

    def test_3_view_notes_on_dashboard(self):
        """Functionalities 3: Test viewing notes on dashboard"""
        self.login("testuser", "testpass")
        
        # Check if notes are displayed
        notes = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(notes), 0, "No notes found on dashboard")
        
        # Verify sample notes exist
        note_titles = [note.text for note in notes]
        self.assertIn('Welcome Note', note_titles)
        self.assertIn('Sample Note', note_titles)

    def test_4_add_new_note(self):
        """Functionalities 4: Test adding a new note"""
        self.login("testuser", "testpass")
        
        # Go to add note page
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        self.wait.until(EC.title_contains('Add Note'))
        
        # Fill note form
        title = "Test Note " + str(int(time.time()))
        content = "This is a test note created by automated tests."
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'content').send_keys(content)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Verify redirection to dashboard and note appears
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn(title, self.driver.page_source)

    def test_5_view_note_details(self):
        """Functionalities 5: Test viewing note details"""
        self.login("testuser", "testpass")
        
        # Click on first note
        first_note = self.driver.find_element(By.XPATH, '//ul/li/a')
        note_title = first_note.text
        first_note.click()
        
        # Verify note details page
        self.wait.until(EC.title_contains(note_title))
        self.assertIn(note_title, self.driver.page_source)
        # Check if content is displayed
        content = self.driver.find_element(By.TAG_NAME, 'p').text
        self.assertTrue(len(content) > 0, "Note content not displayed")

    def test_6_edit_note(self):
        """Functionalities 6: Test editing a note"""
        self.login("testuser", "testpass")
        
        # Go to first note's details
        first_note = self.driver.find_element(By.XPATH, '//ul/li/a')
        note_title = first_note.text
        first_note.click()
        self.wait.until(EC.title_contains(note_title))
        
        # Click edit button
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        self.wait.until(EC.title_contains('Edit'))
        
        # Edit note
        new_title = "Edited " + note_title
        new_content = "This note has been edited by automated tests."
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        
        # Verify changes
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn(new_title, self.driver.page_source)

    def test_7_delete_note(self):
        """Functionalities 7: Test deleting a note"""
        self.login("testuser", "testpass")
        
        # First add a note to delete
        self.driver.find_element(By.LINK_TEXT, 'Add Note').click()
        self.wait.until(EC.title_contains('Add Note'))
        title = "Note to Delete " + str(int(time.time()))
        self.driver.find_element(By.NAME, 'title').send_keys(title)
        self.driver.find_element(By.NAME, 'content').send_keys("This note will be deleted.")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        self.wait.until(EC.title_contains('Dashboard'))
        
        # Now delete the note
        note_link = self.driver.find_element(By.LINK_TEXT, title)
        note_link.click()
        self.wait.until(EC.title_contains(title))
        self.driver.find_element(By.LINK_TEXT, 'Delete').click()
        
        # Verify note is gone
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertNotIn(title, self.driver.page_source)

    def test_8_search_for_note(self):
        """Functionalities 8: Test searching for notes"""
        self.login("testuser", "testpass")
        
        # Go to search page
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        self.wait.until(EC.title_contains('Search Notes'))
        
        # Search for "Welcome"
        self.driver.find_element(By.NAME, 'query').send_keys('Welcome')
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        
        # Verify results
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//h2[contains(text(), "Results for")]')))
        results = self.driver.find_elements(By.XPATH, '//ul/li/a')
        self.assertGreater(len(results), 0, "No search results found")
        self.assertIn('Welcome Note', [r.text for r in results])

    def test_9_navigate_back_to_dashboard(self):
        """Functionalities 9: Test navigating back to dashboard"""
        self.login("testuser", "testpass")
        
        # Go to search page
        self.driver.find_element(By.LINK_TEXT, 'Search Notes').click()
        self.wait.until(EC.title_contains('Search Notes'))
        
        # Click back to dashboard
        self.driver.find_element(By.LINK_TEXT, 'Back to Dashboard').click()
        
        # Verify we're back on dashboard
        self.wait.until(EC.title_contains('Dashboard'))
        self.assertIn('Welcome, testuser!', self.driver.page_source)

    def test_10_logout(self):
        """Functionalities 10: Test logout functionality"""
        self.login("testuser", "testpass")
        
        # Click logout
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        
        # Verify we're back on login page
        self.wait.until(EC.title_contains('Login'))
        self.assertIn('Don\'t have an account?', self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
