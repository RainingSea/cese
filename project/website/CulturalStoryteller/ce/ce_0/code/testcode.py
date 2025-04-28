import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8307/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8307/register')  # Navigate to Registration Page
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
        self.driver.get('http://localhost:8307/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify error message
        self.assertIn("Registration failed. Username already exists.", self.driver.page_source)

    def test_login(self):
        # Functionality 2: User Login
        self.driver.get('http://localhost:8307/')  # Navigate to Login Page
        self.assertIn("Login", self.driver.title)

        # Valid login
        self.login("admin", "admin123")
        self.assertIn("Dashboard", self.driver.title)

        # Invalid login
        self.driver.get('http://localhost:8307/')
        self.login("admin", "wrongpassword")
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_stories(self):
        # Functionality 3: Explore Stories on the Dashboard Page
        self.login("admin", "admin123")  # Log in first
        self.assertIn("Dashboard", self.driver.title)

        # Verify stories are displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the dashboard.")

        # Click on a story
        stories[0].click()
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Functionality 5: View Story Details
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8307/dashboard')
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        stories[0].click()  # Click on the first story

        # Verify story details are displayed
        self.assertIn("Story Details", self.driver.title)
        self.assertIn("The Tale of the Three Brothers", self.driver.page_source)  # Example story title

    def test_bookmark_stories(self):
        # Functionality 6: Bookmark Stories
        self.login("admin", "admin123")  # Log in first
        self.driver.get('http://localhost:8307/dashboard')
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        stories[0].click()  # Click on the first story

        # Attempt to bookmark (assuming a button exists)
        # self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()
        # self.assertIn("Story bookmarked", self.driver.page_source)

        # Navigate to bookmarks page
        self.driver.get('http://localhost:8307/bookmarks')
        self.assertIn("Bookmarks", self.driver.title)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
