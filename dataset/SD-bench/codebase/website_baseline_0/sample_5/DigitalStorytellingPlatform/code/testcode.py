import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'], cwd='D:\\algorithm\\agent\\cese\\dataset\\SD-bench\\codebase\\website\\DigitalStorytellingPlatform\\code')
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8453/')

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
        self.login("admin", "admin123")

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

        # Verify the user is redirected to the login page with a success message
        self.assertIn("Login", self.driver.title)
        self.assertIn("Registration successful", self.driver.page_source)

    def test_create_new_story(self):
        # Functionalities 4: Test creating a new story
        self.login("admin", "admin123")

        # Navigate to Create Story Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Story').click()
        time.sleep(1)  # Wait for the next page to load

        story_title = "My New Story"
        story_content = "This is the content of my new story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the new story is displayed on the View Stories Page
        self.assertIn(story_title, self.driver.page_source)

    def test_save_story(self):
        # Functionalities 5: Test saving a story
        self.login("admin", "admin123")

        # Navigate to Create Story Page
        self.driver.find_element(By.LINK_TEXT, 'Create New Story').click()
        time.sleep(1)  # Wait for the next page to load

        story_title = "My Saved Story"
        story_content = "This is the content of my saved story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Create Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is saved in the text file
        with open('/dataset/SD-bench/codebase/sample_5\\DigitalStorytellingPlatform\\code\\stories.txt', 'r') as file:
            stories = file.read()
            self.assertIn(story_title, stories)

    def test_edit_story(self):
        # Functionalities 6: Test editing a story
        self.login("admin", "admin123")

        # Navigate to Edit Story Page
        self.driver.find_element(By.LINK_TEXT, 'Edit').click()
        time.sleep(1)  # Wait for the next page to load

        new_content = "This is the updated content of my story."

        # Edit the story content
        content_field = self.driver.find_element(By.NAME, 'content')
        content_field.clear()
        content_field.send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Update Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the story is updated in the text file
        with open('/dataset/SD-bench/codebase/sample_5\\DigitalStorytellingPlatform\\code\\stories.txt', 'r') as file:
            stories = file.read()
            self.assertIn(new_content, stories)

    def test_navigate_application(self):
        # Functionalities 7: Test navigating the application
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
