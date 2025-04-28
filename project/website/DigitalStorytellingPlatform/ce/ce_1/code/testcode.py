import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestDigitalStorytellingPlatform(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8324/')  # Access the login page

    def tearDown(self):
        # Close the web driver session and the Flask application
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
        
        # Verify that the Story Creation Page has loaded
        self.assertIn("Create Story", self.driver.title)

    def test_navigate_to_registration_page(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

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

        # Enter a valid story title and content
        self.driver.find_element(By.NAME, 'title').send_keys("My New Story")
        self.driver.find_element(By.NAME, 'content').send_keys("This is the content of my new story.")
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the story is created successfully
        self.assertIn("My New Story", self.driver.page_source)

    def test_save_story(self):
        # Functionalities 5: Test saving a story
        self.login("admin", "admin123")

        # Enter a valid story title and content
        self.driver.find_element(By.NAME, 'title').send_keys("Another Story")
        self.driver.find_element(By.NAME, 'content').send_keys("This is another story content.")
        self.driver.find_element(By.XPATH, '//button[text()="Save Story"]').click()

        # Verify that the story is saved in the text file (not directly testable via Selenium)
        self.assertIn("Another Story", self.driver.page_source)

    def test_edit_story(self):
        # Functionalities 6: Test editing a story
        self.fail("Editing a story functionality is not implemented in the codebase.")

    def test_navigate_application(self):
        # Functionalities 7: Test navigating to the registration page from the login page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)

if __name__ == '__main__':
    unittest.main()
