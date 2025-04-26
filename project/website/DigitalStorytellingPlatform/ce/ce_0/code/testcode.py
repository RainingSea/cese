import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8159/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and terminate the Flask app
        self.driver.quit()
        self.process.terminate()

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")
        self.assertIn("Create Story", self.driver.title)  # Check if redirected to Story Creation Page

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Check if Registration Page has loaded

    def test_user_registration(self):
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

        # Fill out the new story form
        story_title = "My New Story"
        story_content = "This is the content of my new story."

        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the new story is displayed on the page
        self.assertIn(story_title, self.driver.page_source)

    def test_save_story(self):
        # Functionalities 5: Test saving a story
        self.login("admin", "admin123")

        # Fill out the new story form
        story_title = "Another Story"
        story_content = "This is another story content."

        self.driver.find_element(By.NAME, 'title').send_keys(story_title)
        self.driver.find_element(By.NAME, 'content').send_keys(story_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the new story is saved and displayed
        self.assertIn(story_title, self.driver.page_source)

    def test_edit_story(self):
        # Functionalities 6: Test editing a story
        self.login("admin", "admin123")

        # Assuming we have a story titled "My New Story" to edit
        self.driver.find_element(By.LINK_TEXT, "My New Story").click()  # Navigate to the story
        new_title = "Edited Story Title"
        new_content = "This is the edited content of the story."

        self.driver.find_element(By.NAME, 'title').clear()
        self.driver.find_element(By.NAME, 'title').send_keys(new_title)
        self.driver.find_element(By.NAME, 'content').clear()
        self.driver.find_element(By.NAME, 'content').send_keys(new_content)
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the story is edited and displayed
        self.assertIn(new_title, self.driver.page_source)

    def test_navigate_to_registration_page(self):
        # Functionalities 7: Test navigating to the registration page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Check if Registration Page has loaded

if __name__ == '__main__':
    unittest.main()
