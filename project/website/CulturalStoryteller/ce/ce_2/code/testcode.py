import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8145/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_registration(self):
        # Functionality 1: User Registration
        self.driver.get('http://localhost:8145/register')  # Navigate to registration page
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for redirection

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.get('http://localhost:8145/register')
        self.driver.find_element(By.NAME, 'username').send_keys("user1")  # Existing username
        self.driver.find_element(By.NAME, 'password').send_keys("password")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for redirection

        # Check for error message (not implemented in the codebase, so we fail the test)
        self.fail("Error message for existing username not implemented.")

    def test_login(self):
        # Functionality 2: User Login
        self.login("user1", "user123")  # Valid credentials
        self.assertIn("Dashboard", self.driver.title)

        # Attempt to login with invalid credentials
        self.driver.get('http://localhost:8145/')
        self.login("user1", "wrongpassword")  # Invalid password
        time.sleep(1)  # Wait for error message
        self.fail("Error message for invalid credentials not implemented.")

    def test_explore_stories(self):
        # Functionality 3: Explore Stories on the Dashboard Page
        self.login("user1", "user123")  # Valid login
        self.assertIn("Stories", self.driver.page_source)

        # Click on a story title
        self.driver.find_element(By.LINK_TEXT, "The Tortoise and the Hare").click()
        time.sleep(1)  # Wait for the story details page to load
        self.assertIn("The Tortoise and the Hare", self.driver.title)

    def test_search_stories(self):
        # Functionality 4: Search for Stories
        self.login("user1", "user123")  # Valid login
        search_box = self.driver.find_element(By.ID, 'search')
        search_box.send_keys("Tortoise")
        search_box.submit()
        time.sleep(1)  # Wait for search results
        self.assertIn("The Tortoise and the Hare", self.driver.page_source)

    def test_view_story_details(self):
        # Functionality 5: View Story Details
        self.login("user1", "user123")  # Valid login
        self.driver.find_element(By.LINK_TEXT, "The Tortoise and the Hare").click()
        time.sleep(1)  # Wait for the story details page to load
        self.assertIn("A classic fable about a race", self.driver.page_source)
        self.assertTrue(self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]'))

    def test_bookmark_stories(self):
        # Functionality 6: Bookmark Stories
        self.login("user1", "user123")  # Valid login
        self.driver.find_element(By.LINK_TEXT, "The Tortoise and the Hare").click()
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()
        time.sleep(1)  # Wait for confirmation
        self.assertIn("Story added to bookmarks!", self.driver.page_source)

    def test_view_and_manage_bookmarked_stories(self):
        # Functionality 7: View and Manage Bookmarked Stories
        self.login("user1", "user123")  # Valid login
        self.driver.get('http://localhost:8145/bookmarks')  # Navigate to bookmarks page
        self.assertIn("Your Bookmarks", self.driver.page_source)

        # Remove a story from bookmarks (not implemented in the codebase, so we fail the test)
        self.fail("Removing bookmarks functionality not implemented.")

    def test_logout(self):
        # Functionality 8: User Logout
        self.login("user1", "user123")  # Valid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for redirection
        self.assertIn("Login", self.driver.title)

if __name__ == '__main__':
    unittest.main()
