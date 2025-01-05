import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the web application
        self.process = subprocess.Popen(['python', 'main.py'])
        time.sleep(1)  # Wait a moment for the server to start
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8104/')  # Open the login page

    def tearDown(self):
        # Close the web driver session and stop the server
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
        self.login("admin", "adminpass")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

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
        self.login("admin", "adminpass")

        # Verify that the Home Page has loaded
        self.assertIn("Home", self.driver.title)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Test navigation to the Forum Page
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the next page to load

        # Verify that the Forum Page has loaded
        self.assertIn("Forum", self.driver.title)

    def test_create_new_thread(self):
        # Functionalities 6: Test creating a new thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the Forum Page to load

        self.driver.find_element(By.LINK_TEXT, 'Create New Thread').click()
        time.sleep(1)  # Wait for the Post Advice Page to load

        thread_title = "New Parenting Tips"
        thread_content = "Here are some new tips for parenting."

        # Fill out the new thread form
        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        time.sleep(1)  # Wait for the thread to be posted

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn(thread_title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: Test viewing a specific thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the Forum Page to load

        # Click on the first thread
        self.driver.find_element(By.LINK_TEXT, 'Parenting Tips').click()
        time.sleep(1)  # Wait for the View Thread Page to load

        # Verify that the View Thread Page has loaded
        self.assertIn("Parenting Tips", self.driver.title)

    def test_comment_on_thread(self):
        # Functionalities 8: Test commenting on a thread
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        time.sleep(1)  # Wait for the Forum Page to load

        # Click on the first thread
        self.driver.find_element(By.LINK_TEXT, 'Parenting Tips').click()
        time.sleep(1)  # Wait for the View Thread Page to load

        comment_content = "This is a test comment."

        # Submit a comment
        self.driver.find_element(By.NAME, 'content').send_keys(comment_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Comment"]').click()
        time.sleep(1)  # Wait for the comment to be posted

        # Verify that the comment is displayed
        self.assertIn(comment_content, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Test posting advice
        self.login("admin", "adminpass")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()
        time.sleep(1)  # Wait for the Post Advice Page to load

        advice_title = "Healthy Eating Tips"
        advice_content = "Here are some tips for healthy eating."

        # Fill out the post advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()
        time.sleep(1)  # Wait for the advice to be posted

        # Verify that the advice is displayed on the Forum Page
        self.assertIn(advice_title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
