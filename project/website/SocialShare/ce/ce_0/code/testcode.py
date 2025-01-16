import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8641/') 

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
        # Functionality 1: User Registration
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify registration page loaded
        self.assertIn("Register", self.driver.title)

        # Register a new user
        new_username = "new_user"
        new_password = "new_password"
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'bio').send_keys("New user bio")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys("admin")
        self.driver.find_element(By.NAME, 'password').send_keys("admin123")
        self.driver.find_element(By.NAME, 'bio').send_keys("Duplicate user bio")
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the error message

        # Verify error message for existing username
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Functionality 2: User Login
        # Verify login page loaded
        self.assertIn("Login", self.driver.title)

        # Login with valid credentials
        self.login("admin", "admin123")

        # Verify redirection to feed page
        self.assertIn("Feed", self.driver.title)

        # Logout to test invalid login
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Login with invalid credentials
        self.login("invalid_user", "wrong_password")

        # Verify error message for invalid credentials
        self.assertIn("invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Functionality 3: Profile Creation and Update
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Go to Profile').click()
        time.sleep(1)

        # Verify profile page loaded
        self.assertIn("Profile", self.driver.title)

        # Update bio
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.NAME, 'bio').send_keys("Updated bio")
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)

        # Verify profile update confirmation
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Attempt to save empty bio
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Save"]').click()
        time.sleep(1)

        # Verify error message for empty bio
        self.assertIn("bio cannot be empty", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        # Functionality 4: Content Upload and Sharing
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Upload Content').click()
        time.sleep(1)

        # Verify content upload form loaded
        self.assertIn("Upload Content", self.driver.title)

        # Upload a valid article
        self.driver.find_element(By.NAME, 'title').send_keys("New Article")
        self.driver.find_element(By.NAME, 'content').send_keys("This is a new article.")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)

        # Verify article sharing confirmation
        self.assertIn("Article shared successfully", self.driver.page_source)

        # Attempt to upload article with empty title
        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys("Content without title.")
        self.driver.find_element(By.XPATH, '//button[text()="Share"]').click()
        time.sleep(1)

        # Verify error message for empty title
        self.assertIn("title cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Functionality 5: Content Discovery
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Discover').click()
        time.sleep(1)

        # Verify discovery page loaded
        self.assertIn("Discover", self.driver.title)

        # Check for articles in the feed
        articles = self.driver.find_elements(By.CLASS_NAME, 'article')
        self.assertGreater(len(articles), 0, "No articles found in the feed.")

        # Click on an article to view details
        articles[0].click()
        time.sleep(1)

        # Verify article details are displayed
        self.assertIn("Article Details", self.driver.title)

        # Refresh and check for new articles
        self.driver.refresh()
        time.sleep(1)
        new_articles = self.driver.find_elements(By.CLASS_NAME, 'article')
        self.assertGreaterEqual(len(new_articles), len(articles), "New article not found in the feed.")

    def test_interacting_with_content(self):
        # Functionality 6: Interacting with Content
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Discover').click()
        time.sleep(1)

        # Select an article
        article = self.driver.find_element(By.CLASS_NAME, 'article')
        article.click()
        time.sleep(1)

        # Like the article
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)

        # Verify like count increased
        like_count = self.driver.find_element(By.CLASS_NAME, 'like-count').text
        self.assertEqual(like_count, "1", "Like count did not increase.")

        # Leave a comment
        self.driver.find_element(By.NAME, 'comment').send_keys("Great article!")
        self.driver.find_element(By.XPATH, '//button[text()="Comment"]').click()
        time.sleep(1)

        # Verify comment is displayed
        comments = self.driver.find_elements(By.CLASS_NAME, 'comment')
        self.assertGreater(len(comments), 0, "Comment not displayed.")

        # Attempt to like the article again
        self.driver.find_element(By.XPATH, '//button[text()="Like"]').click()
        time.sleep(1)

        # Verify error message for multiple likes
        self.assertIn("cannot like the same article multiple times", self.driver.page_source)

    def test_user_logout(self):
        # Functionality 7: User Logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to login page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the feed page
        self.driver.get('http://localhost:8641/feed')
        time.sleep(1)

        # Verify redirection to login page with message
        self.assertIn("need to log in", self.driver.page_source)

    def test_user_interaction_follow_and_message(self):
        # Functionality 8: User Interaction (Follow and Message)
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Discover').click()
        time.sleep(1)

        # Navigate to another user's profile
        self.driver.find_element(By.LINK_TEXT, 'user1').click()
        time.sleep(1)

        # Follow the user
        self.driver.find_element(By.XPATH, '//button[text()="Follow"]').click()
        time.sleep(1)

        # Verify follow success
        self.assertIn("Unfollow", self.driver.page_source)

        # Send a message
        self.driver.find_element(By.XPATH, '//button[text()="Message"]').click()
        self.driver.find_element(By.NAME, 'message').send_keys("Hello!")
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)

        # Verify message sent confirmation
        self.assertIn("Message sent successfully", self.driver.page_source)

        # Attempt to send an empty message
        self.driver.find_element(By.XPATH, '//button[text()="Message"]').click()
        self.driver.find_element(By.NAME, 'message').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Send"]').click()
        time.sleep(1)

        # Verify error message for empty message
        self.assertIn("message cannot be empty", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
