import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(2)  # Wait for the web application to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8128')

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Test case for user login
        self.login("admin1", "pass123")
        # Verify that the Story Creation Page has loaded
        self.assertIn("Create or Edit Story", self.driver.page_source)

    def test_navigate_to_registration_page(self):
        # Test case for navigating to the registration page
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
        self.login("admin1", "pass123")

        story_title = "My New Story"
        story_content = "This is the content of my new story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved
        with open('stories.txt', 'r') as file:
            stories = file.read()
            self.assertIn(f"admin1|{story_title}|{story_content}", stories)

    def test_saving_a_story(self):
        # Test case for saving a story
        self.login("admin1", "pass123")

        story_title = "Another Story"
        story_content = "This is another story content."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved
        with open('stories.txt', 'r') as file:
            stories = file.read()
            self.assertIn(f"admin1|{story_title}|{story_content}", stories)

    def test_editing_a_story(self):
        # Test case for editing a story
        self.login("admin1", "pass123")

        story_title = "My First Story"
        new_content = "This is the updated content of my first story."

        # Fill out the edit story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Edit Story"]').click()
        time.sleep(1)  # Wait for editing the story

        # Verify that the story is edited
        with open('stories.txt', 'r') as file:
            stories = file.read()
            self.assertIn(f"admin1|{story_title}|{new_content}", stories)

    def test_navigating_the_application(self):
        # Test case for navigating the application
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
