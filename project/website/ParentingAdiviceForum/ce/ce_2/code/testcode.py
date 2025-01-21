import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8970/')  # Access the login page

    def tearDown(self):
        # Close the web driver session
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

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_home_page_after_login(self):
        # Functionalities 4: Test viewing home page after logging in
        self.login("admin", "admin123")

        # Verify navigation links are present
        self.assertIn("Forum", self.driver.page_source)
        self.assertIn("Post Advice", self.driver.page_source)
        self.assertIn("My Account", self.driver.page_source)
        self.assertIn("Contact Us", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Test navigation to the Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()

        # Verify that the Forum Page has loaded
        self.assertIn("Forum Threads", self.driver.page_source)

    def test_create_new_thread(self):
        # Functionalities 6: Test creating a new thread
        self.fail("not implemented")

    def test_view_specific_thread(self):
        # Functionalities 7: Test viewing a specific thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()

        # Verify that the View Thread Page has loaded
        self.assertIn("First Thread", self.driver.page_source)

    def test_comment_on_thread(self):
        # Functionalities 8: Test commenting on a thread
        self.fail("not implemented")

    def test_post_advice(self):
        # Functionalities 9: Test posting advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()

        advice_title = "New Advice"
        advice_content = "This is a new piece of advice."

        # Fill out the advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()

        # Verify that the user is redirected to the Home Page
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
