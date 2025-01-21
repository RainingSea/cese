import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9010/')  # Navigate to the login page

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

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:9010/register')
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:9010/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Check for error message (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9010/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)

    def test_explore_stories_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Verify stories are displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the Dashboard.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Login and navigate to a story details page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Lion and the Mouse').click()
        time.sleep(1)

        # Verify story details are displayed
        self.assertIn("The Lion and the Mouse", self.driver.page_source)

        # Check for 'Bookmark' button
        bookmark_button = self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]')
        self.assertIsNotNone(bookmark_button)

    def test_bookmark_stories(self):
        # Login and navigate to a story details page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Lion and the Mouse').click()
        time.sleep(1)

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()
        time.sleep(1)

        # Navigate to the Bookmarks Page
        self.driver.get('http://localhost:9010/bookmarks')
        self.assertIn("The Lion and the Mouse", self.driver.page_source)

    def test_view_and_manage_bookmarked_stories(self):
        # Login and navigate to the Bookmarks Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:9010/bookmarks')
        self.assertIn("Bookmarks", self.driver.title)

        # Verify bookmarked stories are displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Remove a story from bookmarks (not implemented in codebase)
        self.fail("Remove bookmark functionality not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9010/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Add a new story to local storage (not implemented in codebase)
        self.fail("Add new story to local storage functionality not implemented")

        # Bookmark a story and check the corresponding text file
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Lion and the Mouse').click()
        self.driver.find_element(By.XPATH, '//button[text()="Bookmark"]').click()
        time.sleep(1)

        # Verify the story's details are saved in the bookmarks text file
        with open('bookmarks.txt', 'r') as f:
            bookmarks = f.read()
            self.assertIn("admin|The Lion and the Mouse", bookmarks)

if __name__ == '__main__':
    unittest.main()
