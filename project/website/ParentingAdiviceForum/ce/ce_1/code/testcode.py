import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()  # Terminate the main application process

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//input[@value="Login"]').click()

    def test_user_login(self):
        # Functionalities 1: Test user login functionality
        self.driver.get('http://localhost:5000/login')
        self.login("admin", "admin123")

        # Verify that the Home Page has loaded
        self.assertIn("Welcome to the Forum", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Test navigation to the Registration Page
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.LINK_TEXT, 'Register').click()

        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_user_registration(self):
        # Functionalities 3: Test user registration functionality
        self.driver.get('http://localhost:5000/register')

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//input[@value="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_home_page_after_login(self):
        # Functionalities 4: Test viewing home page after logging in
        self.test_user_login()  # Log in first

        # Verify that the Home Page shows navigation links
        self.assertIn("Forum", self.driver.page_source)
        self.assertIn("Post Advice", self.driver.page_source)
        self.assertIn("My Account", self.driver.page_source)
        self.assertIn("Contact Us", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Test navigation to Forum Page
        self.test_user_login()  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()

        # Verify that the Forum Page has loaded
        self.assertIn("Discussion Threads", self.driver.page_source)

    def test_create_new_thread(self):
        # Functionalities 6: Test creating a new thread
        self.test_navigate_to_forum_page()  # Navigate to Forum Page
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()

        thread_title = "My New Thread"
        thread_content = "This is the content of my new thread."

        # Fill out the new thread form
        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//input[@value="Post Advice"]').click()

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn(thread_title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: Test viewing a specific thread
        self.test_create_new_thread()  # Create a thread first
        self.driver.find_element(By.LINK_TEXT, 'My New Thread').click()

        # Verify that the View Thread Page has loaded
        self.assertIn("Thread Title", self.driver.page_source)  # Adjust based on actual content

    def test_comment_on_thread(self):
        # Functionalities 8: Test commenting on a thread
        self.test_view_specific_thread()  # View a specific thread first

        comment_content = "This is a comment on the thread."
        self.driver.find_element(By.NAME, 'comment').send_keys(comment_content)
        self.driver.find_element(By.XPATH, '//input[@value="Submit Comment"]').click()

        # Verify that the comment is displayed below the thread
        self.assertIn(comment_content, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Test posting advice
        self.driver.get('http://localhost:5000/post_advice')

        advice_title = "My Advice Title"
        advice_content = "This is the content of my advice."

        # Fill out the post advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//input[@value="Post Advice"]').click()

        # Verify that the advice is displayed on the Post Advice Page
        self.assertIn(advice_title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
