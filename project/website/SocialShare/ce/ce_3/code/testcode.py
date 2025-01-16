import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Allow some time for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8644/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and stop the server
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
        time.sleep(1)

        # Verify the Registration Page is displayed
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password and submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify successful registration
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys('newuser')
        self.driver.find_element(By.NAME, 'password').send_keys('newpassword')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("Username already exists!", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify successful login and redirection
        self.assertIn("Feed", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8644/')
        self.login("invaliduser", "invalidpassword")

        # Verify error message for invalid credentials
        self.assertIn("Invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Login and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)

        # Verify the Profile Page is displayed
        self.assertIn("Profile", self.driver.title)

        # Fill in the bio and personal information and save changes
        self.driver.find_element(By.NAME, 'bio').send_keys('New Bio')
        self.driver.find_element(By.NAME, 'personal_info').send_keys('{"age": 31, "location": "UK"}')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify successful profile update
        self.assertIn("Feed", self.driver.title)

        # Leave the bio field empty and attempt to save changes
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify error message for empty bio
        self.assertIn("Bio cannot be empty", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        # Login and navigate to the content upload section
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Upload Content').click()
        time.sleep(1)

        # Verify the content upload form is displayed
        self.assertIn("Upload Content", self.driver.title)

        # Upload a valid article and submit
        self.driver.find_element(By.NAME, 'article').send_keys('This is a new article.')
        self.driver.find_element(By.XPATH, '//button[text()="Upload"]').click()
        time.sleep(1)

        # Verify successful article upload
        self.assertIn("Feed", self.driver.title)

        # Attempt to upload an article with invalid content (empty article)
        self.driver.find_element(By.LINK_TEXT, 'Upload Content').click()
        time.sleep(1)
        self.driver.find_element(By.NAME, 'article').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Upload"]').click()
        time.sleep(1)

        # Verify error message for empty article
        self.assertIn("Article cannot be empty", self.driver.page_source)

    def test_content_discovery(self):
        # Login and navigate to the discovery page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Feed').click()
        time.sleep(1)

        # Verify the feed of content is displayed
        self.assertIn("Content Feed", self.driver.page_source)

        # Scroll through the feed and click on a shared article
        articles = self.driver.find_elements(By.TAG_NAME, 'li')
        if articles:
            articles[0].click()
            time.sleep(1)

            # Verify article details are displayed
            self.assertIn("Article Details", self.driver.page_source)

        # Refresh the discovery page after a new article has been uploaded
        self.driver.refresh()
        time.sleep(1)

        # Verify the newly uploaded article appears in the feed
        self.assertIn("This is a new article.", self.driver.page_source)

    def test_interacting_with_content(self):
        # Functionality not implemented in the codebase
        self.fail("Interacting with content functionality not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8644/feed')
        time.sleep(1)

        # Verify redirection back to the Login Page
        self.assertIn("Login", self.driver.title)

    def test_user_interaction_follow_and_message(self):
        # Functionality not implemented in the codebase
        self.fail("User interaction (follow and message) functionality not implemented")

if __name__ == '__main__':
    unittest.main()
