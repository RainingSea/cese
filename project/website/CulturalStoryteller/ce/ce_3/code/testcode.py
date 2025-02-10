import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8608/')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8608/register')
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the registration form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8608/register')
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:8608/')
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8608/')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Login", self.driver.title)

    def test_explore_stories_on_dashboard(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Click on a story title
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        self.assertIn("The Tortoise and the Hare", self.driver.title)

    def test_view_story_details(self):
        # Login and navigate to a story details page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()

        # Check for the presence of a 'Bookmark' button
        self.assertTrue(self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]'))

    def test_bookmark_stories(self):
        # Navigate to the Story Details Page and bookmark a story
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()

        # Navigate to the Bookmarks Page
        self.driver.get('http://localhost:8608/bookmarks')
        self.assertIn("Your Bookmarks", self.driver.title)

    def test_view_and_manage_bookmarked_stories(self):
        # Navigate to the Bookmarks Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8608/bookmarks')
        self.assertIn("Your Bookmarks", self.driver.title)

    def test_user_logout(self):
        # Logout from the Dashboard Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
