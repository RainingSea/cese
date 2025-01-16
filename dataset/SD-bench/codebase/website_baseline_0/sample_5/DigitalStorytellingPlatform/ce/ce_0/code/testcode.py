import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        # time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8068')

    def tearDown(self):
        # Close the web driver session and terminate the process
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test case for user login
        self.login("admin", "pass123")

        # Verify redirection to the Story Creation Page
        self.assertIn("Create Story", self.driver.page_source)

    def test_navigate_to_registration_page(self):
        # Test case for navigating to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Test case for user registration
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

    def test_creating_a_new_story(self):
        # Test case for creating a new story
        self.login("admin", "pass123")

        # Enter a valid story title and content
        story_title = "My New Story"
        story_content = "This is the content of my new story."
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for the story to be saved

        # Verify that the story is saved and displayed
        self.assertIn(story_title, self.driver.page_source)

    def test_saving_a_story(self):
        # Test case for saving a story
        self.login("admin", "pass123")

        # Enter a valid story title and content
        story_title = "Another Story"
        story_content = "This is another story content."
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for the story to be saved

        # Verify that the story is saved and displayed
        self.assertIn(story_title, self.driver.page_source)

    def test_editing_a_story(self):
        # Test case for editing a story
        self.fail("Editing a story functionality not implemented")

    def test_navigating_the_application(self):
        # Test case for navigating the application
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the registration page loads successfully
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
