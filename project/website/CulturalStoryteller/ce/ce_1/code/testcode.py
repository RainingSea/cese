import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestCulturalStorytellerApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask app
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8606/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password, then submit
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify redirection to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Expectation: An error message is displayed (not implemented in codebase)
        self.fail("Error message for existing username not implemented")

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Dashboard", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8606/')  # Navigate back to login
        self.login("invalid_user", "wrong_password")

        # Expectation: An error message is displayed (not implemented in codebase)
        self.fail("Error message for invalid credentials not implemented")

    def test_explore_stories_on_dashboard(self):
        self.login("admin", "admin123")

        # Verify stories are displayed on the Dashboard Page
        stories = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertGreater(len(stories), 0, "No stories found on the Dashboard.")

        # Click on a story title
        stories[0].find_element(By.TAG_NAME, 'a').click()

        # Verify redirection to the Story Details Page
        self.assertIn("Story Details", self.driver.title)

    def test_search_for_stories(self):
        self.fail("Search functionality not implemented")

    def test_view_story_details(self):
        self.login("admin", "admin123")

        # Click on a story from the Dashboard Page
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()

        # Verify the Story Details Page is displayed
        self.assertIn("The Tortoise and the Hare", self.driver.title)

        # Check for the presence of a 'Bookmark' button
        bookmark_button = self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks')
        self.assertIsNotNone(bookmark_button)

    def test_bookmark_stories(self):
        self.login("admin", "admin123")

        # Navigate to the Story Details Page
        self.driver.find_element(By.LINK_TEXT, 'The Tortoise and the Hare').click()

        # Click the 'Add to Bookmarks' button
        self.driver.find_element(By.LINK_TEXT, 'Add to Bookmarks').click()

        # Verify the story is added to bookmarks
        self.driver.find_element(By.LINK_TEXT, 'My Bookmarks').click()
        bookmarks = self.driver.find_elements(By.TAG_NAME, 'li')
        self.assertIn('The Tortoise and the Hare', [b.text for b in bookmarks])

    def test_view_and_manage_bookmarked_stories(self):
        self.fail("Remove bookmark functionality not implemented")

    def test_user_logout(self):
        self.login("admin", "admin123")

        # Click the Logout button
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8606/dashboard')
        self.assertIn("Login", self.driver.title)

    def test_local_data_storage(self):
        self.fail("Local data storage functionality not implemented")

if __name__ == '__main__':
    unittest.main()
