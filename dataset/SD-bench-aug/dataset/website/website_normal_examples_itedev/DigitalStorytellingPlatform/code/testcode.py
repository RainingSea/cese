import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(5)  # Wait for the web application to fully start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000')

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

    def test_user_login(self):
        # Test case for user login
        self.login("user1", "password1")

        # Verify that the Story Creation Page has loaded
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

    def test_creating_new_story(self):
        # Test case for creating a new story
        self.login("user1", "password1")

        story_title = "My New Story"
        story_content = "This is the content of my new story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the new story is displayed on the Story Creation Page
        self.assertIn(story_title, self.driver.page_source)

    def test_saving_story(self):
        # Test case for saving a story
        self.login("user1", "password1")

        story_title = "Another Story"
        story_content = "This is another story content."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved and displayed
        self.assertIn(story_title, self.driver.page_source)

    def test_editing_story(self):
        # Test case for editing a story
        self.login("user1", "password1")

        # Assuming a story titled "My New Story" exists
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)  # Wait for the edit page to load

        new_content = "Updated content for my story."
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Changes"]').click()
        time.sleep(1)  # Wait for saving the changes

        # Verify that the story content is updated
        self.assertIn(new_content, self.driver.page_source)

    def test_navigating_application(self):
        # Test case for navigating the application
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
