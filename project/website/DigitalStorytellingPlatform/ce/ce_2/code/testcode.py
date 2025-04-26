import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import time

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8161/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the application
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()
        time.sleep(1)  # Wait for the next page to load

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Create Story", self.driver.title)  # Check if redirected to Story Creation Page

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load
        self.assertIn("Register", self.driver.title)  # Check if Registration Page has loaded

    def test_user_registration(self):
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
        self.login("admin", "admin123")

        # Navigate to Story Creation Page
        self.driver.get('http://localhost:8161/story')
        time.sleep(1)  # Wait for the next page to load

        story_title = "My New Story"
        story_content = "This is the content of my new story."

        # Fill out the new story form
        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()
        time.sleep(1)  # Wait for saving the story

        # Verify that the new story is saved (this would require checking the stories.txt file)
        self.assertIn(story_title, self.driver.page_source)

    def test_edit_story(self):
        # Functionalities 6: Test editing a story
        self.fail("Edit story functionality not implemented")  # Placeholder for unimplemented functionality

    def test_navigate_application(self):
        # Functionalities 7: Test navigation to the registration page from the login page
        self.test_navigate_to_registration()  # Reuse the test for navigation

if __name__ == '__main__':
    unittest.main()
