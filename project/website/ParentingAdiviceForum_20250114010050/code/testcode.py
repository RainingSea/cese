import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Initialize the webdriver and open the login page
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Give the server time to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8461/login')

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
        # Functionalities 1: Test user login functionality
        self.login("admin", "admin123")

        # Verify that the user is redirected to the Forum Page
        self.assertIn("Forum", self.driver.title)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.title)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        time.sleep(1)  # Wait for the next page to load

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.title)

    def test_view_home_page_after_login(self):
        # Functionalities 4: Test viewing Home Page after logging in
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Test navigation to the Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Forum", self.driver.title)

    def test_create_new_thread(self):
        # Functionalities 6: Test creating a new thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        self.driver.find_element(By.LINK_TEXT, 'Create a New Thread').click()
        time.sleep(1)  # Wait for the next page to load

        thread_title = "New Thread Title"
        thread_content = "This is the content of the new thread."

        # Fill out the new thread form
        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the thread to be posted

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn(thread_title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: Test viewing a specific thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first thread
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the thread page displays the correct content
        self.assertIn("This is the content of the first thread.", self.driver.page_source)

    def test_comment_on_thread(self):
        # Functionalities 8: Test commenting on a thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Click on the first thread
        self.driver.find_element(By.LINK_TEXT, 'First Thread').click()
        time.sleep(1)  # Wait for the next page to load

        comment_content = "This is a new comment."

        # Add a comment
        self.driver.find_element(By.NAME, 'content').send_keys(comment_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()
        time.sleep(1)  # Wait for the comment to be posted

        # Verify that the comment is displayed on the thread page
        self.assertIn(comment_content, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Test posting advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)  # Wait for the next page to load

        advice_title = "New Advice Title"
        advice_content = "This is the content of the new advice."

        # Fill out the advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post"]').click()
        time.sleep(1)  # Wait for the advice to be posted

        # Verify that the advice is displayed on the Post Advice Page
        self.assertIn(advice_title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
