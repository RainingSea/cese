import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the server to start
        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:9011/login')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password, then submit
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.driver.get('http://localhost:9011/login')
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9011/login')
        self.login("invalid_user", "invalid_pass")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_explore_stories_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify stories are displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_search_for_stories(self):
        # This functionality is not implemented in the codebase
        self.fail("Search functionality not implemented")

    def test_view_story_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a story title
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Story Details Page is displayed
        self.assertIn("Story Details", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        bookmark_button = self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]')
        self.assertIsNotNone(bookmark_button)

    def test_bookmark_stories(self):
        # This functionality is not implemented in the codebase
        self.fail("Bookmark functionality not implemented")

    def test_view_and_manage_bookmarked_stories(self):
        # This functionality is not implemented in the codebase
        self.fail("Bookmark management functionality not implemented")

    def test_user_logout(self):
        # This functionality is not implemented in the codebase
        self.fail("Logout functionality not implemented")

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
