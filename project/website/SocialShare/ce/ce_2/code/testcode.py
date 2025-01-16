import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8643/')  # Navigate to the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_registration(self):
        # Navigate to the Registration Page
        self.driver.get('http://localhost:8643/register')

        # Verify the Registration Page is displayed
        self.assertIn("Registration", self.driver.title)

        # Enter a valid username and password and submit the form
        self.driver.find_element(By.ID, 'username').send_keys('new_user')
        self.driver.find_element(By.ID, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify registration success message
        self.assertIn("Registration successful", self.driver.page_source)

        # Attempt to register with an existing username
        self.driver.find_element(By.ID, 'username').send_keys('admin')
        self.driver.find_element(By.ID, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)

        # Verify error message for existing username
        self.assertIn("username is already taken", self.driver.page_source)

    def test_user_login(self):
        # Verify the Login Page is displayed
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")

        # Verify redirection to the Dashboard Page
        self.assertIn("Feed", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8643/')
        self.login("admin", "wrongpassword")

        # Verify error message for invalid credentials
        self.assertIn("invalid credentials", self.driver.page_source)

    def test_profile_creation_and_update(self):
        # Login and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8643/profile')

        # Verify the Profile Page is displayed
        self.assertIn("Profile", self.driver.title)

        # Fill in the bio and save changes
        self.driver.find_element(By.ID, 'bio').send_keys('Updated bio')
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify profile update success message
        self.assertIn("Profile updated successfully", self.driver.page_source)

        # Leave the bio field empty and attempt to save changes
        self.driver.find_element(By.ID, 'bio').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Profile"]').click()
        time.sleep(1)

        # Verify error message for empty bio
        self.assertIn("bio cannot be empty", self.driver.page_source)

    def test_content_upload_and_sharing(self):
        self.fail("Not implemented")

    def test_content_discovery(self):
        # Login and navigate to the Feed Page
        self.login("admin", "admin123")
        self.driver.get('http://localhost:8643/feed')

        # Verify the Feed Page is displayed
        self.assertIn("Feed", self.driver.title)

        # Scroll through the feed and click on a shared article
        articles = self.driver.find_elements(By.CLASS_NAME, 'list-group-item')
        self.assertGreater(len(articles), 0, "No articles found in the feed.")

        # Refresh the discovery page after a new article has been uploaded
        self.driver.refresh()
        time.sleep(1)

        # Verify the newly uploaded article appears in the feed
        self.assertIn("Flask Tutorial", self.driver.page_source)

    def test_interacting_with_content(self):
        self.fail("Not implemented")

    def test_user_logout(self):
        # Login and logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)

        # Verify redirection to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Dashboard Page after logging out
        self.driver.get('http://localhost:8643/feed')
        self.assertIn("Login", self.driver.title)

    def test_user_interaction(self):
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
