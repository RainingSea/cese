import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestSocialShareApp(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8642/login')

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
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

        # Enter a valid username and password and submit the form
        self.driver.find_element(By.NAME, 'username').send_keys('new_user')
        self.driver.find_element(By.NAME, 'password').send_keys('new_password')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

        # Attempt to register with an existing username
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.driver.find_element(By.NAME, 'username').send_keys('admin')
        self.driver.find_element(By.NAME, 'password').send_keys('admin123')
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Check for error message indicating username is taken
        self.assertIn("Register", self.driver.title)  # Assuming it stays on the page

    def test_user_login(self):
        # Navigate to the Login Page
        self.assertIn("Login", self.driver.title)

        # Enter a valid username and password
        self.login("admin", "admin123")
        self.assertIn("Feed", self.driver.title)

        # Enter an invalid username or password
        self.driver.get('http://localhost:8642/login')
        self.login("invalid_user", "wrong_password")
        self.assertIn("Login", self.driver.title)

    def test_profile_creation_and_update(self):
        # Login and navigate to the Profile Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Profile').click()
        self.assertIn("Profile", self.driver.title)

        # Fill in the bio and save changes
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.NAME, 'bio').send_keys('New Bio')
        self.driver.find_element(By.XPATH, '//button[text()="Update Bio"]').click()
        time.sleep(1)  # Wait for the update

        # Leave the bio field empty and attempt to save changes
        self.driver.find_element(By.NAME, 'bio').clear()
        self.driver.find_element(By.XPATH, '//button[text()="Update Bio"]').click()
        time.sleep(1)  # Wait for the update
        self.assertIn("Profile", self.driver.title)  # Assuming it stays on the page

    def test_content_upload_and_sharing(self):
        # This functionality is not implemented in the codebase
        self.fail("Content upload and sharing functionality not implemented")

    def test_content_discovery(self):
        # Login and navigate to the Feed Page
        self.login("admin", "admin123")
        self.assertIn("Feed", self.driver.title)

        # Scroll through the feed and click on a shared article
        articles = self.driver.find_elements(By.TAG_NAME, 'h2')
        if articles:
            articles[0].click()
            time.sleep(1)  # Wait for the article details
            self.assertIn(articles[0].text, self.driver.page_source)

    def test_interacting_with_content(self):
        # This functionality is not implemented in the codebase
        self.fail("Interacting with content functionality not implemented")

    def test_user_logout(self):
        # Login and then logout
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Logout').click()
        time.sleep(1)  # Wait for the logout

        # Verify that the user is redirected to the Login Page
        self.assertIn("Login", self.driver.title)

        # Attempt to access the Feed Page after logging out
        self.driver.get('http://localhost:8642/feed')
        self.assertIn("Login", self.driver.title)

    def test_user_interaction(self):
        # This functionality is not implemented in the codebase
        self.fail("User interaction functionality not implemented")

if __name__ == '__main__':
    unittest.main()
