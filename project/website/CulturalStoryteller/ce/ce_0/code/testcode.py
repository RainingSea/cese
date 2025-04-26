import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8143/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8143/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8143/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify that an error message is displayed
        self.assertIn("Username already taken", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8143/')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_stories(self):
        # Functionality 3: Explore Stories on the Dashboard Page
        self.login("admin", "admin123")
        self.assertIn("Stories", self.driver.page_source)

        # Click on a story title
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click the first story
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Functionality 5: View Story Details
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click the first story
        self.assertIn("Story Details", self.driver.title)
        self.assertIn("Add to Bookmarks", self.driver.page_source)

    def test_bookmark_story(self):
        # Functionality 6: Bookmark Stories
        self.login("admin", "admin123")
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click the first story
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()

        # Verify that the story is added to bookmarks
        self.driver.get('http://localhost:8143/bookmarks')
        self.assertIn("Your Bookmarks", self.driver.title)
        self.assertIn("Story 1 Title", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8143/dashboard')
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
