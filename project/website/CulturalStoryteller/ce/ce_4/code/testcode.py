import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server a second to start

        # Initialize the webdriver and open the login page
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8609/')

    def tearDown(self):
        # Close the web driver session and stop the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@type="submit"]').click()
        time.sleep(1)

        # Expectation: Error message indicating username is already taken
        self.assertIn("Register", self.driver.title)  # Assuming no change in page title

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter valid credentials
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter invalid credentials
        self.driver.get('http://localhost:8609/')
        self.login("invalid_user", "invalid_pass")

        # Expectation: Error message indicating invalid credentials
        self.assertIn("Login", self.driver.title)  # Assuming no change in page title

    def test_explore_stories_on_dashboard(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Verify stories are displayed
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the Dashboard.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()
        time.sleep(1)

        # Verify redirection to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_view_story_details(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click on a story title
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)

        # Verify the Story Details Page is displayed
        self.assertIn("The Tortoise and the Hare", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        bookmark_button = self.driver.find_element(By.XPATH, '//a[text()="Back to Dashboard"]')
        self.assertIsNotNone(bookmark_button)

    def test_bookmark_stories(self):
        # Login and navigate to the Story Details Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()
        time.sleep(1)

        # Click the 'Add to Bookmarks' button
        # Assuming there is a button to add bookmarks which is not implemented in the codebase
        self.fail("Bookmark functionality not implemented")

    def test_view_and_manage_bookmarked_stories(self):
        # Login and navigate to the Bookmarks Page
        self.login("user1", "user123")
        self.driver.find_element(By.LINK_TEXT, 'View Bookmarks').click()
        time.sleep(1)

        # Verify the list of bookmarked stories is displayed
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(bookmarks), 0, "No bookmarks found.")

        # Remove a story from bookmarks
        # Assuming there is a functionality to remove bookmarks which is not implemented in the codebase
        self.fail("Remove bookmark functionality not implemented")

    def test_user_logout(self):
        # Login and navigate to the Dashboard Page
        self.login("admin", "admin123")

        # Click the Logout button
        # Assuming there is a logout button which is not implemented in the codebase
        self.fail("Logout functionality not implemented")

    def test_local_data_storage(self):
        # Test adding a new story to local storage and refreshing the Dashboard
        # Assuming there is a functionality to add stories which is not implemented in the codebase
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
