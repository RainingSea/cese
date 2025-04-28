import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8308/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8308/register')  # Navigate to Registration Page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "test_user"
        new_password = "test_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8308/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message for existing username
        self.assertIn("Username already taken", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")  # Valid credentials

        # Verify redirection to Dashboard
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8308/')
        self.login("admin", "wrongpassword")  # Invalid password

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_stories(self):
        # Functionality 3: Explore Stories on the Dashboard Page
        self.login("admin", "admin123")  # Valid login
        self.assertIn("Dashboard", self.driver.title)

        # Verify stories are displayed
        stories = self.driver.find_elements(By.XPATH, '//li/a')
        self.assertGreater(len(stories), 0, "No stories found.")

        # Click on a story title
        stories[0].click()
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Functionality 5: View Story Details
        self.login("admin", "admin123")  # Valid login
        self.driver.get('http://localhost:8308/dashboard')
        stories = self.driver.find_elements(By.XPATH, '//li/a')
        stories[0].click()  # Click on the first story

        # Verify story details are displayed
        self.assertIn("The Tortoise and the Hare", self.driver.page_source)
        self.assertIn("Cultural Origin:", self.driver.page_source)

    def test_bookmark_story(self):
        # Functionality 6: Bookmark Stories
        self.login("admin", "admin123")  # Valid login
        self.driver.get('http://localhost:8308/story/The Tortoise and the Hare')
        
        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()

        # Verify bookmark confirmation (assuming a confirmation message appears)
        self.assertIn("Story added to bookmarks", self.driver.page_source)

    def test_view_bookmarks(self):
        # Functionality 7: View and Manage Bookmarked Stories
        self.login("admin", "admin123")  # Valid login
        self.driver.get('http://localhost:8308/bookmarks')

        # Verify bookmarks are displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

    def test_user_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Valid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
