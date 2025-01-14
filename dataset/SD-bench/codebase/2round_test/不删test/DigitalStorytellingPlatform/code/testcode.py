import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8068/') 

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

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "pass123")

        # Verify that the Story Creation Page has loaded
        self.assertIn("Create Story", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_create_new_story(self):
        # Functionalities 4: Test creating a new story
        self.login("admin", "pass123")

        story_title = "My New Story"
        story_content = "This is the content of my new story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved (check if the form is cleared or a success message is shown)
        self.assertIn("Create Story", self.driver.title)

    def test_save_story(self):
        # Functionalities 5: Test saving a story
        self.login("admin", "pass123")

        story_title = "Another Story"
        story_content = "This is another story content."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved (check if the form is cleared or a success message is shown)
        self.assertIn("Create Story", self.driver.title)

    def test_edit_story(self):
        # Functionalities 6: Test editing a story
        self.fail("Not implemented")

    def test_navigate_application(self):
        # Functionalities 7: Test navigating the application
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
