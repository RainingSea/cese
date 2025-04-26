import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace 5000 with the actual port from main.py

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.ID, 'username').send_keys(username)
        self.driver.find_element(By.ID, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the Story Creation Page has loaded
        self.assertIn("Create Story", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        new_username = "new_user"
        new_password = "new_password"
        new_email = "new_user@example.com"

        # Input username, password, and email for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.NAME, 'email').send_keys(new_email)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_create_new_story(self):
        # Functionalities 4: Test creating a new story
        self.login("admin", "admin123")

        # Fill out the story creation form
        story_title = "My New Story"
        story_content = "This is the content of my new story."

        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the story is saved in the text file (this would require additional implementation)
        self.assertIn("Story saved successfully", self.driver.page_source)

    def test_edit_story(self):
        # Functionalities 6: Test editing an existing story
        self.login("admin", "admin123")

        # Assuming the story to edit exists, fill out the edit form
        edit_title = "My New Story"
        new_content = "This is the updated content of my story."

        self.driver.find_element(By.NAME, 'edit_title').send_keys(edit_title)
        self.driver.find_element(By.NAME, 'new_content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Edit Story"]').click()

        # Verify that the story is edited successfully (this would require additional implementation)
        self.assertIn("Story edited successfully", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
