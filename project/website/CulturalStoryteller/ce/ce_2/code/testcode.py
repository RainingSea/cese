import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8607/login')

    def tearDown(self):
        # Close the web driver session and stop the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify error message for existing username
        self.assertIn("User already exists!", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8607/login')
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
        time.sleep(1)  # Wait for the Story Details Page to load

        # Verify redirection to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a story title
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)  # Wait for the Story Details Page to load

        # Verify the Story Details Page is displayed
        self.assertIn("The Tortoise and the Hare", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        self.assertIn("Add to Bookmarks", self.driver.page_source)

    def test_bookmark_stories(self):
        # Login and navigate to the Story Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)  # Wait for the Story Details Page to load

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the story is added to bookmarks
        self.assertIn("Story added to bookmarks!", self.driver.page_source)

        # Navigate to the Bookmarks Page
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the Bookmarks Page to load

        # Verify the bookmarked story is listed
        self.assertIn("The Tortoise and the Hare", self.driver.page_source)

    def test_view_and_manage_bookmarked_stories(self):
        # Login and navigate to the Bookmarks Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the Bookmarks Page to load

        # Verify the list of bookmarked stories is displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Remove a story from bookmarks
        self.driver.find_element(By.LINK_TEXT, 'Remove').click()
        time.sleep(1)  # Wait for the confirmation message

        # Verify the story is removed from bookmarks
        self.assertIn("Story removed from bookmarks!", self.driver.page_source)

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the Login Page to load

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8607/dashboard')
        time.sleep(1)  # Wait for the redirection

        # Verify redirection back to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality is not implemented in the codebase
        self.fail("Functionality not implemented")

if __name__ == '__main__':
    unittest.main()
