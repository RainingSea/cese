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
        self.driver.get('http://localhost:8605/') 

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
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit the registration form
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register here').click()
        time.sleep(1)  # Wait for the next page to load
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that an error message is displayed
        self.assertIn("Register", self.driver.title)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8605/') 
        self.login("invalid_user", "invalid_pass")

        # Verify that an error message is displayed
        self.assertIn("Login", self.driver.title)

    def test_explore_stories_on_dashboard(self):
        # Login successfully and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify that a collection of stories is displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the Dashboard.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the user is redirected to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Login and navigate to a story details page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Story Details Page is displayed
        self.assertIn("The Tortoise and the Hare", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        bookmark_button = self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]')
        self.assertIsNotNone(bookmark_button)

    def test_bookmark_stories(self):
        # Login and navigate to a story details page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)  # Wait for the next page to load

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.XPATH, '//button[text()="Add to Bookmarks"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Navigate to the Bookmarks Page
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the bookmarked story is listed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

    def test_view_and_manage_bookmarked_stories(self):
        # Login and navigate to the Bookmarks Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the list of bookmarked stories is displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Remove a story from bookmarks (not implemented in the codebase)
        self.fail("Remove bookmark functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Logout from the Dashboard Page (not implemented in the codebase)
        self.fail("Logout functionality not implemented")

    def test_local_data_storage(self):
        # Add a new story to the local storage (not implemented in the codebase)
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
