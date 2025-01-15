import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8554/login')

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
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)  # Wait for the page to load

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password and submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify registration success
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, "Don't have an account? Register here.").click()
        time.sleep(1)  # Wait for the page to load
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify error message for existing username
        self.assertIn("Username already exists", self.driver.page_source)

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify access is granted and redirected to the Profile Page
        self.assertIn("Profile", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8554/login')
        self.login("invaliduser", "invalidpass")

        # Verify error message for invalid credentials
        self.assertIn("Invalid username or password", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Login and navigate to the Profile Page
        self.login("admin", "admin123")
        self.assertIn("Profile", self.driver.title)

        # Fill in the bio and save changes
        self.driver.find_element(By.NAME, 'bio').send_keys('This is my new bio.')
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify profile update success
        self.assertIn("Profile", self.driver.title)

        # Leave the bio field empty and attempt to save changes
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify error message for empty bio
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        # Login and navigate to the Feed Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8554/feed')
        self.assertIn("Feed", self.driver.title)

        # Upload a valid article
        self.driver.find_element(By.NAME, 'title').send_keys('New Article')
        self.driver.find_element(By.NAME, 'content').send_keys('This is the content of the new article.')
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify article sharing success
        self.assertIn("New Article", self.driver.page_source)

        # Attempt to upload an article with an empty title
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'content').send_keys('Content without a title.')
        self.driver.find_element(By.XPATH, '//button[text()="Share Article"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify error message for empty title
        self.assertIn("Title cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Login and navigate to the Feed Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8554/feed')
        self.assertIn("Feed", self.driver.title)

        # Verify feed content is displayed
        articles = self.driver.find_elements(By.TAG_NAME, 'h2')
        self.assertGreater(len(articles), 0, "No articles found in the feed.")

        # Refresh the page and verify new articles appear
        self.driver.refresh()
        time.sleep(1)  # Wait for the page to load
        self.assertGreater(len(articles), 0, "No articles found after refresh.")

    def test_interacting_with_content(self):
        # Login and navigate to the Feed Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8554/feed')
        self.assertIn("Feed", self.driver.title)

        # Like an article
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify like count increases
        self.assertIn("Likes: 1", self.driver.page_source)

        # Leave a comment on the article
        self.driver.find_element(By.NAME, 'content').send_keys('This is a comment.')
        self.driver.find_element(By.XPATH, '//button[text()="Comment"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify comment is displayed
        self.assertIn("This is a comment.", self.driver.page_source)

        # Attempt to like the same article again
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify error message for liking the same article again
        self.assertIn("Cannot like the same article multiple times", self.driver.page_source)

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the page to load

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Profile Page after logging out
        self.driver.get('http://localhost:8554/profile')
        self.assertIn("Login", self.driver.title)

    def test_user_interaction_follow(self):
        # Login and navigate to another user's profile
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8554/profile')
        self.assertIn("Profile", self.driver.title)

        # Follow a user
        self.driver.find_element(By.XPATH, '//button[text()="Follow"]').click()
        time.sleep(1)  # Wait for the page to load

        # Verify follow success
        self.assertIn("Unfollow", self.driver.page_source)

        # Attempt to send a message (not implemented in the current codebase)
        self.fail("Messaging functionality not implemented")

if __name__ == '__main__':
    unittest.main()
