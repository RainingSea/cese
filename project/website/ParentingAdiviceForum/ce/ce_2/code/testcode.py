import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess

class TestParentingAdviceForum(unittest.TestCase):

    def setUp(self):
        # Start the main application
        self.process = subprocess.Popen(['python', 'main.py'])
        self.driver = webdriver.Chrome()
        self.driver.get('http://localhost:5000/')  # Replace with the actual port from main.py

    def tearDown(self):
        # Close the web driver session
        self.driver.quit()
        self.process.terminate()  # Terminate the main application process

    def login(self, username, password):
        # Helper method to perform login
        self.driver.find_element(By.NAME, 'username').send_keys(username)
        self.driver.find_element(By.NAME, 'password').send_keys(password)
        self.driver.find_element(By.XPATH, '//button[text()="Login"]').click()

    def test_login(self):
        # Functionalities 1: User Login
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.login("admin", "admin123")
        
        # Verify that the Home Page has loaded
        self.assertIn("Welcome to Parenting Advice Forum", self.driver.page_source)

    def test_navigate_to_registration(self):
        # Functionalities 2: Navigate to Registration Page
        self.driver.get('http://localhost:5000/login')  # Navigate to login page
        self.driver.find_element(By.LINK_TEXT, 'Register').click()
        
        # Verify that the Registration Page has loaded
        self.assertIn("Register", self.driver.page_source)

    def test_registration(self):
        # Functionalities 3: User Registration
        self.driver.get('http://localhost:5000/register')  # Navigate to registration page

        new_username = "new_user"
        new_password = "new_password"

        # Input username and password for registration
        self.driver.find_element(By.NAME, 'username').send_keys(new_username)
        self.driver.find_element(By.NAME, 'password').send_keys(new_password)
        self.driver.find_element(By.XPATH, '//button[text()="Register"]').click()

        # Verify the user is redirected to the login page
        self.assertIn("Login", self.driver.page_source)

    def test_view_home_page_after_login(self):
        # Functionalities 4: View Home Page After Login
        self.test_login()  # Log in first

        # Verify that the Home Page shows navigation options
        self.assertIn("Forum", self.driver.page_source)
        self.assertIn("Post Advice", self.driver.page_source)
        self.assertIn("My Account", self.driver.page_source)
        self.assertIn("Contact Us", self.driver.page_source)

    def test_navigate_to_forum_page(self):
        # Functionalities 5: Navigate to Forum Page
        self.test_login()  # Log in first
        self.driver.find_element(By.LINK_TEXT, 'Forum').click()
        
        # Verify that the Forum Page has loaded
        self.assertIn("Forum Threads", self.driver.page_source)

    def test_create_new_thread(self):
        # Functionalities 6: Create New Thread
        self.test_navigate_to_forum_page()  # Navigate to forum page
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()  # Navigate to post advice page

        thread_title = "New Thread Title"
        thread_content = "This is the content of the new thread."

        # Fill out the new thread form
        self.driver.find_element(By.NAME, 'title').send_keys(thread_title)
        self.driver.find_element(By.NAME, 'content').send_keys(thread_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Advice"]').click()

        # Verify that the new thread is displayed on the Forum Page
        self.assertIn(thread_title, self.driver.page_source)

    def test_view_specific_thread(self):
        # Functionalities 7: View Specific Thread
        self.test_navigate_to_forum_page()  # Navigate to forum page
        self.driver.find_element(By.LINK_TEXT, 'Thread Title 1').click()  # Click on a specific thread
        
        # Verify that the View Thread Page has loaded
        self.assertIn("Thread Title", self.driver.page_source)

    def test_comment_on_thread(self):
        # Functionalities 8: Comment on a Thread
        self.test_view_specific_thread()  # Navigate to a specific thread
        comment_text = "This is a comment on the thread."

        # Fill out the comment form
        self.driver.find_element(By.NAME, 'comment').send_keys(comment_text)
        self.driver.find_element(By.XPATH, '//button[text()="Post Comment"]').click()

        # Verify that the comment is displayed below the thread
        self.assertIn(comment_text, self.driver.page_source)

    def test_post_advice(self):
        # Functionalities 9: Post Advice
        self.test_navigate_to_forum_page()  # Navigate to forum page
        self.driver.find_element(By.LINK_TEXT, 'Post Advice').click()  # Navigate to post advice page

        advice_title = "Advice Title"
        advice_content = "This is the content of the advice."

        # Fill out the advice form
        self.driver.find_element(By.NAME, 'title').send_keys(advice_title)
        self.driver.find_element(By.NAME, 'content').send_keys(advice_content)
        self.driver.find_element(By.XPATH, '//button[text()="Submit Advice"]').click()

        # Verify that the advice is displayed on the Post Advice Page
        self.assertIn(advice_title, self.driver.page_source)

if __name__ == '__main__':
    unittest.main()
