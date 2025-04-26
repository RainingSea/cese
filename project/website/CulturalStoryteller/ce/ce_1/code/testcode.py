import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8144/')  # Access the login page

    def tearDown(self):
        # Close the web driver and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.get('http://localhost:8144/')  # Ensure we are on the login page
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

    def test_user_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8144/register')
        
        # Enter valid username and password
        self.driver.find_element(By.NAME, 'username').send_keys("new_user")
        self.driver.find_element(By.NAME, 'password').send_keys("new_password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Check if redirected to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8144/register')
        self.driver.find_element(By.NAME, 'username').send_keys("admin")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: Registration failed
        self.assertIn("Registration failed", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        self.login("admin", "admin123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8144/')
        self.login("admin", "wrongpassword")

        # Expectation: Invalid credentials message
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_explore_stories(self):
        # Functionality 3: Explore Stories on the Dashboard Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8144/dashboard')

        # Check if stories are displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the dashboard.")

        # Click on a story title
        stories[0].click()
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Functionality 5: View Story Details
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8144/dashboard')
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        stories[0].click()

        # Check if the story details page is displayed
        self.assertIn("Story Details", self.driver.title)
        self.assertIn("The Tale of Two Cities", self.driver.page_source)  # Example story

    def test_bookmark_story(self):
        # Functionality 6: Bookmark Stories
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8144/dashboard')
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        stories[0].click()

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks').click()

        # Verify that the story is bookmarked
        self.driver.get('http://localhost:8144/bookmarks')
        self.assertIn("The Tale of Two Cities", self.driver.page_source)

    def test_view_bookmarked_stories(self):
        # Functionality 7: View and Manage Bookmarked Stories
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8144/bookmarks')

        # Check if bookmarked stories are displayed
        self.assertIn("The Tale of Two Cities", self.driver.page_source)

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
