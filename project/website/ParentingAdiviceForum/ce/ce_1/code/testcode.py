import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the Flask application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:8493/')  # Accessing the login page

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
        self.assertIn("Home", self.driver.title)  # Expectation: Redirected to Home Page

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        self.assertIn("Register", self.driver.title)  # Expectation: Redirected to Registration Page

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
        self.assertIn("Login", self.driver.title)

    def test_view_home_page_after_login(self):
        # Functionalities 4: Test viewing Home Page after logging in
        self.login("admin", "admin123")
        self.assertIn("Home", self.driver.title)  # Expectation: Redirected to Home Page

        # Check navigation links
        self.assertIn("Forum", self.driver.page_source)
        self.assertIn("Post Advice", self.driver.page_source)
        self.assertIn("My Account", self.driver.page_source)
        self.assertIn("Contact Us", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Test navigation to Forum Page
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.assertIn("Discussion Threads", self.driver.title)  # Expectation: Redirected to Forum Page

    def test_create_new_thread(self):
        # Functionalities 6: Test creating a new thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post New Advice').click()

        thread_title = "New Thread Title"
        thread_content = "This is the content of the new thread."

        # Fill out the new thread form
        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn(thread_title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: Test viewing a specific thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click the first thread
        self.assertIn("View Thread", self.driver.title)  # Expectation: Redirected to View Thread Page

    def test_comment_on_thread(self):
        # Functionalities 8: Test commenting on a thread
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        self.driver.find_element(By.XPATH, '//li/a').click()  # Click the first thread

        comment = "This is a comment."
        self.driver.find_element(By.NAME, 'comment').send_keys(comment)
        self.driver.find_element(By.XPATH, '//button[text()="Submit"]').click()

        # Verify that the comment is displayed below the thread
        self.assertIn(comment, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Test posting advice
        self.login("admin", "admin123")
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()

        advice_title = "Advice Title"
        advice_content = "This is some advice content."

        # Fill out the advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Post Advice"]').click()

        # Verify that the advice is posted successfully
        self.assertIn(advice_title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
