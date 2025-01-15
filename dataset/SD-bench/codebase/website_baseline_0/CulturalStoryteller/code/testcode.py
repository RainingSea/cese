import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8528')

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
        # Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Input username and password for registration
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Test user login functionality
        self.login("user1", "user123")

        # Verify that the Dashboard Page has loaded
        self.assertIn("Dashboard", self.driver.title)

        # Test invalid login
        self.driver.get('http://localhost:8528/login')
        self.login("invalid_user", "invalid_pass")
        self.assertIn("Invalid credentials!", self.driver.page_source)

    def test_explore_stories_on_dashboard(self):
        # Test exploring stories on the dashboard
        self.login("user1", "user123")

        # Verify that stories are displayed
        stories = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(stories), 0, "No stories found on the dashboard.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)
        self.assertIn("Story Details", self.driver.title)

    def test_search_for_stories(self):
        # Test searching for stories
        self.login("user1", "user123")

        # Enter a keyword in the search bar and submit
        self.driver.find_element(By.ID, 'query').send_keys("Bamboo")
        self.driver.find_element(By.XPATH, '//button[text()="Search"]').click()
        time.sleep(1)

        # Verify search results
        self.assertIn("Search Results", self.driver.title)
        self.assertIn("The Tale of the Bamboo Cutter", self.driver.page_source)

    def test_view_story_details(self):
        # Test viewing story details
        self.login("user1", "user123")

        # Click on a story title
        self.driver.find_elements(By.CLASS_NAME, 'list-group-item')[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify story details page
        self.assertIn("Story Details", self.driver.title)
        self.assertIn("The Tale of the Bamboo Cutter", self.driver.page_source)

    def test_bookmark_stories(self):
        # Test bookmarking stories
        self.login("user1", "user123")

        # Navigate to a story and bookmark it
        self.driver.find_elements(By.CLASS_NAME, 'list-group-item')[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify bookmark functionality (assuming a button exists)
        self.fail("Bookmark functionality not implemented")

    def test_view_and_manage_bookmarked_stories(self):
        # Test viewing and managing bookmarked stories
        self.login("user1", "user123")

        # Navigate to bookmarks page
        self.driver.get('http://localhost:8528/bookmarks')
        time.sleep(1)

        # Verify bookmarked stories
        self.assertIn("Your Bookmarked Stories", self.driver.page_source)

        # Test removing a bookmark (assuming functionality exists)
        self.fail("Remove bookmark functionality not implemented")

    def test_user_logout(self):
        # Test user logout functionality
        self.login("user1", "user123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        # Test local data storage functionality
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
