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
        self.driver.get('http://localhost:9013/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the application
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
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify an error message is displayed
        self.assertIn("Register", self.driver.title)  # Assuming the page doesn't change on error

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:9013/')  # Navigate back to the login page
        self.login("invalid_user", "invalid_pass")

        # Verify an error message is displayed
        self.assertIn("Login", self.driver.title)  # Assuming the page doesn't change on error

    def test_explore_stories_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify a collection of stories is displayed
        stories = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(stories), 0, "No stories found on the Dashboard.")

        # Click on a story title
        stories[0].click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_search_for_stories(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Enter a keyword in the search bar and submit
        # Assuming there's a search bar element with name 'search'
        self.driver.find_element(By.NAME, 'search').send_keys("Lion")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)  # Wait for the search results

        # Verify a list of stories matching the keyword is displayed
        search_results = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(search_results), 0, "No search results found.")

    def test_view_story_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a story title
        stories = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        stories[0].click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the Story Details Page is displayed
        self.assertIn("Story Details", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        bookmark_button = self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks')
        self.assertIsNotNone(bookmark_button, "Bookmark button not found.")

    def test_bookmark_stories(self):
        # Login and navigate to a Story Details Page
        self.login("admin", "admin123")
        stories = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        stories[0].click()
        time.sleep(1)  # Wait for the next page to load

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks').click()
        time.sleep(1)  # Wait for the action to complete

        # Navigate to the Bookmarks Page
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the bookmarked story is listed
        bookmarks = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

    def test_view_and_manage_bookmarked_stories(self):
        # Login and navigate to the Bookmarks Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the list of bookmarked stories is displayed
        bookmarks = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Remove a story from bookmarks
        # Assuming there's a remove button for each bookmark
        self.driver.find_element(By.XPATH, '//button[text()="Remove"]').click()
        time.sleep(1)  # Wait for the action to complete

        # Verify the story is removed from the bookmarks list
        bookmarks_after_removal = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertLess(len(bookmarks_after_removal), len(bookmarks), "Bookmark not removed.")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:9013/dashboard')
        time.sleep(1)  # Wait for the redirection

        # Verify access is denied and redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # This functionality requires manual verification of the file system
        self.fail("Local data storage test not implemented")

if __name__ == '__main__':
    unittest.main()
